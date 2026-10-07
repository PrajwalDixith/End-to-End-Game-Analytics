End-to-End-Game-Analytics

Problem Statement: 
The SportRadar Event Explorer project aims to develop a comprehensive solution 
for managing, visualizing, and analyzing sports competition data extracted from the 
Sportradar API. The application will parse JSON data, store structured information in a 
relational database, and provide intuitive insights into tournaments, competition 
hierarchies, and event details. This project is designed to assist sports enthusiasts, 
analysts, and organizations in understanding competition structures and trends while 
exploring detailed event-specific information interactively. 

Business Use Cases: 
1.  Event Exploration: Enable users to navigate through competition hierarchies 
(e.g., ATP Vienna events). 

2. Trend Analysis: Visualize the distribution of events by type, gender, and 
competition level. 

3. Performance Insights: Analyze player participation across singles and 
doubles events. 

4. Decision Support: Offer data-driven insights to event organizers or sports 
bodies for resource allocation.

Data Analysis: 
Execute the Following SQL queries; 
1) List all competitions along with their category name 
2) Count the number of competitions in each category 
Links to the 
category table 
3) Find all competitions of type 'doubles' 
4) Get competitions that belong to a specific category (e.g., ITF Men) 
5) Identify parent competitions and their sub-competitions 
6) Analyze the distribution of competition types by category 
7) List all competitions with no parent (top-level competitions)

Execute the following SQL queries: 
1) List all venues along with their associated complex name 
2) Count the number of venues in each complex 
3) Get details of venues in a specific country (e.g., Chile) 
4) Identify all venues and their timezones 
5) Find complexes that have more than one venue 
6) List venues grouped by country 
7) Find all venues for a specific complex (e.g., Nacional)

Execute the following SQL queries: 
 
1) Get all competitors with their rank and points. 
2) Find competitors ranked in the top 5 
3) List competitors with no rank movement (stable rank) 
4) Get the total points of competitors from a specific country (e.g., Croatia) 
5) Count the number of competitors per country 
6) Find competitors with the highest points in the current week

Build a Streamlit Application: 
● Connect the Streamlit app with the SQL database for real-time query execution. 
● Display analysis results in the form of tables, charts, or dashboards within the 
app.User Interface: Interactive dashboards with filters for competition types, 
levels, and categories. 
Suggested Features for the Application (Use your creativity) 
1. Homepage Dashboard: 
   ○ Summary statistics like: 
      ■ Total number of competitors. 
      ■ Number of countries represented. 
      ■ Highest points scored by a competitor. 

2. Search and Filter Competitors: 
   ○ Allow users to search for a competitor by name. 
   ○ Filter competitors by rank range, country, or points threshold. 

3. Competitor Details Viewer: 
   ○ Display detailed information about a selected competitor, including: 
     ■ Rank, movement, competitions played, and country. 

4. Country-Wise Analysis: 
   ○ List countries with the total number of competitors and their average 
points. 

5. Leaderboards: 
   ○ Show tables for: 
     ■ Top-ranked competitors. 
     ■ Competitors with the highest points.
