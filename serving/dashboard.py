import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Ignorer les avertissements mineurs de Pandas liés aux connexions directes PostgreSQL
warnings.filterwarnings('ignore', category=UserWarning)

def get_db_connection():
    """Établit la connexion à la base de données PostgreSQL log_analysis."""
    return psycopg2.connect(
        dbname="log_analysis", 
        user="postgres",
        password="123", 
        host="localhost",
        port="5432"
    )

def generate_dashboard():
    """Récupère les données et génère les graphiques Matplotlib."""
    print("📊 Connexion à PostgreSQL et récupération des données en cours...")
    
    try:
        conn = get_db_connection()
        df = pd.read_sql_query("SELECT * FROM ssh_logs;", conn)
        conn.close()
    except Exception as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return

    if df.empty:
        print("⚠️ Aucune donnée trouvée.")
        return

    print(f"✅ {len(df)} lignes récupérées ! Création des graphiques...")

    plt.figure(figsize=(15, 10))
    plt.suptitle("Tableau de Bord - Analyse des Logs SSH", fontsize=16, fontweight='bold', y=0.98)

    # 1. Top 10 des Pays (FILTRÉ)
    plt.subplot(2, 2, 1)
    # Hna kan-7iydo Limit_Reached, Local, w Unknown
    df_countries = df[~df['country'].isin(['Limit_Reached', 'Local', 'Unknown'])]
    top_countries = df_countries['country'].value_counts().head(10)
    top_countries.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Top 10 des Pays')
    plt.xlabel('Pays')
    plt.ylabel('Nombre de requêtes')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 2. Top 10 des Adresses IP (FILTRÉ)
    plt.subplot(2, 2, 2)
    # Hna kan-7iydo N/A w l-adresses locales bhal 127.0.0.1
    df_ips = df[~df['ip_address'].isin(['N/A', '127.0.0.1'])]
    top_ips = df_ips['ip_address'].value_counts().head(10)
    top_ips.plot(kind='bar', color='salmon', edgecolor='black')
    plt.title('Top 10 des Adresses IP ciblées')
    plt.xlabel('Adresse IP')
    plt.ylabel('Nombre de requêtes')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # 3. Top 10 des Ports visés (Déjà filtré f l'ancien code)
    plt.subplot(2, 2, 3)
    df_ports = df[df['port'].notna() & (df['port'] != '') & (df['port'] != 'N/A')]
    top_ports = df_ports['port'].value_counts().head(10)
    top_ports.plot(kind='bar', color='lightgreen', edgecolor='black')
    plt.title('Top 10 des Ports Visés')
    plt.xlabel('Port')
    plt.ylabel('Nombre de requêtes')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    generate_dashboard()