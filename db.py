import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="food_waste_mgmt",
        user="postgres",
        password="custom",
        host="localhost",
        port="5432"
    )

def fetch_all(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

def execute_query(query, params=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params or ())
    conn.commit()
    cur.close()
    conn.close()

def fix_sequence(table, pk_column):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"""
            SELECT setval(
                pg_get_serial_sequence('{table}', '{pk_column}'),
                COALESCE((SELECT MAX({pk_column}) FROM {table}), 1)
            );
        """)
        conn.commit()
        print(f"Sequence for {table}.{pk_column} has been fixed.")
    except Exception as e:
        print(f"Failed to fix sequence: {e}")
    finally:
        cur.close()
        conn.close()
