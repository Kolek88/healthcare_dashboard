import psycopg2

try:
    # Connect to your database
    print("Connecting to the database...")
    conn = psycopg2.connect(
        dbname="hospital_db",
        user="postgres",
        password="CONFIDENTIAL_GITHUB",  
        host="localhost",
        port="5432"
    )
    print("Connected successfully!\n")

    # Create a cursor to execute commands
    cur = conn.cursor()

    # Run the "Wait Time" Analysis Query
    cur.execute("""
        SELECT 
            p.name, 
            v.wait_time_minutes,
            CASE 
                WHEN v.wait_time_minutes > 60 THEN 'Critical'
                WHEN v.wait_time_minutes > 30 THEN 'Moderate'
                ELSE 'On Time'
            END AS status
        FROM patients p
        JOIN visits v ON p.patient_id = v.patient_id
        ORDER BY v.wait_time_minutes DESC
        LIMIT 10;
    """)

    # Fetch the results
    rows = cur.fetchall()

    # Print a nice header
    print(f"{'PATIENT NAME':<20} | {'WAIT':<5} | {'STATUS'}")
    print("-" * 40)

    # Loop through and print each row
    for row in rows:
        print(f"{row[0]:<20} | {row[1]:<5} | {row[2]}")

except Exception as e:
    print("Error connecting to database:", e)

finally:
    # Clean up
    if 'conn' in locals() and conn:
        cur.close()
        conn.close()
        print("\nDatabase connection closed.")