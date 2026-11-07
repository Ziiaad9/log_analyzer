import sqlite3
import os
import re
import matplotlib.pyplot as plt
from collections import Counter

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'storage', 'logs_analysis.db')
    return sqlite3.connect(db_path)

def generate_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()

    # ==========================================
    # 1: Tentatives échouées par pays (Filtre Unknown/Local)
    # ==========================================
    cursor.execute('''
        SELECT country, COUNT(*) 
        FROM ssh_logs 
        WHERE (message LIKE '%Failed password%' OR message LIKE '%authentication failure%')
          AND country != 'Unknown' 
          AND country != 'Local'
        GROUP BY country 
        ORDER BY COUNT(*) DESC 
        LIMIT 10
    ''')
    failed_by_country = cursor.fetchall()

    # ==========================================
    # 2: Tentatives réussies par user (Correction de la Regex)
    # ==========================================
    cursor.execute('''
        SELECT message 
        FROM ssh_logs 
        WHERE message LIKE '%session opened%' 
           OR message LIKE '%Accepted password%'
    ''')
    success_messages = cursor.fetchall()
    
    success_users = []
    for (msg,) in success_messages:
        # Regex améliorée pour capturer le VRAI nom d'utilisateur (ex: "root")
        match = re.search(r'(?:for user |user |for )([a-zA-Z0-9_.-]+)', msg)
        if match:
            user = match.group(1)
            if user not in ['from', 'port']:
                success_users.append(user)
                
    user_counts = Counter(success_users).most_common(10)

    # ==========================================
    # 3: Tentatives "invalid user" par pays (Filtre Unknown/Local)
    # ==========================================
    cursor.execute('''
        SELECT country, COUNT(*) 
        FROM ssh_logs 
        WHERE message LIKE '%Invalid user%' 
          AND country != 'Unknown' 
          AND country != 'Local'
        GROUP BY country 
        ORDER BY COUNT(*) DESC 
        LIMIT 10
    ''')
    invalid_users_data = cursor.fetchall()

    conn.close()

    # ==========================================
    # DESSIN DU DASHBOARD
    # ==========================================
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Dashboard d\'Analyse des Logs SSH', fontsize=18, fontweight='bold', color='#333333')

    # Graphique 1
    if failed_by_country:
        countries, counts = zip(*failed_by_country)
        axes[0].bar(countries, counts, color='tomato', edgecolor='black')
        axes[0].set_title('Tentatives échouées par pays', fontsize=12)
        axes[0].set_ylabel('Nombre de tentatives')
        axes[0].tick_params(axis='x', rotation=45)
        for i, v in enumerate(counts):
            axes[0].text(i, v + (max(counts)*0.01), str(v), ha='center')

    # Graphique 2
    if user_counts:
        users, u_counts = zip(*user_counts)
        axes[1].bar(users, u_counts, color='mediumseagreen', edgecolor='black')
        axes[1].set_title('Tentatives réussies par utilisateur', fontsize=12)
        axes[1].set_ylabel('Nombre de réussites')
        axes[1].tick_params(axis='x', rotation=45)
        for i, v in enumerate(u_counts):
            axes[1].text(i, v + (max(u_counts)*0.01), str(v), ha='center')

    # Graphique 3
    if invalid_users_data:
        inv_countries, inv_counts = zip(*invalid_users_data)
        axes[2].bar(inv_countries, inv_counts, color='orange', edgecolor='black')
        axes[2].set_title('Tentatives "Invalid User" par pays', fontsize=12)
        axes[2].set_ylabel('Nombre de tentatives')
        axes[2].tick_params(axis='x', rotation=45)
        for i, v in enumerate(inv_counts):
            axes[2].text(i, v + (max(inv_counts)*0.01), str(v), ha='center')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    generate_dashboard()