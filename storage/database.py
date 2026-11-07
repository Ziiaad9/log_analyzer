import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from process.extract_transform import extract_from_row
from ingestion.raw import towRows

def init_db(db_name="logs_analysis.db"):
    db_path = os.path.join(os.path.dirname(__file__), db_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Zdna l'colonne port TEXT hna
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ssh_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            day TEXT,
            time TEXT,
            message TEXT,
            ip TEXT,
            port TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

def store_logs(data_path):
    conn, cursor = init_db()
    
    # Vider la table pour éviter les doublons lors des tests
    cursor.execute('DELETE FROM ssh_logs')
    
    raw_lines = towRows(data_path)
    inserted_count = 0
    
    for row in raw_lines:
        parsed_data = extract_from_row(row)
        if parsed_data:
            cursor.execute('''
                INSERT INTO ssh_logs (month, day, time, message, ip, port)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                parsed_data['month'], 
                parsed_data['day'], 
                parsed_data['time'], 
                parsed_data['message'], 
                parsed_data['ip'], 
                parsed_data['port']
            ))
            inserted_count += 1
            
    conn.commit()
    conn.close()
    print(f"Succès ! {inserted_count} lignes (avec IP et Port) insérées dans la base de données.")

if __name__ == "__main__":
    path_to_data = os.path.join(os.path.dirname(__file__), '..', 'data')
    store_logs(path_to_data)