CREATE DATABASE IF NOT EXISTS tennis_analytics;
USE tennis_analytics;

-- 1. Categories (Parent table)
CREATE TABLE IF NOT EXISTS Categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- 2. Competitions (Child referencing Categories)
CREATE TABLE IF NOT EXISTS Competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50) NULL,
    type VARCHAR(50) NOT NULL,
    gender VARCHAR(20) NOT NULL,
    category_id VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE SET NULL
);

-- 3. Complexes (Parent table)
CREATE TABLE IF NOT EXISTS Complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);

-- 4. Venues (Child referencing Complexes)
CREATE TABLE IF NOT EXISTS Venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100) NOT NULL,
    city_name VARCHAR(100) NOT NULL,
    country_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(10) NOT NULL,
    timezone VARCHAR(100) NOT NULL,
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id) ON DELETE CASCADE
);

-- 5. Competitors (Parent table)
CREATE TABLE IF NOT EXISTS Competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    country_code VARCHAR(10) NOT NULL,
    abbreviation VARCHAR(20) NOT NULL
);

-- 6. Competitor_Rankings (Child referencing Competitors)
CREATE TABLE IF NOT EXISTS Competitor_Rankings (
    rank_id INT AUTO_INCREMENT PRIMARY KEY,
    `rank` INT NOT NULL,
    `movement` INT NOT NULL,
    `points` INT NOT NULL,
    `competitions_played` INT NOT NULL,
    competitor_id VARCHAR(50),
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id) ON DELETE CASCADE
);