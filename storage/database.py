import psycopg2
from process import extract_transform
from ingestion import raw
from process import geolocation

def get_db_connection():
    return psycopg2.connect(
        dbname="log_analysis", 
        user="postgres",
        password="123", 
        host="localhost",
        port="5432"
    )

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ssh_logs (
            id SERIAL PRIMARY KEY,
            month VARCHAR(50),
            day VARCHAR(50),
            time VARCHAR(50),
            ip_address VARCHAR(50),
            port VARCHAR(20),
            message TEXT,
            country VARCHAR(100)
        )
    ''')
    
    # HAD S-STER HOWA LI KAY-KHWI L-TABLE MN DAK "UNKNOWN" L-9DIM AUTOMATIQUEMENT
    cursor.execute('TRUNCATE TABLE ssh_logs RESTART IDENTITY')
    
    logs = raw.towRows('./data')
    total = len(logs)
    print(f"🚀 Début du traitement de {total} logs...")
    
    for i, log_line in enumerate(logs):
        extracted = extract_transform.extract_from_row(log_line)
        if extracted:
            country = geolocation.get_location(extracted['ip'])
            cursor.execute('''
                INSERT INTO ssh_logs (month, day, time, ip_address, port, message, country)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                extracted['month'], extracted['day'], extracted['time'], 
                extracted['ip'], extracted['port'], extracted['message'], country
            ))
        
        if i % 1000 == 0 and i > 0:
            print(f"⏳ {i} / {total} lignes traitées...")
            conn.commit() 
            
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Données insérées avec succès dans PostgreSQL !")

if __name__ == "__main__":
    setup_database()