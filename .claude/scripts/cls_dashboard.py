#!/usr/bin/env python3
"""
Tencent Cloud CLS Dashboard Management Tool

Create, list, delete, and describe CLS dashboards.
Uses direct API calls since the SDK may be outdated.

Usage:
  python3 .claude/scripts/cls_dashboard.py list
  python3 .claude/scripts/cls_dashboard.py get --id <dashboard-id>
  python3 .claude/scripts/cls_dashboard.py create --name <name> --data <json-file-or-string>
  python3 .claude/scripts/cls_dashboard.py delete --id <dashboard-id>

Environment:
  Reads TENCENT_CLOUD_SECRET_ID and TENCENT_CLOUD_SECRET_KEY from
  PlatformBackend/.env
"""

import argparse
import hashlib
import hmac
import json
import os
import sys
import time
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
DOTENV_PATH = os.path.join(PROJECT_ROOT, "PlatformBackend", ".env")

REGION = "ap-hongkong"
SERVICE = "cls"
HOST = "cls.tencentcloudapi.com"
API_VERSION = "2020-10-16"

# CLS topic IDs for reference when building dashboard data
TOPICS = {
    "trace": "751a7350-dc5d-41c3-a6ca-c178bae05807",
    "api-usages": "fbb6d4ce-4c55-418a-87e0-f6e15815b3a9",
}


def load_env(path):
    if not os.path.isfile(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip("'\"")
            if key not in os.environ:
                os.environ[key] = value


load_env(DOTENV_PATH)


def sign_tc3(secret_id, secret_key, action, payload, timestamp=None):
    """Generate Tencent Cloud TC3-HMAC-SHA256 signature."""
    if timestamp is None:
        timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")

    # Step 1: canonical request
    http_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    canonical_headers = f"content-type:{ct}\nhost:{HOST}\nx-tc-action:{action.lower()}\n"
    signed_headers = "content-type;host;x-tc-action"
    payload_str = json.dumps(payload)
    hashed_payload = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
    canonical_request = f"{http_method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{hashed_payload}"

    # Step 2: string to sign
    algorithm = "TC3-HMAC-SHA256"
    credential_scope = f"{date}/{SERVICE}/tc3_request"
    hashed_canonical = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = f"{algorithm}\n{timestamp}\n{credential_scope}\n{hashed_canonical}"

    # Step 3: signing key
    def _hmac_sha256(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = _hmac_sha256(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = _hmac_sha256(secret_date, SERVICE)
    secret_signing = _hmac_sha256(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    # Step 4: authorization
    authorization = (
        f"{algorithm} Credential={secret_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )
    return authorization, timestamp, payload_str


def call_api(action, payload):
    """Call Tencent Cloud CLS API."""
    import requests

    secret_id = os.environ.get("TENCENT_CLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENT_CLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("ERROR: TENCENT_CLOUD_SECRET_ID and TENCENT_CLOUD_SECRET_KEY required", file=sys.stderr)
        sys.exit(1)

    timestamp = int(time.time())
    authorization, _, payload_str = sign_tc3(secret_id, secret_key, action, payload, timestamp)

    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": HOST,
        "X-TC-Action": action,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": API_VERSION,
        "X-TC-Region": REGION,
    }

    resp = requests.post(f"https://{HOST}", headers=headers, data=payload_str, timeout=30)
    result = resp.json()

    if "Response" in result and "Error" in result["Response"]:
        err = result["Response"]["Error"]
        print(f"ERROR: [{err['Code']}] {err['Message']}", file=sys.stderr)
        sys.exit(1)

    return result.get("Response", result)


def cmd_list(args):
    """List all dashboards."""
    payload = {"Offset": args.offset, "Limit": args.limit}
    if args.name:
        payload["Filters"] = [{"Key": "dashboardName", "Values": [args.name]}]

    result = call_api("DescribeDashboards", payload)
    dashboards = result.get("DashboardInfos", [])
    total = result.get("TotalCount", len(dashboards))

    print(f"Total dashboards: {total}\n")
    for d in dashboards:
        print(f"  ID:       {d.get('DashboardId', 'N/A')}")
        print(f"  Name:     {d.get('DashboardName', 'N/A')}")
        print(f"  Created:  {d.get('CreateTime', 'N/A')}")
        print(f"  Updated:  {d.get('UpdateTime', 'N/A')}")
        region = d.get("DashboardRegion", "")
        if region:
            print(f"  Region:   {region}")
        topics = d.get("DashboardTopicInfos", [])
        if topics:
            print(f"  Topics:   {', '.join(t.get('TopicId', '') for t in topics)}")
        tags = d.get("Tags", [])
        if tags:
            tag_strs = [f"{t.get('Key')}={t.get('Value')}" for t in tags]
            print(f"  Tags:     {', '.join(tag_strs)}")
        print()


def cmd_get(args):
    """Get a specific dashboard's full data."""
    payload = {
        "Offset": 0,
        "Limit": 1,
        "Filters": [{"Key": "dashboardId", "Values": [args.id]}],
    }
    result = call_api("DescribeDashboards", payload)
    dashboards = result.get("DashboardInfos", [])
    if not dashboards:
        print(f"Dashboard not found: {args.id}", file=sys.stderr)
        sys.exit(1)

    d = dashboards[0]
    if args.format == "json":
        print(json.dumps(d, indent=2, ensure_ascii=False))
    else:
        print(f"ID:       {d.get('DashboardId')}")
        print(f"Name:     {d.get('DashboardName')}")
        print(f"Created:  {d.get('CreateTime')}")
        print(f"Updated:  {d.get('UpdateTime')}")
        data = d.get("Data", "")
        if data:
            try:
                parsed = json.loads(data)
                print(f"\nData (formatted):\n{json.dumps(parsed, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"\nData (raw):\n{data}")


def cmd_create(args):
    """Create a new dashboard."""
    payload = {"DashboardName": args.name}

    if args.data:
        if os.path.isfile(args.data):
            with open(args.data) as f:
                data_str = f.read()
        else:
            data_str = args.data
        # Validate it's valid JSON
        try:
            json.loads(data_str)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON data: {e}", file=sys.stderr)
            sys.exit(1)
        payload["Data"] = data_str

    if args.tags:
        tags = []
        for t in args.tags:
            k, _, v = t.partition("=")
            tags.append({"Key": k, "Value": v})
        payload["Tags"] = tags

    result = call_api("CreateDashboard", payload)
    dashboard_id = result.get("DashboardId", "N/A")
    print(f"Dashboard created successfully!")
    print(f"  ID: {dashboard_id}")
    print(f"  Name: {args.name}")
    print(f"\nView in console: https://console.cloud.tencent.com/cls/dashboard/{dashboard_id}?region={REGION}")


def cmd_delete(args):
    """Delete a dashboard."""
    payload = {"DashboardId": args.id}
    call_api("DeleteDashboard", payload)
    print(f"Dashboard deleted: {args.id}")


def cmd_topics(args):
    """Show available CLS topic IDs for dashboard configuration."""
    print("Available CLS Topics (ap-hongkong):\n")
    for name, topic_id in TOPICS.items():
        print(f"  {name}: {topic_id}")
    print("\nUse these topic IDs when configuring dashboard chart queries.")


def main():
    parser = argparse.ArgumentParser(description="Tencent Cloud CLS Dashboard Manager")
    sub = parser.add_subparsers(dest="command", help="Command")

    # list
    p_list = sub.add_parser("list", help="List dashboards")
    p_list.add_argument("--name", help="Filter by dashboard name (fuzzy)")
    p_list.add_argument("--offset", type=int, default=0)
    p_list.add_argument("--limit", type=int, default=100)

    # get
    p_get = sub.add_parser("get", help="Get dashboard details")
    p_get.add_argument("--id", required=True, help="Dashboard ID")
    p_get.add_argument("--format", choices=["text", "json"], default="text")

    # create
    p_create = sub.add_parser("create", help="Create a dashboard")
    p_create.add_argument("--name", required=True, help="Dashboard name")
    p_create.add_argument("--data", help="Dashboard data JSON (file path or inline string)")
    p_create.add_argument("--tags", nargs="*", help="Tags as key=value pairs")

    # delete
    p_delete = sub.add_parser("delete", help="Delete a dashboard")
    p_delete.add_argument("--id", required=True, help="Dashboard ID")

    # topics
    sub.add_parser("topics", help="Show available CLS topic IDs")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {"list": cmd_list, "get": cmd_get, "create": cmd_create, "delete": cmd_delete, "topics": cmd_topics}
    cmds[args.command](args)


if __name__ == "__main__":
    main()
