import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import plotly.express as px

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Tennis Global Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Database Connection
# ---------------------------------------------------------
DB_USER = "root"
DB_PASS = "PradiAtMysql24"  # <-- Enter your MySQL password here
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "tennis_analytics"

@st.cache_resource
def get_database_engine():
    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )
    return create_engine(connection_url)

engine = get_database_engine()

@st.cache_data(ttl=600)
def run_query(sql_query, params=None):
    with engine.connect() as conn:
        return pd.read_sql(text(sql_query), conn, params=params)

# ---------------------------------------------------------
# Sidebar Navigation
# ---------------------------------------------------------
st.sidebar.title("Tennis Analytics")
menu = st.sidebar.radio(
    "Navigate Modules",
    ["Executive Overview", "Competitions Explorer", "Venue Infrastructure", "Competitor Rankings", "SQL Query Sandbox"]
)

# ---------------------------------------------------------
# 1. Executive Overview
# ---------------------------------------------------------
if menu == "Executive Overview":
    st.title(" Tennis Ecosystem Global Overview")
    st.markdown("High-level KPI distribution across professional circuits, global venues, and active competitors.")

    # High-level KPIs
    col1, col2, col3, col4 = st.columns(4)
    total_comps = run_query("SELECT COUNT(*) AS val FROM Competitions")['val'][0]
    total_venues = run_query("SELECT COUNT(*) AS val FROM Venues")['val'][0]
    total_complexes = run_query("SELECT COUNT(*) AS val FROM Complexes")['val'][0]
    total_players = run_query("SELECT COUNT(*) AS val FROM Competitors")['val'][0]

    col1.metric("Total Competitions", f"{total_comps:,}")
    col2.metric("Total Venues", f"{total_venues:,}")
    col3.metric("Tennis Complexes", f"{total_complexes:,}")
    col4.metric("Ranked Competitors", f"{total_players:,}")

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Tournament Volume by Category")
        df_cat = run_query("""
            SELECT cat.category_name, COUNT(c.competition_id) AS total
            FROM Categories cat
            JOIN Competitions c ON cat.category_id = c.category_id
            GROUP BY cat.category_name
            ORDER BY total DESC
            LIMIT 10;
        """)
        fig_cat = px.bar(df_cat, x="total", y="category_name", orientation="h",
                         color="total", color_continuous_scale="Viridis",
                         labels={"total": "Competitions", "category_name": "Circuit Category"})
        fig_cat.update_layout(yaxis={'categoryorder': 'total ascending'}, showlegend=False)
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_right:
        st.subheader("Top 10 Host Countries by Venues")
        df_venues_ctry = run_query("""
            SELECT country_name, COUNT(venue_id) AS total_venues
            FROM Venues
            GROUP BY country_name
            ORDER BY total_venues DESC
            LIMIT 10;
        """)
        fig_venue = px.pie(df_venues_ctry, values="total_venues", names="country_name",
                           hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
        st.plotly_chart(fig_venue, use_container_width=True)

# ---------------------------------------------------------
# 2. Competitions Explorer
# ---------------------------------------------------------
elif menu == "Competitions Explorer":
    st.title("Competitions & Circuits Analysis")

    cat_list = run_query("SELECT DISTINCT category_name FROM Categories ORDER BY category_name;")['category_name'].tolist()
    selected_cat = st.selectbox("Filter by Category", ["All"] + cat_list)

    if selected_cat == "All":
        query_comp = """
            SELECT c.competition_id, c.competition_name, cat.category_name, c.type, c.gender
            FROM Competitions c
            LEFT JOIN Categories cat ON c.category_id = cat.category_id;
        """
        df_comp = run_query(query_comp)
    else:
        query_comp = """
            SELECT c.competition_id, c.competition_name, cat.category_name, c.type, c.gender
            FROM Competitions c
            JOIN Categories cat ON c.category_id = cat.category_id
            WHERE cat.category_name = :category;
        """
        df_comp = run_query(query_comp, params={"category": selected_cat})

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.metric("Tournaments Listed", f"{len(df_comp):,}")
        type_dist = df_comp['type'].value_counts().reset_index()
        type_dist.columns = ['Type', 'Count']
        fig_pie = px.pie(type_dist, names='Type', values='Count', title="Singles vs. Doubles Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.dataframe(df_comp, use_container_width=True, height=450)

# ---------------------------------------------------------
# 3. Venue Infrastructure
# ---------------------------------------------------------
elif menu == "Venue Infrastructure":
    st.title("Global Venue & Stadium Network")

    sub_tab1, sub_tab2 = st.tabs(["Complexes Breakdown", "Geographic Concentration"])

    with sub_tab1:
        st.subheader("Major Multi-Court Complexes")
        df_complex = run_query("""
            SELECT c.complex_name, COUNT(v.venue_id) AS venue_count
            FROM Complexes c
            JOIN Venues v ON c.complex_id = v.complex_id
            GROUP BY c.complex_name
            HAVING COUNT(v.venue_id) > 1
            ORDER BY venue_count DESC
            LIMIT 15;
        """)
        fig_comp = px.bar(df_complex, x="complex_name", y="venue_count",
                          labels={"complex_name": "Complex Name", "venue_count": "Court / Venue Count"},
                          color="venue_count", color_continuous_scale="Blues")
        st.plotly_chart(fig_comp, use_container_width=True)

    with sub_tab2:
        st.subheader("Venues by Country")
        df_ctry = run_query("""
            SELECT country_name, COUNT(venue_id) AS total_venues
            FROM Venues
            GROUP BY country_name
            ORDER BY total_venues DESC;
        """)
        st.dataframe(df_ctry, use_container_width=True, height=400)

# ---------------------------------------------------------
# 4. Competitor Rankings
# ---------------------------------------------------------
elif menu == "Competitor Rankings":
    st.title("Player Leaderboards & Points")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        top_n = st.slider("Select Top N Competitors", min_value=5, max_value=50, value=10)
    with col_f2:
        sort_metric = st.selectbox("Sort By", ["Points", "Rank"])

    order_clause = "r.points DESC" if sort_metric == "Points" else "r.`rank` ASC"

    df_rankings = run_query(f"""
        SELECT c.name, c.country, r.`rank`, r.movement, r.points, r.competitions_played
        FROM Competitor_Rankings r
        JOIN Competitors c ON r.competitor_id = c.competitor_id
        ORDER BY {order_clause}
        LIMIT :limit;
    """, params={"limit": top_n})

    fig_rank = px.bar(df_rankings, x="name", y="points", color="country",
                      title=f"Top {top_n} Competitors by Points",
                      labels={"name": "Player Name", "points": "ATP/WTA Points", "country": "Nation"})
    st.plotly_chart(fig_rank, use_container_width=True)

    st.dataframe(df_rankings, use_container_width=True)

# ---------------------------------------------------------
# 5. SQL Query Sandbox
# ---------------------------------------------------------
elif menu == "SQL Query Sandbox":
    st.title("Live SQL Query Executor")
    st.markdown("Execute verified queries against `tennis_analytics`.")

    default_query = "SELECT c.name, c.country, r.`rank`, r.points FROM Competitor_Rankings r JOIN Competitors c ON r.competitor_id = c.competitor_id ORDER BY r.points DESC LIMIT 10;"
    user_sql = st.text_area("Input SQL Query", value=default_query, height=120)

    if st.button("Execute Query"):
        try:
            res_df = run_query(user_sql)
            st.success(f"Query returned {len(res_df)} rows.")
            st.dataframe(res_df, use_container_width=True)
        except Exception as err:
            st.error(f"SQL Execution Error: {err}")