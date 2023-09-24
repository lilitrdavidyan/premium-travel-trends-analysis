
-- initialize_database.sql

-- Creating Database if not exists
CREATE DATABASE IF NOT EXISTS LuxuryToursDB;
USE LuxuryToursDB;

-- Creating the Tour Table
CREATE TABLE IF NOT EXISTS Tour (
    id VARCHAR(255) PRIMARY KEY,
    brand VARCHAR(255),
    type VARCHAR(255),
    slug VARCHAR(255),
    url VARCHAR(255),
    title TEXT,
    subTitle TEXT,
    shortDescription TEXT,
    highlights TEXT,
    createdAt DATETIME
);

-- Creating the Itinerary Table
CREATE TABLE IF NOT EXISTS Itinerary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id VARCHAR(255),
    day_number INT,
    title TEXT,
    description TEXT,
    FOREIGN KEY (tour_id) REFERENCES Tour(id)
);

-- Creating the Options Table
CREATE TABLE IF NOT EXISTS Options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id VARCHAR(255),
    title TEXT,
    price DECIMAL(10,2),
    value DECIMAL(10,2),
    discount DECIMAL(5,2),
    FOREIGN KEY (tour_id) REFERENCES Tour(id)
);

-- Creating the Destination Table
CREATE TABLE IF NOT EXISTS Destination (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id VARCHAR(255),
    name VARCHAR(255),
    type VARCHAR(255),
    country VARCHAR(255),
    FOREIGN KEY (tour_id) REFERENCES Tour(id)
);

-- Creating the Addons Table
CREATE TABLE IF NOT EXISTS Addons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id VARCHAR(255),
    title TEXT,
    price DECIMAL(10,2),
    FOREIGN KEY (tour_id) REFERENCES Tour(id)
);
