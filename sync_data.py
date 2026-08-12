import json
import requests

# Example: Pulling live NFL depth chart metadata from Sleeper's open API
url = "https://api.sleeper.app/v1/players/nfl"
response = requests.get(url)
sleeper_players = response.json() if response.status_code == 200 else {}

# Maps names to live teams and depth positions
depth_map = {}
for p_id, p in sleeper_players.items():
    full_name = f"{p.get('first_name', '')} {p.get('last_name', '')}".strip()
    team = p.get('team') or 'FA'
    depth_pos = p.get('depth_chart_position') or p.get('position') or ''
    depth_order = p.get('depth_chart_order')
    depth_label = f"{depth_pos}{depth_order}" if (depth_pos and depth_order) else depth_pos
    depth_map[full_name] = {"team": team, "depth": depth_label}

print(f"Loaded live metadata for {len(depth_map)} players.")
