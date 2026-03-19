import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

# 1. Connect (The same code as before)
conn = psycopg2.connect(
    dbname="hospital_db",
    user="postgres",
    password="Khaliq88", 
    host="localhost",
    port="5432"
)

# 2. Use Pandas to run the SQL and get a "DataFrame" (Table)
sql = """
SELECT name, wait_time_minutes 
FROM visits 
JOIN patients ON visits.patient_id = patients.patient_id
ORDER BY wait_time_minutes DESC
LIMIT 10;
"""
df = pd.read_sql(sql, conn)

# 3. Create the Bar Chart
plt.figure(figsize=(10, 6))  # Make the image 10x6 inches
plt.bar(df['name'], df['wait_time_minutes'], color='skyblue')

# 4. Style it
plt.title('Patient Wait Times (Real-Time DB Data)')
plt.xlabel('Patient Name')
plt.ylabel('Minutes Waited')
plt.xticks(rotation=45)      # Tilt the names so they don't overlap
plt.axhline(y=60, color='r', linestyle='--', label='Critical Threshold (60m)') # Red line
plt.legend()

# 5. Show it (and save it!)
plt.tight_layout()
plt.savefig('hospital_analysis.png')  # <--- This saves the image for your portfolio!
plt.show()

conn.close()