USE tennis_analytics;

-- =====================================================================
-- 1. COMPETITIONS ANALYSIS
-- =====================================================================

-- 1.1 List all competitions along with their category name
SELECT 
    c.competition_id,
    c.competition_name,
    cat.category_name,
    c.type,
    c.gender
FROM Competitions c
LEFT JOIN Categories cat ON c.category_id = cat.category_id;

-- 1.2 Count the number of competitions in each category
SELECT 
    cat.category_name,
    COUNT(c.competition_id) AS competition_count
FROM Categories cat
LEFT JOIN Competitions c ON cat.category_id = c.category_id
GROUP BY cat.category_name
ORDER BY competition_count DESC;

-- 1.3 Find all competitions of type 'doubles'
SELECT 
    competition_id,
    competition_name,
    type,
    gender
FROM Competitions
WHERE LOWER(type) = 'doubles';

-- 1.4 Get competitions that belong to a specific category (e.g., ITF Men)
SELECT 
    c.competition_id,
    c.competition_name,
    cat.category_name
FROM Competitions c
JOIN Categories cat ON c.category_id = cat.category_id
WHERE cat.category_name = 'ITF Men';

-- 1.5 Identify parent competitions and their sub-competitions
SELECT 
    parent.competition_name AS parent_competition,
    child.competition_name AS sub_competition
FROM Competitions child
JOIN Competitions parent ON child.parent_id = parent.competition_id;

-- 1.6 Analyze the distribution of competition types by category
SELECT 
    cat.category_name,
    c.type,
    COUNT(c.competition_id) AS total_competitions
FROM Categories cat
JOIN Competitions c ON cat.category_id = c.category_id
GROUP BY cat.category_name, c.type
ORDER BY cat.category_name, total_competitions DESC;

-- 1.7 List all competitions with no parent (top-level competitions)
SELECT 
    competition_id,
    competition_name,
    type,
    gender
FROM Competitions
WHERE parent_id IS NULL;


-- =====================================================================
-- 2. VENUE ANALYSIS
-- =====================================================================

-- 2.1 List all venues along with their associated complex name
SELECT 
    v.venue_name,
    v.city_name,
    v.country_name,
    c.complex_name
FROM Venues v
JOIN Complexes c ON v.complex_id = c.complex_id;

-- 2.2 Count the number of venues in each complex
SELECT 
    c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM Complexes c
LEFT JOIN Venues v ON c.complex_id = v.complex_id
GROUP BY c.complex_name
ORDER BY venue_count DESC;

-- 2.3 Get details of venues in a specific country (e.g., Chile or Great Britain)
SELECT 
    venue_name,
    city_name,
    country_name,
    country_code,
    timezone
FROM Venues
WHERE country_name = 'Chile';

-- 2.4 Identify all venues and their timezones
SELECT 
    venue_name,
    country_name,
    timezone
FROM Venues
ORDER BY timezone;

-- 2.5 Find complexes that have more than one venue
SELECT 
    c.complex_name,
    COUNT(v.venue_id) AS venue_count
FROM Complexes c
JOIN Venues v ON c.complex_id = v.complex_id
GROUP BY c.complex_name
HAVING COUNT(v.venue_id) > 1;

-- 2.6 List venues grouped by country
SELECT 
    country_name,
    COUNT(venue_id) AS total_venues
FROM Venues
GROUP BY country_name
ORDER BY total_venues DESC;

-- 2.7 Find all venues for a specific complex (e.g., Nacional)
SELECT 
    v.venue_name,
    v.city_name,
    v.country_name,
    c.complex_name
FROM Venues v
JOIN Complexes c ON v.complex_id = c.complex_id
WHERE c.complex_name LIKE '%Nacional%';


-- =====================================================================
-- 3. COMPETITOR RANKING ANALYSIS
-- =====================================================================

-- 3.1 Get all competitors with their rank and points
SELECT 
    c.name,
    c.country,
    r.`rank`,
    r.points
FROM Competitor_Rankings r
JOIN Competitors c ON r.competitor_id = c.competitor_id
ORDER BY r.`rank` ASC;

-- 3.2 Find competitors ranked in the top 5
SELECT 
    c.name,
    c.country,
    r.`rank`,
    r.points
FROM Competitor_Rankings r
JOIN Competitors c ON r.competitor_id = c.competitor_id
ORDER BY r.`rank` ASC
LIMIT 5;

-- 3.3 List competitors with no rank movement (stable rank)
SELECT 
    c.name,
    c.country,
    r.`rank`,
    r.movement
FROM Competitor_Rankings r
JOIN Competitors c ON r.competitor_id = c.competitor_id
WHERE r.movement = 0
ORDER BY r.`rank` ASC;

-- 3.4 Get the total points of competitors from a specific country (e.g., Croatia)
SELECT 
    c.country,
    SUM(r.points) AS total_points,
    COUNT(c.competitor_id) AS total_players
FROM Competitors c
JOIN Competitor_Rankings r ON c.competitor_id = r.competitor_id
WHERE c.country = 'Croatia'
GROUP BY c.country;

-- 3.5 Count the number of competitors per country
SELECT 
    country,
    COUNT(competitor_id) AS competitor_count
FROM Competitors
GROUP BY country
ORDER BY competitor_count DESC;

-- 3.6 Find competitors with the highest points in the current week
SELECT 
    c.name,
    c.country,
    r.`rank`,
    r.points
FROM Competitor_Rankings r
JOIN Competitors c ON r.competitor_id = c.competitor_id
ORDER BY r.points DESC
LIMIT 10;