import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from process.extract_transform import extract_from_row
from process.geolocation import get_location
from ingestion.raw import towRows

def init_db(db_name="logs_analysis.db"):
    db_path = os.path.join(os.path.dirname(__file__), db_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ssh_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT,
            day TEXT,
            time TEXT,
            message TEXT,
            ip TEXT,
            port TEXT,
            country TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

def store_logs(data_path):
    conn, cursor = init_db()
    
    # Vider la table pour repartir à zéro
    cursor.execute('DELETE FROM ssh_logs')
    
    raw_lines = towRows(data_path)
    inserted_count = 0
    
    # Dictionnaire cache pour ne pas interroger l'API 2 fois pour la même IP
    ip_cache = {}
    
    print("Traitement et géolocalisation des logs en cours...")
    for row in raw_lines:
        parsed_data = extract_from_row(row)
        if parsed_data:
            ip = parsed_data['ip']
            
            # Gestion du Cache pour l'IP
            if ip == "N/A" or ip.startswith("127.") or ip.startswith("10.") or ip.startswith("192.168."):
                country = "Local"
            elif ip in ip_cache:
                country = ip_cache[ip]  # On récupère depuis le cache si déjà vu
            else:
                country = get_location(ip)
                ip_cache[ip] = country  # On sauvegarde dans le cache
            
            cursor.execute('''
                INSERT INTO ssh_logs (month, day, time, message, ip, port, country)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                parsed_data['month'], 
                parsed_data['day'], 
                parsed_data['time'], 
                parsed_data['message'], 
                ip, 
                parsed_data['port'],
                country
            ))
            inserted_count += 1
            
    conn.commit()
    conn.close()
    print(f"Succès ! {inserted_count} lignes insérées avec succès dans la base de données.")

if __name__ == "__main__":
    path_to_data = os.path.join(os.path.dirname(__file__), '..', 'data')
    store_logs(path_to_data)