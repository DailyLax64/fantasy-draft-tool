import json
import requests

def fetch_live_depth_and_teams():
    """Fetches real-time depth chart & team status from Sleeper's free NFL API."""
    url = "https://api.sleeper.app/v1/players/nfl"
    try:
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            data = res.json()
            mapping = {}
            for pid, p in data.items():
                first = p.get('first_name', '') or ''
                last = p.get('last_name', '') or ''
                full_name = f"{first} {last}".strip()
                
                pos = p.get('position', '')
                team = p.get('team') or 'FA'
                depth_order = p.get('depth_chart_order')
                depth_label = f"{pos}{depth_order}" if (pos and depth_order) else (p.get('depth_chart_position') or pos)

                if full_name:
                    mapping[full_name.lower()] = {
                        "team": team,
                        "depth": depth_label
                    }
            return mapping
    except Exception as e:
        print(f"Warning: Could not fetch Sleeper API: {e}")
    return {}

# Baseline player projections dataset
BASE_PLAYERS = [
    # QBs
    { "name": "Josh Allen", "pos": "QB", "team": "BUF", "depth": "QB1", "passYds": 3800, "passTd": 28, "int": 11, "rushYds": 540, "rushTd": 10, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2 },
    { "name": "Lamar Jackson", "pos": "QB", "team": "BAL", "depth": "QB1", "passYds": 3500, "passTd": 27, "int": 8, "rushYds": 720, "rushTd": 5, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2 },
    { "name": "Drake Maye", "pos": "QB", "team": "NE", "depth": "QB1", "passYds": 4050, "passTd": 28, "int": 10, "rushYds": 480, "rushTd": 4, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2 },
    { "name": "Jayden Daniels", "pos": "QB", "team": "WAS", "depth": "QB1", "passYds": 3650, "passTd": 23, "int": 9, "rushYds": 650, "rushTd": 6, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2 },
    { "name": "Jalen Hurts", "pos": "QB", "team": "PHI", "depth": "QB1", "passYds": 3600, "passTd": 25, "int": 10, "rushYds": 520, "rushTd": 9, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2 },
    { "name": "Joe Burrow", "pos": "QB", "team": "CIN", "depth": "QB1", "passYds": 4300, "passTd": 34, "int": 10, "rushYds": 180, "rushTd": 2, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2 },
    { "name": "Caleb Williams", "pos": "QB", "team": "CHI", "depth": "QB1", "passYds": 3850, "passTd": 26, "int": 10, "rushYds": 410, "rushTd": 3, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2 },
    { "name": "Patrick Mahomes", "pos": "QB", "team": "KC", "depth": "QB1", "passYds": 4200, "passTd": 30, "int": 10, "rushYds": 320, "rushTd": 2, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2 },
    { "name": "Bo Nix", "pos": "QB", "team": "DEN", "depth": "QB1", "passYds": 3750, "passTd": 26, "int": 11, "rushYds": 390, "rushTd": 4, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2 },
    { "name": "Dak Prescott", "pos": "QB", "team": "DAL", "depth": "QB1", "passYds": 4150, "passTd": 29, "int": 11, "rushYds": 200, "rushTd": 2, "rec": 0, "recYds": 0, "recTd": 0, "fum": 2 },
    
    # RBs
    { "name": "Jahmyr Gibbs", "pos": "RB", "team": "DET", "depth": "RB1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 1480, "rushTd": 14, "rec": 73, "recYds": 650, "recTd": 6, "fum": 2 },
    { "name": "Bijan Robinson", "pos": "RB", "team": "ATL", "depth": "RB1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 1630, "rushTd": 12, "rec": 74, "recYds": 650, "recTd": 5, "fum": 2 },
    { "name": "James Cook III", "pos": "RB", "team": "BUF", "depth": "RB1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 1560, "rushTd": 12, "rec": 32, "recYds": 280, "recTd": 4, "fum": 1 },
    { "name": "Saquon Barkley", "pos": "RB", "team": "PHI", "depth": "RB1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 1460, "rushTd": 13, "rec": 30, "recYds": 260, "recTd": 3, "fum": 2 },
    { "name": "Jonathan Taylor", "pos": "RB", "team": "IND", "depth": "RB1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 1370, "rushTd": 13, "rec": 38, "recYds": 290, "recTd": 2, "fum": 2 },
    { "name": "Quinshon Judkins", "pos": "RB", "team": "CLE", "depth": "RB1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 860, "rushTd": 7, "rec": 28, "recYds": 210, "recTd": 1, "fum": 1 },
    { "name": "De'Von Achane", "pos": "RB", "team": "MIA", "depth": "RB1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 1150, "rushTd": 8, "rec": 65, "recYds": 490, "recTd": 3, "fum": 1 },
    { "name": "Derrick Henry", "pos": "RB", "team": "BAL", "depth": "RB1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 1420, "rushTd": 12, "rec": 20, "recYds": 160, "recTd": 0, "fum": 2 },

    # WRs
    { "name": "Jaxon Smith-Njigba", "pos": "WR", "team": "SEA", "depth": "WR1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 30, "rushTd": 0, "rec": 111, "recYds": 1568, "recTd": 9, "fum": 1 },
    { "name": "Puka Nacua", "pos": "WR", "team": "LAR", "depth": "WR1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 106, "rushTd": 1, "rec": 123, "recYds": 1590, "recTd": 10, "fum: 1 },
    { "name": "Ja'Marr Chase", "pos": "WR", "team": "CIN", "depth": "WR1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 40, "rushTd": 0, "rec": 121, "recYds": 1512, "recTd": 11, "fum": 1 },
    { "name": "Amon-Ra St. Brown", "pos": "WR", "team": "DET", "depth": "WR1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 25, "rushTd": 0, "rec": 117, "recYds": 1391, "recTd": 10, "fum": 1 },
    { "name": "Justin Jefferson", "pos": "WR", "team": "MIN", "depth": "WR1", "passYds": 0, "passTd": 0, "int": 0, "rushYds: 15, "rushTd": 0, "rec": 99, "recYds": 1302, "recTd": 8, "fum": 1 },
    { "name": "CeeDee Lamb", "pos": "WR", "team": "DAL", "depth": "WR1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 60, "rushTd": 1, "rec": 97, "recYds": 1296, "recTd": 8, "fum": 1 },

    # TEs
    { "name": "Trey McBride", "pos": "TE", "team": "ARI", "depth": "TE1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 0, "rushTd": 0, "rec": 109, "recYds": 1120, "recTd": 6, "fum": 1 },
    { "name": "Brock Bowers", "pos": "TE", "team": "LV", "depth": "TE1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 20, "rushTd": 0, "rec": 96, "recYds": 1080, "recTd": 8, "fum": 1 },
    { "name": "George Kittle", "pos": "TE", "team": "SF", "depth": "TE1", "passYds": 0, "passTd": 0, "int": 0, "rushYds": 0, "rushTd": 0, "rec": 75, "recYds: 940, "recTd": 7, "fum": 1 },

    # Ks
    { "name": "Brandon Aubrey", "pos": "K", "team": "DAL", "depth": "K1", "fgYds": 1450, "pat": 44 },
    { "name": "Harrison Butker", "pos": "K", "team": "KC", "depth": "K1", "fgYds": 1280, "pat": 46 },

    # DSTs
    { "name": "Baltimore Ravens DEF", "pos": "DEF", "team": "BAL", "depth": "DST", "pts": 128 },
    { "name": "San Francisco 49ers DEF", "pos": "DEF", "team": "SF", "depth": "DST", "pts": 124 }
]

def main():
    live_meta = fetch_live_depth_and_teams()
    
    # Update base players with real-time teams and depth positions if found
    for p in BASE_PLAYERS:
        key = p["name"].lower()
        if key in live_meta:
            if live_meta[key].get("team") and live_meta[key]["team"] != "FA":
                p["team"] = live_meta[key]["team"]
            if live_meta[key].get("depth"):
                p["depth"] = live_meta[key]["depth"]

    with open("projections.json", "w") as f:
        json.dump(BASE_PLAYERS, f, indent=2)
        
    print(f"Successfully generated projections.json with {len(BASE_PLAYERS)} players.")

if __name__ == "__main__":
    main()
