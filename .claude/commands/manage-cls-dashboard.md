---
name: manage-cls-dashboard
description: 'Manage Tencent Cloud CLS (Cloud Log Service) dashboards. Use when: create CLS dashboard, list dashboards, delete dashboard, view dashboard config, build monitoring dashboard, set up log visualization, create charts for API usage, error rate dashboard, traffic monitoring, billing dashboard.'
argument-hint: 'What to do, e.g. "list all dashboards", "create API error rate dashboard", "get dashboard details for xxx"'
---

# CLS Dashboard Management

Create, list, view, and delete Tencent Cloud CLS dashboards for AceDataCloud monitoring.

## When to Use

- Create a new CLS monitoring dashboard
- List existing dashboards
- View dashboard configuration / chart definitions
- Delete a dashboard
- Build dashboards for API usage, error rates, traffic patterns, billing

## Quick Reference

```bash
DASH=.claude/scripts/cls_dashboard.py

# List all dashboards
python3 $DASH list

# Filter by name
python3 $DASH list --name "API"

# Get dashboard details (full config)
python3 $DASH get --id <dashboard-id>
python3 $DASH get --id <dashboard-id> --format json

# Create a dashboard (empty)
python3 $DASH create --name "My Dashboard"

# Create with data from JSON file
python3 $DASH create --name "API Errors" --data dashboard_config.json

# Create with tags
python3 $DASH create --name "Production" --tags env=prod team=platform

# Delete a dashboard
python3 $DASH delete --id <dashboard-id>

# Show available topic IDs (for chart queries)
python3 $DASH topics
```

## Credentials

Uses Tencent Cloud credentials from `PlatformBackend/.env` (auto-loaded):

| Variable                     | Description                |
|------------------------------|----------------------------|
| `TENCENT_CLOUD_SECRET_ID`    | Tencent Cloud API SecretId |
| `TENCENT_CLOUD_SECRET_KEY`   | Tencent Cloud API SecretKey|

## CLS Topics (for Dashboard Charts)

| Topic | ID | Contains |
|-------|----|----------|
| `trace` | `751a7350-dc5d-41c3-a6ca-c178bae05807` | PlatformGateway request traces |
| `api-usages` | `fbb6d4ce-4c55-418a-87e0-f6e15815b3a9` | API usage records (billing, costs) |

## Dashboard Data Format

The `--data` parameter accepts a JSON file or inline JSON string. The Data field is a JSON string containing the dashboard's chart/panel configuration. To understand the format:

1. **Create a dashboard manually** in the [CLS Console](https://console.cloud.tencent.com/cls/dashboard)
2. **Export its config** via: `python3 $DASH get --id <id> --format json`
3. **Use that as a template** for creating new dashboards programmatically

## Common Dashboard Patterns

### Create an API Error Monitoring Dashboard

1. First, query what error patterns exist:
   ```bash
   python3 .claude/scripts/cls_search.py --query "status_code:>=400 | SELECT api_name, status_code, count(*) as cnt GROUP BY api_name, status_code ORDER BY cnt DESC LIMIT 20" --topic api-usages --time 1d
   ```

2. Create a reference dashboard in CLS console with charts for:
   - Error count over time (by service)
   - Top erroring APIs
   - Error rate percentage
   - Status code distribution

3. Export and reuse:
   ```bash
   python3 $DASH get --id <id> --format json > templates/error_dashboard.json
   python3 $DASH create --name "API Errors (Copy)" --data templates/error_dashboard.json
   ```

### View Console Link

After creating a dashboard, the script outputs a direct console link:
```
https://console.cloud.tencent.com/cls/dashboard/<id>?region=ap-hongkong
```

## Procedure

### Build a new monitoring dashboard

1. **List existing dashboards** to check what already exists:
   ```bash
   python3 $DASH list
   ```

2. **If creating from scratch**, create an empty dashboard first:
   ```bash
   python3 $DASH create --name "Dashboard Name"
   ```
   Then configure charts in the CLS Console UI.

3. **If cloning an existing dashboard**, export then re-create:
   ```bash
   python3 $DASH get --id <source-id> --format json > /tmp/dash.json
   # Edit /tmp/dash.json as needed
   python3 $DASH create --name "New Dashboard" --data /tmp/dash.json
   ```

4. **Verify** the dashboard in console:
   Open the console link output by the create command.
