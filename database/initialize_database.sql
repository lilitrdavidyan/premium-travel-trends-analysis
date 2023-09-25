-- initialize_database.sql

-- Creating Database if not exists
CREATE DATABASE IF NOT EXISTS LuxuryToursDB;
USE LuxuryToursDB;

-- Creating the Tour Table
CREATE TABLE  IF NOT EXISTS tours (
    id CHAR(41) PRIMARY KEY,
    productType VARCHAR(255),
    source VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    brand VARCHAR(255),
    brandName VARCHAR(255),
    brandCode VARCHAR(255),
    slug VARCHAR(255),
    depositAmount DECIMAL(10,2), 
    activityLevel VARCHAR(255),
    reviewsRating DECIMAL(4,2),
    reviewsTotal INT,
    reviewsSource VARCHAR(255),
    lowestOptionRoomType VARCHAR(255),
    lowestOptionPrice DECIMAL(10,2), 
    lowestOptionFullPrice DECIMAL(10,2), 
    fkSeasonId CHAR(36),
    fkTourOptionId CHAR(36),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tour_options (
    id CHAR(36) PRIMARY KEY,
    tour_id CHAR(41) NOT NULL,
    sourceTourOptionName VARCHAR(255),
    isPrivateRequest BOOLEAN,
    slug VARCHAR(255),
    maxPax INT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    travelInclusions TEXT,
    diningInclusions TEXT,
    startLocationName VARCHAR(255),
    startLocationCountryCode CHAR(2),
    startLocationLongitude DECIMAL(9,6),
    startLocationLatitude DECIMAL(9,6),
    endLocationName VARCHAR(255),
    endLocationCountryCode CHAR(2),
    endLocationLongitude DECIMAL(9,6),
    endLocationLatitude DECIMAL(9,6),
    countries_visited VARCHAR(255),
    minChildPriceAge INT,
    maxChildPriceAge INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tour_id) REFERENCES tours (id)
);


-- Creating the Itinerary Table
CREATE TABLE IF NOT EXISTS itineraries (
	id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id CHAR(41) NOT NULL,
    tour_option_id CHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    startDay INT,
    duration INT,
    accommodation VARCHAR(255),
    meals VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tour_id) REFERENCES tours (id),
    FOREIGN KEY (tour_option_id) REFERENCES tour_options (id)
);

CREATE TABLE IF NOT EXISTS locations_visited (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id CHAR(41) NOT NULL,
    itinerary_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    countryCode CHAR(2),
    longitude DOUBLE,
    latitude DOUBLE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (itinerary_id) REFERENCES itineraries (id)
);

CREATE TABLE IF NOT EXISTS options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tour_id CHAR(41) NOT NULL,
    roomType VARCHAR(255),
    price DECIMAL(13, 2),
    fullPrice DECIMAL(13, 2),
    fkRoomTypePricingId CHAR(36),
    fkDepartureId CHAR(36),
    fkSeasonId CHAR(36),
    fkTourOptionId CHAR(36),
    fkTourId CHAR(41),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (tour_id) REFERENCES tours (id)
);


CREATE TABLE IF NOT EXISTS departures (
    id CHAR(36) PRIMARY KEY,
    fkSeasonId CHAR(36),
    fkTourOptionId CHAR(36),
    startDate DATE,
    endDate DATE,
    availability VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	FOREIGN KEY (fkTourOptionId) REFERENCES tour_options (id)
);



