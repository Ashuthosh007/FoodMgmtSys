# Food Mangement System
It is an Food Management Application using Python and PostgreSQL, The UI is done using Streamlit. This application is mainly used to track the food usage and consumption per city. A Streamlit-powered web application to manage surplus food distribution from providers.

---

## Features

- **Food Listings**: View available food by location with relevant details.
- **Add Listing**: Register new food donations by existing providers.
- **Insights & Analytics**: Visualize provider stats, food claims, common food types, and more.
- **Data Management**: Includes scripts for database creation and CSV-based data population.

---

## Technologies Used

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python (psycopg2 for PostgreSQL)
- **Database**: PostgreSQL
- **Data Loading**: Pandas for CSV integration

---

## Project Structure

```
├── app.py               # Streamlit UI and logic
├── db.py                # Database connection and utility functions
├── data_loader.py       # Table creation and CSV import
├── queries.py           # Insight-generating SQL queries
├── Food_mgmt.sql        # SQL schema for PostgreSQL database
├── Data/
│   ├── providers_data.csv
│   ├── receivers_data.csv
│   ├── food_listings_data.csv
│   └── claims_data.csv
```

---

## Setup Instructions

### 1. PostgreSQL Setup

- Create a database:

```sql
CREATE DATABASE food_waste_mgmt;
```

### 2. Python Environment

Ensure you have the required libraries:

```bash
pip install streamlit pandas psycopg2
```

### 3. Data Ingestion

To reset and populate the database from CSVs:

```bash
python data_loader.py
```

Ensure the following CSVs are placed in the `Data/` directory:
- `providers_data.csv`
- `receivers_data.csv`
- `food_listings_data.csv`
- `claims_data.csv`

---

## Running the App

```bash
streamlit run app.py
```

The app will launch in your browser with options to:
- View food listings by city.
- Add new listings.
- Explore analytics and insights.

---

## Available Insights

- Providers & receivers per city
- Top food-donating provider types
- Receiver activity
- Total and average food quantities
- Most claimed food and meal types
- Status of claims

---

## Future Improvements

- User authentication (admin vs receiver/provider roles)
- Real-time notifications for food expiry
- Location-based claim recommendations

---
