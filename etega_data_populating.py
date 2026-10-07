import json
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# --- 1. Database Connection Setup ---
# URL.create passes your custom password directly without parsing issues
connection_url = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="PradiAtMysql24",  # <-- Replace with your new custom password
    host="127.0.0.1",
    port=3306,
    database="tennis_analytics"
)

engine = create_engine(connection_url)

# --- 2. Test Connection ---
def test_connection():
    print("Connecting to MySQL database...")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT DATABASE();"))
            db_name = result.scalar()
            print(f"[SUCCESS] Connected to database: {db_name}\n")
            return True
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return False

# --- 3. Ingestion Functions ---
def load_competitions_data():
    if not os.path.exists("competitions.json"):
        print("[SKIP] competitions.json not found.")
        return

    print("Loading Competitions & Categories...")
    with open("competitions.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = []
    competitions = []

    for comp in data.get("competitions", []):
        cat = comp.get("category", {})
        cat_id = cat.get("id") if cat else None
        
        if cat_id:
            categories.append({
                "category_id": cat_id,
                "category_name": cat.get("name", "Unknown")
            })

        competitions.append({
            "competition_id": comp.get("id"),
            "competition_name": comp.get("name", "Unknown"),
            "parent_id": comp.get("parent_id"),
            "type": comp.get("type", "unknown"),
            "gender": comp.get("gender", "unknown"),
            "category_id": cat_id
        })

    df_cat = pd.DataFrame(categories).drop_duplicates(subset=["category_id"])
    df_comp = pd.DataFrame(competitions).drop_duplicates(subset=["competition_id"])

    df_cat.to_sql("Categories", con=engine, if_exists="append", index=False)
    df_comp.to_sql("Competitions", con=engine, if_exists="append", index=False)
    print(f" -> Inserted {len(df_cat)} categories and {len(df_comp)} competitions.")

def load_complexes_data():
    if not os.path.exists("complexes.json"):
        print("[SKIP] complexes.json not found.")
        return

    print("Loading Complexes & Venues...")
    with open("complexes.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    complexes = []
    venues = []

    for comp in data.get("complexes", []):
        c_id = comp.get("id")
        complexes.append({
            "complex_id": c_id,
            "complex_name": comp.get("name", "Unknown")
        })

        for v in comp.get("venues", []):
            venues.append({
                "venue_id": v.get("id"),
                "venue_name": v.get("name", "Unknown"),
                "city_name": v.get("city_name", "Unknown"),
                "country_name": v.get("country_name", "Unknown"),
                "country_code": (v.get("country_code") or "UNK")[:10],
                "timezone": v.get("timezone", "UTC"),
                "complex_id": c_id
            })

    df_complexes = pd.DataFrame(complexes).drop_duplicates(subset=["complex_id"])
    df_venues = pd.DataFrame(venues).drop_duplicates(subset=["venue_id"])

    df_complexes.to_sql("Complexes", con=engine, if_exists="append", index=False)
    df_venues.to_sql("Venues", con=engine, if_exists="append", index=False)
    print(f" -> Inserted {len(df_complexes)} complexes and {len(df_venues)} venues.")

def load_rankings_data():
    filename = "doubles_competitor_rankings.json"
    if not os.path.exists(filename):
        print(f"[SKIP] {filename} not found.")
        return

    print("Loading Competitors & Rankings...")
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    competitors = []
    rankings = []

    for group in data.get("rankings", []):
        for item in group.get("competitor_rankings", []):
            comp = item.get("competitor", {})
            c_id = comp.get("id")
            if not c_id:
                continue

            competitors.append({
                "competitor_id": c_id,
                "name": comp.get("name", "Unknown"),
                "country": comp.get("country", "Unknown"),
                "country_code": (comp.get("country_code") or "UNK")[:10],
                "abbreviation": (comp.get("abbreviation") or "UNK")[:20]
            })

            rankings.append({
                "rank": item.get("rank", 0),
                "movement": item.get("movement", 0),
                "points": item.get("points", 0),
                "competitions_played": item.get("competitions_played", 0),
                "competitor_id": c_id
            })

    df_competitors = pd.DataFrame(competitors).drop_duplicates(subset=["competitor_id"])
    df_rankings = pd.DataFrame(rankings)

    df_competitors.to_sql("Competitors", con=engine, if_exists="append", index=False)
    df_rankings.to_sql("Competitor_Rankings", con=engine, if_exists="append", index=False)
    print(f" -> Inserted {len(df_competitors)} competitors and {len(df_rankings)} rankings.")

if __name__ == "__main__":
    if test_connection():
        load_competitions_data()
        load_complexes_data()
        load_rankings_data()
        print("\nAll database tables populated successfully!")