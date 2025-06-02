CREATE DATABASE food_waste_mgmt;

CREATE TABLE providers (
    provider_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(50),
    address TEXT,
    city VARCHAR(50),
    contact VARCHAR(20)
);

CREATE TABLE receivers (
    receiver_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    type VARCHAR(50),
    city VARCHAR(50),
    contact VARCHAR(20)
);

CREATE TABLE food_listings (
    food_id SERIAL PRIMARY KEY,
    food_name VARCHAR(100),
    quantity INT,
    expiry_date DATE,
    provider_id INT REFERENCES providers(provider_id),
    provider_type VARCHAR(50),
    location VARCHAR(50),
    food_type VARCHAR(50),
    meal_type VARCHAR(50)
);

CREATE TABLE claims (
    claim_id SERIAL PRIMARY KEY,
    food_id INT REFERENCES food_listings(food_id),
    receiver_id INT REFERENCES receivers(receiver_id),
    status VARCHAR(20),
    timestamp TIMESTAMP
);

CREATE TABLE providers (
            provider_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            type VARCHAR(50),
            address TEXT,
            city VARCHAR(50),
            contact VARCHAR(100)
        );

CREATE TABLE receivers (
            receiver_id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            type VARCHAR(50),
            city VARCHAR(50),
            contact VARCHAR(100)
        );

CREATE TABLE food_listings (
            food_id SERIAL PRIMARY KEY,
            food_name VARCHAR(100),
            quantity INT,
            expiry_date DATE,
            provider_id INT REFERENCES providers(provider_id),
            provider_type VARCHAR(50),
            location VARCHAR(50),
            food_type VARCHAR(50),
            meal_type VARCHAR(50)
        );

CREATE TABLE claims (
            claim_id SERIAL PRIMARY KEY,
            food_id INT REFERENCES food_listings(food_id),
            receiver_id INT REFERENCES receivers(receiver_id),
            status VARCHAR(20),
            timestamp TIMESTAMP
        );

