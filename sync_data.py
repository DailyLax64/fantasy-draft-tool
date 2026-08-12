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

# Schema: (Name, Pos, Team, Depth, PassYds, PassTd, Int, RushYds, RushTd, Rec, RecYds, RecTd, Fum)
SKILL_PLAYERS = [
    # === 40 QUARTERBACKS ===
    ("Josh Allen", "QB", "BUF", "QB1", 3800, 28, 11, 540, 10, 0, 0, 0, 2),
    ("Lamar Jackson", "QB", "BAL", "QB1", 3500, 27, 8, 720, 5, 0, 0, 0, 2),
    ("Drake Maye", "QB", "NE", "QB1", 4050, 28, 10, 480, 4, 0, 0, 0, 2),
    ("Jayden Daniels", "QB", "WAS", "QB1", 3650, 23, 9, 650, 6, 0, 0, 0, 2),
    ("Jalen Hurts", "QB", "PHI", "QB1", 3600, 25, 10, 520, 9, 0, 0, 0, 2),
    ("Joe Burrow", "QB", "CIN", "QB1", 4300, 34, 10, 180, 2, 0, 0, 0, 2),
    ("Caleb Williams", "QB", "CHI", "QB1", 3850, 26, 10, 410, 3, 0, 0, 0, 2),
    ("Patrick Mahomes", "QB", "KC", "QB1", 4200, 30, 10, 320, 2, 0, 0, 0, 2),
    ("Bo Nix", "QB", "DEN", "QB1", 3750, 26, 11, 390, 4, 0, 0, 0, 2),
    ("Dak Prescott", "QB", "DAL", "QB1", 4150, 29, 11, 200, 2, 0, 0, 0, 2),
    ("Trevor Lawrence", "QB", "JAX", "QB1", 3850, 25, 12, 330, 4, 0, 0, 0, 3),
    ("Justin Herbert", "QB", "LAC", "QB1", 3850, 25, 9, 290, 3, 0, 0, 0, 2),
    ("Kyler Murray", "QB", "ARI", "QB1", 3600, 22, 10, 460, 4, 0, 0, 0, 2),
    ("Brock Purdy", "QB", "SF", "QB1", 3950, 27, 12, 210, 3, 0, 0, 0, 2),
    ("Jared Goff", "QB", "DET", "QB1", 4250, 30, 10, 40, 1, 0, 0, 0, 2),
    ("Jordan Love", "QB", "GB", "QB1", 3900, 27, 11, 160, 2, 0, 0, 0, 2),
    ("C.J. Stroud", "QB", "HOU", "QB1", 3950, 24, 9, 150, 1, 0, 0, 0, 2),
    ("Matthew Stafford", "QB", "LAR", "QB1", 4050, 30, 12, 30, 1, 0, 0, 0, 2),
    ("Sam Darnold", "QB", "MIN", "QB1", 3800, 25, 13, 140, 2, 0, 0, 0, 2),
    ("Baker Mayfield", "QB", "TB", "QB1", 3750, 25, 11, 170, 2, 0, 0, 0, 2),
    ("Jaxson Dart", "QB", "NYG", "QB1", 3400, 21, 11, 430, 5, 0, 0, 0, 2),
    ("Bryce Young", "QB", "CAR", "QB1", 3450, 21, 11, 230, 2, 0, 0, 0, 2),
    ("Geno Smith", "QB", "SEA", "QB1", 3600, 21, 11, 180, 1, 0, 0, 0, 2),
    ("Tua Tagovailoa", "QB", "MIA", "QB1", 3750, 24, 12, 50, 0, 0, 0, 0, 2),
    ("Aaron Rodgers", "QB", "NYJ", "QB1", 3450, 22, 9, 40, 0, 0, 0, 0, 2),
    ("Cam Ward", "QB", "TEN", "QB1", 3350, 20, 12, 260, 3, 0, 0, 0, 3),
    ("Kirk Cousins", "QB", "ATL", "QB1", 3400, 21, 11, 30, 0, 0, 0, 0, 2),
    ("Daniel Jones", "QB", "IND", "QB1", 3150, 17, 10, 320, 2, 0, 0, 0, 3),
    ("Deshaun Watson", "QB", "CLE", "QB1", 3200, 18, 10, 270, 2, 0, 0, 0, 3),
    ("Tyler Shough", "QB", "LV", "QB1", 3100, 18, 10, 210, 2, 0, 0, 0, 2),
    ("Will Levis", "QB", "TEN", "QB2", 3100, 17, 12, 220, 2, 0, 0, 0, 3),
    ("Shedeur Sanders", "QB", "NO", "QB1", 3200, 19, 11, 150, 2, 0, 0, 0, 2),
    ("Michael Penix Jr.", "QB", "ATL", "QB2", 3250, 19, 10, 80, 1, 0, 0, 0, 2),
    ("J.J. McCarthy", "QB", "MIN", "QB2", 3300, 20, 11, 190, 2, 0, 0, 0, 2),
    ("Derek Carr", "QB", "NO", "QB2", 3300, 19, 10, 50, 0, 0, 0, 0, 2),
    ("Russell Wilson", "QB", "PIT", "QB1", 3000, 17, 9, 160, 1, 0, 0, 0, 2),
    ("Jacoby Brissett", "QB", "NE", "QB2", 2800, 15, 8, 120, 1, 0, 0, 0, 1),
    ("Gardner Minshew", "QB", "LV", "QB2", 2900, 15, 10, 100, 1, 0, 0, 0, 2),
    ("Aidan O'Connell", "QB", "LV", "QB3", 2850, 14, 9, 40, 0, 0, 0, 0, 2),
    ("Drew Lock", "QB", "NYG", "QB2", 2700, 14, 10, 90, 1, 0, 0, 0, 2),

    # === 76 RUNNING BACKS ===
    ("Jahmyr Gibbs", "RB", "DET", "RB1", 0, 0, 0, 1480, 14, 73, 650, 6, 2),
    ("Bijan Robinson", "RB", "ATL", "RB1", 0, 0, 0, 1630, 12, 74, 650, 5, 2),
    ("James Cook III", "RB", "BUF", "RB1", 0, 0, 0, 1560, 12, 32, 280, 4, 1),
    ("Saquon Barkley", "RB", "PHI", "RB1", 0, 0, 0, 1460, 13, 30, 260, 3, 2),
    ("Jonathan Taylor", "RB", "IND", "RB1", 0, 0, 0, 1370, 13, 38, 290, 2, 2),
    ("Omarion Hampton", "RB", "DAL", "RB1", 0, 0, 0, 1240, 10, 62, 440, 3, 2),
    ("Kenneth Walker III", "RB", "SEA", "RB1", 0, 0, 0, 1290, 11, 44, 350, 2, 2),
    ("Ashton Jeanty", "RB", "LV", "RB1", 0, 0, 0, 1230, 9, 65, 520, 2, 2),
    ("Quinshon Judkins", "RB", "CLE", "RB1", 0, 0, 0, 860, 7, 28, 210, 1, 1),
    ("De'Von Achane", "RB", "MIA", "RB1", 0, 0, 0, 1150, 8, 65, 490, 3, 1),
    ("Chase Brown", "RB", "CIN", "RB1", 0, 0, 0, 1060, 9, 67, 460, 3, 2),
    ("Derrick Henry", "RB", "BAL", "RB1", 0, 0, 0, 1420, 12, 20, 160, 0, 2),
    ("Josh Jacobs", "RB", "GB", "RB1", 0, 0, 0, 1120, 10, 35, 280, 1, 2),
    ("Breece Hall", "RB", "NYJ", "RB1", 0, 0, 0, 1100, 8, 60, 500, 3, 2),
    ("Christian McCaffrey", "RB", "SF", "RB1", 0, 0, 0, 1050, 9, 70, 580, 4, 2),
    ("Kyren Williams", "RB", "LAR", "RB1", 0, 0, 0, 1040, 10, 36, 270, 1, 2),
    ("Travis Etienne Jr.", "RB", "JAX", "RB1", 0, 0, 0, 980, 7, 48, 380, 2, 2),
    ("Isiah Pacheco", "RB", "KC", "RB1", 0, 0, 0, 950, 8, 38, 260, 1, 2),
    ("David Montgomery", "RB", "DET", "RB2", 0, 0, 0, 880, 8, 28, 210, 1, 1),
    ("Rachaad White", "RB", "TB", "RB1", 0, 0, 0, 820, 6, 55, 420, 2, 1),
    ("Alvin Kamara", "RB", "NO", "RB1", 0, 0, 0, 780, 5, 68, 490, 3, 2),
    ("Tony Pollard", "RB", "TEN", "RB1", 0, 0, 0, 890, 6, 42, 310, 1, 1),
    ("Brian Robinson Jr.", "RB", "WAS", "RB1", 0, 0, 0, 850, 7, 25, 190, 1, 1),
    ("Jonathon Brooks", "RB", "CAR", "RB1", 0, 0, 0, 860, 6, 35, 270, 2, 1),
    ("Trey Benson", "RB", "ARI", "RB1", 0, 0, 0, 790, 6, 30, 240, 1, 1),
    ("Chuba Hubbard", "RB", "CAR", "RB2", 0, 0, 0, 810, 5, 32, 220, 1, 1),
    ("Javonte Williams", "RB", "DEN", "RB1", 0, 0, 0, 760, 5, 42, 290, 1, 2),
    ("Jerome Ford", "RB", "CLE", "RB2", 0, 0, 0, 680, 4, 38, 260, 2, 1),
    ("Ty Chandler", "RB", "MIN", "RB2", 0, 0, 0, 640, 4, 30, 210, 1, 1),
    ("Nick Chubb", "RB", "CLE", "RB3", 0, 0, 0, 720, 5, 15, 100, 0, 1),
    ("Jaylen Warren", "RB", "PIT", "RB2", 0, 0, 0, 690, 4, 45, 320, 1, 1),
    ("Raheem Mostert", "RB", "MIA", "RB2", 0, 0, 0, 580, 5, 22, 170, 1, 2),
    ("Zach Charbonnet", "RB", "SEA", "RB2", 0, 0, 0, 550, 4, 32, 220, 1, 1),
    ("Rico Dowdle", "RB", "DAL", "RB2", 0, 0, 0, 610, 4, 28, 200, 1, 1),
    ("Roschon Johnson", "RB", "CHI", "RB2", 0, 0, 0, 510, 5, 26, 180, 1, 1),
    ("Blake Corum", "RB", "LAR", "RB2", 0, 0, 0, 530, 5, 18, 130, 0, 1),
    ("MarShawn Lloyd", "RB", "GB", "RB2", 0, 0, 0, 490, 3, 22, 170, 1, 2),
    ("Ray Davis", "RB", "BUF", "RB2", 0, 0, 0, 460, 4, 20, 150, 1, 1),
    ("Isaac Guerendo", "RB", "SF", "RB2", 0, 0, 0, 440, 3, 21, 160, 1, 1),
    ("Audric Estime", "RB", "DEN", "RB2", 0, 0, 0, 420, 3, 12, 90, 0, 1),
    ("Kenneth Gainwell", "RB", "PHI", "RB2", 0, 0, 0, 450, 3, 35, 260, 1, 1),
    ("Bucky Irving", "RB", "TB", "RB2", 0, 0, 0, 780, 5, 40, 310, 2, 1),
    ("Tyrone Tracy Jr.", "RB", "NYG", "RB1", 0, 0, 0, 720, 4, 38, 280, 2, 1),
    ("Tank Bigsby", "RB", "JAX", "RB2", 0, 0, 0, 690, 5, 15, 110, 0, 1),
    ("Tyler Allgeier", "RB", "ATL", "RB2", 0, 0, 0, 620, 4, 18, 140, 0, 1),
    ("Braelon Allen", "RB", "NYJ", "RB2", 0, 0, 0, 560, 4, 20, 150, 1, 1),
    ("Jordan Mason", "RB", "SF", "RB3", 0, 0, 0, 580, 4, 16, 120, 0, 1),
    ("Kimani Vidal", "RB", "LAC", "RB2", 0, 0, 0, 480, 3, 22, 160, 1, 1),
    ("Jaleel McLaughlin", "RB", "DEN", "RB3", 0, 0, 0, 410, 2, 34, 230, 1, 1),
    ("Antonio Gibson", "RB", "NE", "RB2", 0, 0, 0, 420, 2, 30, 220, 1, 1),
    ("Zamir White", "RB", "LV", "RB2", 0, 0, 0, 490, 3, 14, 90, 0, 1),
    ("Alexander Mattison", "RB", "LV", "RB3", 0, 0, 0, 440, 3, 24, 170, 1, 1),
    ("Gus Edwards", "RB", "LAC", "RB3", 0, 0, 0, 430, 4, 8, 50, 0, 1),
    ("Keaton Mitchell", "RB", "BAL", "RB2", 0, 0, 0, 390, 2, 18, 150, 1, 1),
    ("Dameon Pierce", "RB", "HOU", "RB2", 0, 0, 0, 380, 2, 12, 80, 0, 1),
    ("Miles Sanders", "RB", "CAR", "RB3", 0, 0, 0, 360, 2, 20, 130, 0, 1),
    ("Elijah Mitchell", "RB", "SF", "RB4", 0, 0, 0, 350, 2, 10, 70, 0, 1),
    ("Kareem Hunt", "RB", "KC", "RB2", 0, 0, 0, 390, 3, 15, 100, 0, 1),
    ("Cam Akers", "RB", "MIN", "RB3", 0, 0, 0, 370, 2, 14, 90, 0, 1),
    ("Khalil Herbert", "RB", "CIN", "RB2", 0, 0, 0, 380, 2, 15, 110, 0, 1),
    ("D'Onta Foreman", "RB", "CLE", "RB4", 0, 0, 0, 360, 3, 8, 50, 0, 1),
    ("Samaje Perine", "RB", "KC", "RB3", 0, 0, 0, 250, 1, 35, 260, 1, 1),
    ("Cordarrelle Patterson", "RB", "PIT", "RB3", 0, 0, 0, 280, 2, 18, 140, 0, 1),
    ("Justice Hill", "RB", "BAL", "RB3", 0, 0, 0, 290, 1, 30, 220, 1, 1),
    ("Clyde Edwards-Helaire", "RB", "KC", "RB4", 0, 0, 0, 260, 1, 18, 120, 0, 1),
    ("AJ Dillon", "RB", "GB", "RB3", 0, 0, 0, 340, 2, 14, 90, 0, 1),
    ("Jeff Wilson Jr.", "RB", "MIA", "RB3", 0, 0, 0, 270, 1, 12, 80, 0, 1),
    ("Jamaal Williams", "RB", "NO", "RB2", 0, 0, 0, 280, 2, 12, 70, 0, 1),
    ("Boston Scott", "RB", "LAR", "RB3", 0, 0, 0, 230, 1, 15, 100, 0, 1),
    ("Chase Edmonds", "RB", "TB", "RB3", 0, 0, 0, 220, 1, 20, 140, 0, 1),
    ("Craig Reynolds", "RB", "DET", "RB3", 0, 0, 0, 210, 1, 10, 70, 0, 0),
    ("Michael Carter", "RB", "ARI", "RB2", 0, 0, 0, 230, 1, 22, 150, 0, 1),
    ("Deon Jackson", "RB", "NYG", "RB3", 0, 0, 0, 200, 1, 15, 90, 0, 0),
    ("Patrick Taylor", "RB", "SF", "RB5", 0, 0, 0, 190, 1, 8, 50, 0, 0),
    ("Trayveon Williams", "RB", "CIN", "RB3", 0, 0, 0, 180, 1, 10, 60, 0, 0),
    ("Sean Tucker", "RB", "TB", "RB4", 0, 0, 0, 210, 1, 12, 80, 0, 0),

    # === 100 WIDE RECEIVERS ===
    ("Jaxon Smith-Njigba", "WR", "SEA", "WR1", 0, 0, 0, 30, 0, 111, 1568, 9, 1),
    ("Puka Nacua", "WR", "LAR", "WR1", 0, 0, 0, 106, 1, 123, 1590, 10, 1),
    ("Ja'Marr Chase", "WR", "CIN", "WR1", 0, 0, 0, 40, 0, 121, 1512, 11, 1),
    ("Amon-Ra St. Brown", "WR", "DET", "WR1", 0, 0, 0, 25, 0, 117, 1391, 10, 1),
    ("Drake London", "WR", "ATL", "WR1", 0, 0, 0, 0, 0, 102, 1328, 9, 1),
    ("Justin Jefferson", "WR", "MIN", "WR1", 0, 0, 0, 15, 0, 99, 1302, 8, 1),
    ("CeeDee Lamb", "WR", "DAL", "WR1", 0, 0, 0, 60, 1, 97, 1296, 8, 1),
    ("A.J. Brown", "WR", "PHI", "WR1", 0, 0, 0, 0, 0, 92, 1234, 8, 1),
    ("Nico Collins", "WR", "HOU", "WR1", 0, 0, 0, 0, 0, 88, 1212, 8, 1),
    ("Rashee Rice", "WR", "KC", "WR1", 0, 0, 0, 20, 0, 99, 1180, 10, 1),
    ("Tee Higgins", "WR", "CIN", "WR2", 0, 0, 0, 0, 0, 85, 1120, 9, 1),
    ("Malik Nabers", "WR", "NYG", "WR1", 0, 0, 0, 35, 0, 94, 1220, 7, 1),
    ("Marvin Harrison Jr.", "WR", "ARI", "WR1", 0, 0, 0, 10, 0, 88, 1190, 8, 1),
    ("Garrett Wilson", "WR", "NYJ", "WR1", 0, 0, 0, 15, 0, 95, 1160, 7, 1),
    ("Jaylen Waddle", "WR", "MIA", "WR2", 0, 0, 0, 25, 0, 82, 1100, 6, 1),
    ("DeVonta Smith", "WR", "PHI", "WR2", 0, 0, 0, 10, 0, 84, 1080, 7, 1),
    ("Cooper Kupp", "WR", "LAR", "WR2", 0, 0, 0, 15, 0, 89, 1050, 7, 1),
    ("DK Metcalf", "WR", "SEA", "WR2", 0, 0, 0, 0, 0, 72, 1040, 8, 1),
    ("Brandon Aiyuk", "WR", "SF", "WR1", 0, 0, 0, 15, 0, 75, 1060, 6, 1),
    ("Deebo Samuel", "WR", "SF", "WR2", 0, 0, 0, 180, 3, 65, 880, 5, 2),
    ("Chris Olave", "WR", "NO", "WR1", 0, 0, 0, 0, 0, 84, 1020, 5, 1),
    ("Mike Evans", "WR", "TB", "WR1", 0, 0, 0, 0, 0, 68, 990, 9, 1),
    ("Terry McLaurin", "WR", "WAS", "WR1", 0, 0, 0, 0, 0, 78, 980, 6, 1),
    ("DJ Moore", "WR", "CHI", "WR1", 0, 0, 0, 30, 0, 80, 970, 6, 1),
    ("Zay Flowers", "WR", "BAL", "WR1", 0, 0, 0, 45, 1, 82, 950, 5, 1),
    ("George Pickens", "WR", "PIT", "WR1", 0, 0, 0, 0, 0, 65, 960, 6, 1),
    ("Amari Cooper", "WR", "BUF", "WR1", 0, 0, 0, 0, 0, 68, 920, 5, 1),
    ("Christian Kirk", "WR", "JAX", "WR2", 0, 0, 0, 10, 0, 74, 890, 5, 1),
    ("Xavier Worthy", "WR", "KC", "WR2", 0, 0, 0, 60, 1, 62, 870, 6, 1),
    ("Ladd McConkey", "WR", "LAC", "WR1", 0, 0, 0, 20, 0, 76, 880, 5, 1),
    ("Brian Thomas Jr.", "WR", "JAX", "WR1", 0, 0, 0, 15, 0, 64, 890, 6, 1),
    ("Keon Coleman", "WR", "BUF", "WR2", 0, 0, 0, 0, 0, 58, 830, 6, 1),
    ("Rome Odunze", "WR", "CHI", "WR2", 0, 0, 0, 0, 0, 60, 820, 5, 1),
    ("Stefon Diggs", "WR", "HOU", "WR2", 0, 0, 0, 0, 0, 72, 810, 5, 1),
    ("Jayden Reed", "WR", "GB", "WR1", 0, 0, 0, 80, 1, 62, 790, 6, 1),
    ("Jordan Addison", "WR", "MIN", "WR2", 0, 0, 0, 0, 0, 58, 780, 6, 1),
    ("Jauan Jennings", "WR", "SF", "WR3", 0, 0, 0, 0, 0, 64, 770, 5, 1),
    ("Josh Downs", "WR", "IND", "WR2", 0, 0, 0, 0, 0, 68, 760, 4, 1),
    ("Rashid Shaheed", "WR", "NO", "WR2", 0, 0, 0, 40, 0, 52, 780, 5, 1),
    ("Jameson Williams", "WR", "DET", "WR2", 0, 0, 0, 50, 1, 50, 760, 5, 1),
    ("Wan'Dale Robinson", "WR", "NYG", "WR2", 0, 0, 0, 20, 0, 70, 710, 4, 1),
    ("Khalil Shakir", "WR", "BUF", "WR3", 0, 0, 0, 15, 0, 62, 720, 4, 1),
    ("Jerry Jeudy", "WR", "CLE", "WR1", 0, 0, 0, 0, 0, 56, 710, 4, 1),
    ("Dontayvion Wicks", "WR", "GB", "WR3", 0, 0, 0, 0, 0, 50, 680, 5, 1),
    ("Christian Watson", "WR", "GB", "WR2", 0, 0, 0, 20, 0, 44, 660, 5, 1),
    ("Courtland Sutton", "WR", "DEN", "WR1", 0, 0, 0, 0, 0, 62, 780, 5, 1),
    ("Calvin Ridley", "WR", "TEN", "WR1", 0, 0, 0, 20, 0, 60, 810, 4, 1),
    ("Jakobi Meyers", "WR", "LV", "WR1", 0, 0, 0, 0, 0, 68, 740, 4, 1),
    ("Keenan Allen", "WR", "CHI", "WR3", 0, 0, 0, 0, 0, 65, 680, 4, 1),
    ("Tyler Lockett", "WR", "SEA", "WR3", 0, 0, 0, 0, 0, 55, 670, 4, 1),
    ("DeAndre Hopkins", "WR", "KC", "WR3", 0, 0, 0, 0, 0, 56, 700, 4, 1),
    ("Michael Pittman Jr.", "WR", "IND", "WR1", 0, 0, 0, 0, 0, 75, 820, 4, 1),
    ("Diontae Johnson", "WR", "BAL", "WR2", 0, 0, 0, 0, 0, 68, 750, 4, 1),
    ("Hollywood Brown", "WR", "KC", "WR4", 0, 0, 0, 10, 0, 58, 720, 4, 1),
    ("Gabe Davis", "WR", "JAX", "WR3", 0, 0, 0, 0, 0, 42, 650, 5, 1),
    ("Curtis Samuel", "WR", "BUF", "WR4", 0, 0, 0, 60, 1, 48, 520, 3, 1),
    ("Demarcus Robinson", "WR", "LAR", "WR3", 0, 0, 0, 0, 0, 46, 560, 4, 1),
    ("Adonai Mitchell", "WR", "IND", "WR3", 0, 0, 0, 10, 0, 45, 610, 4, 1),
    ("Ricky Pearsall", "WR", "SF", "WR4", 0, 0, 0, 15, 0, 48, 620, 3, 1),
    ("Ja'Lynn Polk", "WR", "NE", "WR1", 0, 0, 0, 0, 0, 44, 570, 3, 1),
    ("Malachi Corley", "WR", "NYJ", "WR3", 0, 0, 0, 40, 0, 42, 490, 3, 1),
    ("Jermaine Burton", "WR", "CIN", "WR3", 0, 0, 0, 0, 0, 38, 550, 3, 1),
    ("Troy Franklin", "WR", "DEN", "WR2", 0, 0, 0, 0, 0, 40, 520, 3, 1),
    ("Darnell Mooney", "WR", "ATL", "WR2", 0, 0, 0, 10, 0, 48, 610, 3, 1),
    ("Rashod Bateman", "WR", "BAL", "WR3", 0, 0, 0, 0, 0, 46, 580, 3, 1),
    ("Demario Douglas", "WR", "NE", "WR2", 0, 0, 0, 20, 0, 55, 590, 2, 1),
    ("Josh Palmer", "WR", "LAC", "WR2", 0, 0, 0, 0, 0, 42, 560, 3, 1),
    ("Quentin Johnston", "WR", "LAC", "WR3", 0, 0, 0, 0, 0, 44, 540, 3, 1),
    ("Adam Thielen", "WR", "CAR", "WR1", 0, 0, 0, 0, 0, 54, 550, 3, 1),
    ("Brandin Cooks", "WR", "DAL", "WR2", 0, 0, 0, 0, 0, 42, 510, 3, 1),
    ("Tre Tucker", "WR", "LV", "WR2", 0, 0, 0, 25, 0, 40, 490, 2, 1),
    ("Jalen Tolbert", "WR", "DAL", "WR3", 0, 0, 0, 0, 0, 42, 510, 3, 1),
    ("Kendrick Bourne", "WR", "NE", "WR3", 0, 0, 0, 0, 0, 40, 480, 3, 1),
    ("K.J. Osborn", "WR", "NE", "WR4", 0, 0, 0, 0, 0, 38, 450, 2, 1),
    ("Noah Brown", "WR", "WAS", "WR2", 0, 0, 0, 0, 0, 36, 470, 2, 1),
    ("Greg Dortch", "WR", "ARI", "WR2", 0, 0, 0, 15, 0, 46, 440, 2, 1),
    ("Marquez Valdes-Scantling", "WR", "NO", "WR3", 0, 0, 0, 0, 0, 26, 460, 3, 0),
    ("Tutu Atwell", "WR", "LAR", "WR4", 0, 0, 0, 20, 0, 34, 450, 2, 0),
    ("Elijah Moore", "WR", "CLE", "WR2", 0, 0, 0, 10, 0, 44, 440, 2, 1),
    ("Michael Wilson", "WR", "ARI", "WR3", 0, 0, 0, 0, 0, 38, 480, 3, 1),
    ("Alec Pierce", "WR", "IND", "WR4", 0, 0, 0, 0, 0, 32, 510, 3, 0),
    ("Ray-Ray McCloud", "WR", "ATL", "WR3", 0, 0, 0, 30, 0, 38, 410, 1, 1),
    ("Dyami Brown", "WR", "WAS", "WR3", 0, 0, 0, 0, 0, 30, 420, 2, 0),
    ("Cedric Tillman", "WR", "CLE", "WR3", 0, 0, 0, 0, 0, 36, 430, 2, 1),
    ("Andrei Iosivas", "WR", "CIN", "WR4", 0, 0, 0, 0, 0, 34, 410, 3, 0),
    ("Jalen McMillan", "WR", "TB", "WR2", 0, 0, 0, 10, 0, 36, 430, 3, 1),
    ("Jordan Whittington", "WR", "LAR", "WR5", 0, 0, 0, 0, 0, 35, 400, 2, 0),
    ("Devaughn Vele", "WR", "DEN", "WR3", 0, 0, 0, 0, 0, 36, 390, 2, 0),
    ("Kayshon Boutte", "WR", "NE", "WR5", 0, 0, 0, 0, 0, 30, 380, 2, 0),
    ("Luke McCaffrey", "WR", "WAS", "WR4", 0, 0, 0, 15, 0, 34, 370, 2, 1),
    ("Bo Melton", "WR", "GB", "WR4", 0, 0, 0, 15, 0, 28, 360, 2, 0),
    ("Olamide Zaccheaus", "WR", "WAS", "WR5", 0, 0, 0, 10, 0, 30, 350, 2, 0),
    ("KaVontae Turpin", "WR", "DAL", "WR4", 0, 0, 0, 60, 1, 26, 320, 2, 1),
    ("Kalif Raymond", "WR", "DET", "WR3", 0, 0, 0, 20, 0, 28, 340, 2, 0),
    ("Mack Hollins", "WR", "BUF", "WR5", 0, 0, 0, 0, 0, 26, 330, 2, 0),
    ("Nelson Agholor", "WR", "BAL", "WR4", 0, 0, 0, 0, 0, 25, 320, 2, 0),
    ("Van Jefferson", "WR", "PIT", "WR2", 0, 0, 0, 0, 0, 26, 310, 2, 0),
    ("Sterling Shepard", "WR", "TB", "WR3", 0, 0, 0, 0, 0, 30, 290, 1, 0),
    ("Lil'Jordan Humphrey", "WR", "DEN", "WR4", 0, 0, 0, 0, 0, 24, 280, 2, 0),
    ("David Moore", "WR", "CAR", "WR2", 0, 0, 0, 0, 0, 22, 270, 1, 0),

    # === 20 TIGHT ENDS ===
    ("Trey McBride", "TE", "ARI", "TE1", 0, 0, 0, 0, 0, 109, 1120, 6, 1),
    ("Brock Bowers", "TE", "LV", "TE1", 0, 0, 0, 20, 0, 96, 1080, 8, 1),
    ("George Kittle", "TE", "SF", "TE1", 0, 0, 0, 0, 0, 75, 940, 7, 1),
    ("Travis Kelce", "TE", "KC", "TE1", 0, 0, 0, 0, 0, 82, 890, 6, 1),
    ("Sam LaPorta", "TE", "DET", "TE1", 0, 0, 0, 0, 0, 78, 860, 7, 1),
    ("Dallas Goedert", "TE", "PHI", "TE1", 0, 0, 0, 0, 0, 72, 790, 8, 1),
    ("Mark Andrews", "TE", "BAL", "TE1", 0, 0, 0, 0, 0, 68, 780, 7, 1),
    ("David Njoku", "TE", "CLE", "TE1", 0, 0, 0, 0, 0, 70, 750, 6, 1),
    ("Jake Ferguson", "TE", "DAL", "TE1", 0, 0, 0, 0, 0, 72, 730, 5, 1),
    ("Evan Engram", "TE", "JAX", "TE1", 0, 0, 0, 0, 0, 75, 710, 4, 1),
    ("Dalton Kincaid", "TE", "BUF", "TE1", 0, 0, 0, 0, 0, 65, 700, 5, 1),
    ("Kyle Pitts", "TE", "ATL", "TE1", 0, 0, 0, 0, 0, 58, 720, 4, 1),
    ("Cole Kmet", "TE", "CHI", "TE1", 0, 0, 0, 0, 0, 60, 620, 5, 1),
    ("T.J. Hockenson", "TE", "MIN", "TE1", 0, 0, 0, 0, 0, 62, 640, 4, 1),
    ("Dalton Schultz", "TE", "HOU", "TE1", 0, 0, 0, 0, 0, 55, 580, 4, 1),
    ("Cade Otton", "TE", "TB", "TE1", 0, 0, 0, 0, 0, 52, 530, 4, 1),
    ("Hunter Henry", "TE", "NE", "TE1", 0, 0, 0, 0, 0, 48, 510, 4, 1),
    ("Ben Sinnott", "TE", "WAS", "TE1", 0, 0, 0, 0, 0, 42, 470, 4, 1),
    ("Isaiah Likely", "TE", "BAL", "TE2", 0, 0, 0, 0, 0, 42, 480, 5, 1),
    ("Tyler Conklin", "TE", "NYJ", "TE1", 0, 0, 0, 0, 0, 48, 460, 2, 1)
]

# Schema: (Name, Pos, Team, Depth, FgYds, Pat)
KICKERS = [
    ("Brandon Aubrey", "K", "DAL", "K1", 1450, 44),
    ("Harrison Butker", "K", "KC", "K1", 1280, 46),
    ("Justin Tucker", "K", "BAL", "K1", 1320, 42),
    ("Jake Moody", "K", "SF", "K1", 1240, 48),
    ("Jake Elliott", "K", "PHI", "K1", 1210, 45),
    ("Ka'imi Fairbairn", "K", "HOU", "K1", 1310, 38),
    ("Cameron Dicker", "K", "LAC", "K1", 1250, 39),
    ("Tyler Bass", "K", "BUF", "K1", 1180, 47),
    ("Evan McPherson", "K", "CIN", "K1", 1220, 40),
    ("Jason Sanders", "K", "MIA", "K1", 1190, 42),
    ("Chris Boswell", "K", "PIT", "K1", 1290, 32),
    ("Younghoe Koo", "K", "ATL", "K1", 1200, 36),
    ("Matt Gay", "K", "IND", "K1", 1160, 37),
    ("Chase McLaughlin", "K", "TB", "K1", 1180, 35),
    ("Cairo Santos", "K", "CHI", "K1", 1140, 34),
    ("Jason Myers", "K", "SEA", "K1", 1120, 36),
    ("Daniel Carlson", "K", "LV", "K1", 1110, 32),
    ("Will Reichard", "K", "MIN", "K1", 1130, 35),
    ("Blake Grupe", "K", "NO", "K1", 1090, 34),
    ("Dustin Hopkins", "K", "CLE", "K1", 1080, 31)
]

# Schema: (Name, Pos, Team, Depth, Pts)
DEFENSES = [
    ("Baltimore Ravens DEF", "DEF", "BAL", "DST", 128),
    ("San Francisco 49ers DEF", "DEF", "SF", "DST", 124),
    ("New York Jets DEF", "DEF", "NYJ", "DST", 122),
    ("Pittsburgh Steelers DEF", "DEF", "PIT", "DST", 121),
    ("Cleveland Browns DEF", "DEF", "CLE", "DST", 118),
    ("Kansas City Chiefs DEF", "DEF", "KC", "DST", 117),
    ("Dallas Cowboys DEF", "DEF", "DAL", "DST", 115),
    ("Buffalo Bills DEF", "DEF", "BUF", "DST", 114),
    ("Philadelphia Eagles DEF", "DEF", "PHI", "DST", 112),
    ("Houston Texans DEF", "DEF", "HOU", "DST", 110),
    ("Detroit Lions DEF", "DEF", "DET", "DST", 108),
    ("Minnesota Vikings DEF", "DEF", "MIN", "DST", 106),
    ("Denver Broncos DEF", "DEF", "DEN", "DST", 104),
    ("Chicago Bears DEF", "DEF", "CHI", "DST", 102),
    ("Miami Dolphins DEF", "DEF", "MIA", "DST", 100),
    ("Green Bay Packers DEF", "DEF", "GB", "DST", 99),
    ("Los Angeles Chargers DEF", "DEF", "LAC", "DST", 98),
    ("Seattle Seahawks DEF", "DEF", "SEA", "DST", 96),
    ("Indianapolis Colts DEF", "DEF", "IND", "DST", 94),
    ("Tampa Bay Buccaneers DEF", "DEF", "TB", "DST", 92)
]

def build_player_objects():
    res = []
    for p in SKILL_PLAYERS:
        res.append({
            "name": p[0], "pos": p[1], "team": p[2], "depth": p[3],
            "passYds": p[4], "passTd": p[5], "int": p[6],
            "rushYds": p[7], "rushTd": p[8],
            "rec": p[9], "recYds": p[10], "recTd": p[11],
            "fum": p[12]
        })
    for p in KICKERS:
        res.append({
            "name": p[0], "pos": p[1], "team": p[2], "depth": p[3],
            "fgYds": p[4], "pat": p[5]
        })
    for p in DEFENSES:
        res.append({
            "name": p[0], "pos": p[1], "team": p[2], "depth": p[3],
            "pts": p[4]
        })
    return res

def main():
    live_meta = fetch_live_depth_and_teams()
    players = build_player_objects()
    
    # Update player metadata with live Sleeper API values if found
    for p in players:
        key = p["name"].lower()
        if key in live_meta:
            if live_meta[key].get("team") and live_meta[key]["team"] != "FA":
                p["team"] = live_meta[key]["team"]
            if live_meta[key].get("depth"):
                p["depth"] = live_meta[key]["depth"]

    with open("projections.json", "w") as f:
        json.dump(players, f, indent=2)
        
    print(f"Successfully generated projections.json with {len(players)} players.")

if __name__ == "__main__":
    main()
