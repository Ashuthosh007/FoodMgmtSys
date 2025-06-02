from db import fetch_all

# Food providers and receivers in each city
def providers_and_receivers_by_city():
    return fetch_all("""
        SELECT city, 
               (SELECT COUNT(*) FROM providers p WHERE p.city = c.city) AS providers,
               (SELECT COUNT(*) FROM receivers r WHERE r.city = c.city) AS receivers
        FROM (
            SELECT DISTINCT city FROM providers
            UNION
            SELECT DISTINCT city FROM receivers
        ) c
        ORDER BY city;
    """)

# Which type of provider contributes the most food
def provider_type_with_most_food():
    return fetch_all("""
        SELECT provider_type, COUNT(*) AS total
        FROM food_listings
        GROUP BY provider_type
        ORDER BY total DESC;
    """)

# Contact info of food providers in a specific city
def provider_contacts_by_city(city):
    return fetch_all("""
        SELECT name, type, contact
        FROM providers
        WHERE city = %s;
    """, (city,))

# Receivers who claimed the most food
def top_receivers_by_claim_count():
    return fetch_all("""
        SELECT r.name, COUNT(c.claim_id) AS total_claims
        FROM receivers r
        JOIN claims c ON r.receiver_id = c.receiver_id
        GROUP BY r.name
        ORDER BY total_claims DESC;
    """)

# Total quantity of food available
def total_food_quantity():
    return fetch_all("""
        SELECT SUM(quantity) FROM food_listings;
    """)

# City with the most food listings
def city_with_most_food():
    return fetch_all("""
        SELECT location, COUNT(*) AS total
        FROM food_listings
        GROUP BY location
        ORDER BY total DESC;
    """)

# Most commonly available food types
def most_common_food_types():
    return fetch_all("""
        SELECT food_type, COUNT(*) AS count
        FROM food_listings
        GROUP BY food_type
        ORDER BY count DESC;
    """)

# Food claims made per food item
def claims_per_food_item():
    return fetch_all("""
        SELECT f.food_name, COUNT(c.claim_id) AS claims
        FROM food_listings f
        JOIN claims c ON f.food_id = c.food_id
        GROUP BY f.food_name
        ORDER BY claims DESC;
    """)

# Provider with most successful claims
def top_provider_by_completed_claims():
    return fetch_all("""
        SELECT p.name, COUNT(*) AS successful_claims
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        JOIN providers p ON f.provider_id = p.provider_id
        WHERE c.status = 'Completed'
        GROUP BY p.name
        ORDER BY successful_claims DESC;
    """)

# Claims status breakdown
def claims_status_breakdown():
    return fetch_all("""
        SELECT status, COUNT(*) FROM claims
        GROUP BY status;
    """)

# Avg quantity claimed per receiver
def avg_quantity_per_receiver():
    return fetch_all("""
        SELECT AVG(f.quantity) 
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id;
    """)

# Most claimed meal type
def most_claimed_meal_type():
    return fetch_all("""
        SELECT f.meal_type, COUNT(*) AS total_claims
        FROM claims c
        JOIN food_listings f ON c.food_id = f.food_id
        GROUP BY f.meal_type
        ORDER BY total_claims DESC;
    """)

# Total food donated by each provider
def total_food_by_provider():
    return fetch_all("""
        SELECT p.name, SUM(f.quantity) AS total_quantity
        FROM providers p
        JOIN food_listings f ON p.provider_id = f.provider_id
        GROUP BY p.name
        ORDER BY total_quantity DESC;
    """)
