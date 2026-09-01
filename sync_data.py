import json
import requests

VALID_NFL_TEAMS = {
    'ARI', 'ATL', 'BAL', 'BUF', 'CAR', 'CHI', 'CIN', 'CLE',
    'DAL', 'DEN', 'DET', 'GB', 'HOU', 'IND', 'JAX', 'KC',
    'LAC', 'LAR', 'LV', 'MIA', 'MIN', 'NE', 'NO', 'NYG',
    'NYJ', 'PHI', 'PIT', 'SEA', 'SF', 'TB', 'TEN', 'WAS'
}

def fetch_sleeper_data():
    players_data = {}
    projections_map = {}

    try:
        res = requests.get("https://api.sleeper.app/v1/players/nfl", timeout=30)
        if res.status_code == 200:
            players_data = res.json()
            print(f"✓ Fetched {len(players_data)} player records from Sleeper metadata.")
    except Exception as e:
        print(f"Warning: Player metadata fetch failed: {e}")

    headers = {"User-Agent": "Mozilla/5.0"}
    projection_urls = [
        "https://api.sleeper.app/projections/nfl/2026?season_type=regular&position[]=QB&position[]=RB&position[]=WR&position[]=TE&position[]=K&position[]=DEF",
        "https://api.sleeper.app/projections/nfl/2026?season_type=regular",
        "https://api.sleeper.app/projections/nfl/regular/2026",
        "https://api.sleeper.app/projections/nfl/2025?season_type=regular"
    ]

    for url in projection_urls:
        try:
            res = requests.get(url, headers=headers, timeout=25)
            if res.status_code == 200:
                data = res.json()
                parsed = parse_projections_response(data)
                if len(parsed) > 50:
                    projections_map = parsed
                    print(f"✓ Fetched live projections for {len(projections_map)} players from {url}")
                    break
        except Exception:
            continue

    return players_data, projections_map

def parse_projections_response(data):
    proj_map = {}
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict):
                continue
            pid = str(item.get("player_id") or "")
            stats = item.get("stats") or item
            if pid:
                proj_map[pid] = stats
    elif isinstance(data, dict):
        for pid, val in data.items():
            if isinstance(val, dict):
                stats = val.get("stats") or val
                proj_map[str(pid)] = stats
    return proj_map

def normalize_name(name):
    if not name:
        return ""
    cleaned = name.lower().replace(".", "").replace("'", "").replace("-", " ").strip()
    tokens = cleaned.split()
    suffixes = {"jr", "sr", "ii", "iii", "iv", "v"}
    if tokens and tokens[-1] in suffixes:
        tokens = tokens[:-1]
    return " ".join(tokens)

DEFAULT_ROLE_STATS = {
    "QB1": {"passYds": 3400, "passTd": 20, "int": 11, "rushYds": 200, "rushTd": 2, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2},
    "QB2": {"passYds": 2800, "passTd": 15, "int": 9, "rushYds": 100, "rushTd": 1, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2},
    "RB1": {"passYds": 0, "passTd": 0, "int": 0, "rushYds": 950, "rushTd": 8, "rec": 40, "recYds": 300, "recTd": 2, "fum": 1},
    "RB2": {"passYds": 0, "passTd": 0, "int": 0, "rushYds": 550, "rushTd": 4, "rec": 25, "recYds": 180, "recTd": 1, "fum": 1},
    "RB3": {"passYds": 0, "passTd": 0, "int": 0, "rushYds": 300, "rushTd": 2, "rec": 15, "recYds": 100, "recTd": 0, "fum": 0},
    "WR1": {"passYds": 0, "passTd": 0, "int": 0, "rushYds": 20, "rushTd": 0, "rec": 80, "recYds": 1000, "recTd": 6, "fum": 1},
    "WR2": {"passYds": 0, "passTd": 0, "int": 0, "rushYds": 15, "rushTd": 0, "rec": 60, "recYds": 750, "recTd": 5, "fum": 1},
    "WR3": {"passYds": 0, "passTd": 0, "int": 0, "rushYds": 0, "rushTd": 0, "rec": 45, "recYds": 550, "recTd": 3, "fum": 1},
    "WR4": {"passYds": 0, "passTd": 0, "int": 0, "rushYds": 0, "rushTd": 0, "rec": 30, "recYds": 380, "recTd": 2, "fum": 0},
    "TE1": {"passYds": 0, "passTd": 0, "int": 0, "rushYds": 0, "rushTd": 0, "rec": 60, "recYds": 650, "recTd": 5, "fum": 1},
    "TE2": {"passYds": 0, "passTd": 0, "int": 0, "rushYds": 0, "rushTd": 0, "rec": 35, "recYds": 380, "recTd": 3, "fum": 1},
    "K1":  {"fgYds": 1150, "pat": 36},
    "DST": {"pts": 110.0}
}

def main():
    players_raw, projections_map = fetch_sleeper_data()
    deduped_players = {}

    for pid, s_player in players_raw.items():
        pos = s_player.get("position")
        if pos not in ["QB", "RB", "WR", "TE", "K", "DEF"]:
            continue

        status = s_player.get("status")
        if status in ["Inactive", "Injured Reserve", "Retired"]:
            continue

        depth_order = s_player.get("depth_chart_order")

        # 1. Defenses: Ensure valid 32-team assignment
        if pos == "DEF":
            def_team = s_player.get("team") or s_player.get("player_id")
            if def_team not in VALID_NFL_TEAMS:
                continue

            first_name = s_player.get("first_name", "")
            last_name = s_player.get("last_name", "")
            base_team_name = f"{first_name} {last_name}".strip() or s_player.get("full_name") or def_team
            display_name = base_team_name if base_team_name.endswith("DEF") else f"{base_team_name} DEF"
            norm_key = normalize_name(display_name)

            stats = projections_map.get(str(pid), {})
            def_pts = stats.get("pts_std") or stats.get("pts_half_ppr") or stats.get("pts_ppr") or 110.0

            deduped_players[norm_key] = {
                "name": display_name,
                "pos": "DEF",
                "team": def_team,
                "depth": "DST",
                "pts": float(def_pts)
            }
            continue

        # 2. Skill Players: STRICT VALIDATION (Must be on an active 32 NFL team)
        team = s_player.get("team")
        if not team or team not in VALID_NFL_TEAMS:
            continue  # Drops cut players, free agents, and numeric IDs

        # Positional depth boundaries
        is_relevant = (
            (pos == "QB" and (not depth_order or depth_order <= 3)) or
            (pos == "RB" and (not depth_order or depth_order <= 4)) or
            (pos == "WR" and (not depth_order or depth_order <= 6)) or
            (pos == "TE" and (not depth_order or depth_order <= 3)) or
            (pos == "K"  and (not depth_order or depth_order <= 1))
        )
        if not is_relevant:
            continue

        display_name = (
            s_player.get("full_name") or 
            f"{s_player.get('first_name', '')} {s_player.get('last_name', '')}".strip()
        )
        if len(display_name) < 3:
            continue

        norm_key = normalize_name(display_name)
        depth_tag = f"{pos}{depth_order}" if depth_order else f"{pos}1"
        fallback = DEFAULT_ROLE_STATS.get(depth_tag, DEFAULT_ROLE_STATS.get(f"{pos}1", {}))
        stats = projections_map.get(str(pid), {})

        if pos == "K":
            fg_yds = stats.get("fgm_yds", 0)
            if not fg_yds:
                fg_yds = (
                    stats.get("fgm_0_19", 0) * 15 +
                    stats.get("fgm_20_29", 0) * 25 +
                    stats.get("fgm_30_39", 0) * 35 +
                    stats.get("fgm_40_49", 0) * 45 +
                    stats.get("fgm_50p", 0) * 53
                )
            if not fg_yds and stats.get("fgm", 0):
                fg_yds = stats.get("fgm", 0) * 38
            if not fg_yds and fallback:
                fg_yds = fallback.get("fgYds", 1150)

            pat = stats.get("xpm", 0) or stats.get("xp", 0) or (fallback.get("pat", 35) if fallback else 35)

            player_entry = {
                "name": display_name,
                "pos": "K",
                "team": team,
                "depth": depth_tag,
                "fgYds": int(fg_yds),
                "pat": int(pat)
            }
        else:
            pass_yds = stats.get("pass_yd") if stats.get("pass_yd") is not None else fallback.get("passYds", 0)
            pass_td  = stats.get("pass_td") if stats.get("pass_td") is not None else fallback.get("passTd", 0)
            pass_int = stats.get("pass_int") if stats.get("pass_int") is not None else fallback.get("int", 0)
            rush_yds = stats.get("rush_yd") if stats.get("rush_yd") is not None else fallback.get("rushYds", 0)
            rush_td  = stats.get("rush_td") if stats.get("rush_td") is not None else fallback.get("rushTd", 0)
            rec      = stats.get("rec") if stats.get("rec") is not None else fallback.get("rec", 0)
            rec_yds  = stats.get("rec_yd") if stats.get("rec_yd") is not None else fallback.get("recYds", 0)
            rec_td   = stats.get("rec_td") if stats.get("rec_td") is not None else fallback.get("recTd", 0)
            fum      = stats.get("fum_lost") if stats.get("fum_lost") is not None else fallback.get("fum", 0)

            player_entry = {
                "name": display_name,
                "pos": pos,
                "team": team,
                "depth": depth_tag,
                "passYds": int(round(pass_yds or 0)),
                "passTd": int(round(pass_td or 0)),
                "int": int(round(pass_int or 0)),
                "rushYds": int(round(rush_yds or 0)),
                "rushTd": int(round(rush_td or 0)),
                "rec": int(round(rec or 0)),
                "recYds": int(round(rec_yds or 0)),
                "recTd": int(round(rec_td or 0)),
                "fum": int(round(fum or 0))
            }

        if norm_key in deduped_players:
            existing = deduped_players[norm_key]
            current_activity = (player_entry.get("passYds", 0) + player_entry.get("rushYds", 0) + player_entry.get("recYds", 0))
            existing_activity = (existing.get("passYds", 0) + existing.get("rushYds", 0) + existing.get("recYds", 0))
            if current_activity > existing_activity:
                deduped_players[norm_key] = player_entry
        else:
            deduped_players[norm_key] = player_entry

    final_player_list = list(deduped_players.values())

    # Circuit breaker: Protect existing file if payload is anomalously small
    if len(final_player_list) < 50:
        print("⚠️ API returned insufficient records. Aborting write to protect draft board.")
        return

    with open("projections.json", "w") as f:
        json.dump(final_player_list, f, indent=2)

    print(f"✓ Saved {len(final_player_list)} active NFL players with verified team codes to projections.json.")

if __name__ == "__main__":
    main()
