import psycopg2
import pandas as pd
import warnings


warnings.filterwarnings('ignore', category=UserWarning)

print("Connecting to database...")

try:
    conn = psycopg2.connect(
        dbname="hospital_db",
        user="postgres",
        password="Khaliq88", 
        host="localhost",
        port="5432"
    )

    
    sql = """
    SELECT 
        p.patient_id, 
        p.name, 
        p.age, 
        p.gender, 
        v.visit_id, 
        v.wait_time_minutes
    FROM patients p
    JOIN visits v ON p.patient_id = v.patient_id;
    """

    print("Fetching data...")
    df = pd.read_sql(sql, conn)

    print("Saving to CSV...")
    df.to_csv('hospital_data.csv', index=False)
    
    print("Success! hospital_data.csv has been created.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'conn' in locals() and conn:
        conn.close()