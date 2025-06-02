import pandas as pd
from db import get_connection

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS claims, food_listings, receivers, providers CASCADE;
    """)

    cur.execute("""
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
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_csv_to_db(table, df):
    conn = get_connection()
    cur = conn.cursor()

    # Clean up column names: lowercase and stripped
    df.columns = [col.strip().lower() for col in df.columns]

    for i, row in df.iterrows():
        try:
            cols = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(row))
            sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
            cur.execute(sql, tuple(row))
        except Exception as e:
            print(f"Error inserting row {i}: {row.to_dict()}")
            raise e

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {len(df)} records into '{table}'.")

create_tables()

# Load and insert providers
df_providers = pd.read_csv("Data/providers_data.csv")
insert_csv_to_db("providers", df_providers)

# Load and insert receivers
df_receivers = pd.read_csv("Data/receivers_data.csv")
insert_csv_to_db("receivers", df_receivers)

# Load and insert food listings
df_food = pd.read_csv("Data/food_listings_data.csv")
df_food.columns = [col.strip().lower() for col in df_food.columns]
df_food['expiry_date'] = pd.to_datetime(df_food['expiry_date'], errors='coerce')
insert_csv_to_db("food_listings", df_food)

# Load and insert claims
df_claims = pd.read_csv("Data/claims_data.csv")
df_claims.columns = [col.strip().lower() for col in df_claims.columns]
df_claims['timestamp'] = pd.to_datetime(df_claims['timestamp'], errors='coerce')
insert_csv_to_db("claims", df_claims)
