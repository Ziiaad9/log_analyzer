import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Ignorer les avertissements mineurs de Pandas
warnings.filterwarnings('ignore', category=UserWarning)

def get_db_connection():
    """Établit la connexion à la base de données PostgreSQL Log_Analyser."""
    return psycopg2.connect(
        dbname="log_analysis", 
        user="postgres",
        password="123", 
        host="localhost",
        port="5432"
    )

def generate_dashboard():
    """Récupère les données et génère les graphiques selon les consignes exactes."""
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

    print(f"✅ {len(df)} lignes récupérées ! Création du dashboard officiel...")

    plt.figure(figsize=(16, 10))
    plt.suptitle("Tableau de Bord - Sécurité SSH (Rapport Professeur)", fontsize=16, fontweight='bold', y=0.96)

    # Normalisation des colonnes au cas où (pour s'adapter au format texte du message)
    # On suppose que le message contient des mots clés comme 'Failed', 'Accepted', 'invalid user'
    if 'message' in df.columns:
        df['message_lower'] = df['message'].str.lower()
    else:
        df['message_lower'] = ''

    # 1. Nombre de tentatives échouées par pays
    plt.subplot(2, 2, 1)
    if 'country' in df.columns and 'message_lower' in df.columns:
        # Filtrer les échecs (failed) et éliminer les valeurs inconnues/locales
        df_failed = df[df['message_lower'].str.contains('failed|failure|invalid', na=False)]
        df_failed_countries = df_failed[~df_failed['country'].isin(['Limit_Reached', 'Local', 'Unknown', 'N/A'])]
        top_failed_countries = df_failed_countries['country'].value_counts().head(10)
        
        top_failed_countries.plot(kind='bar', color='indianred', edgecolor='black')
        plt.title('1. Tentatives Échouées par Pays')
        plt.xlabel('Pays')
        plt.ylabel('Nombre d\'échecs')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
    else:
        plt.title('1. Tentatives Échouées par Pays (Données manquantes)')

    # 2. Nombre de tentatives réussies par user
    plt.subplot(2, 2, 2)
    if 'message_lower' in df.columns:
        # Filtrer les connexions réussies (accepted)
        df_success = df[df['message_lower'].str.contains('accepted', na=False)]
        
        # Extraction ou utilisation de la colonne user si elle existe, sinon parsing basique du message
        if 'username' in df.columns:
            top_users = df_success['username'].value_counts().head(10)
        elif 'user' in df.columns:
            top_users = df_success['user'].value_counts().head(10)
        else:
            # Extraction approximative depuis le message "Accepted password for <user> from..."
            extracted_users = df_success['message_lower'].str.extract(r'for\s+([^\s]+)\s+from')[0]
            top_users = extracted_users.value_counts().head(10)
            
        top_users.plot(kind='bar', color='mediumseagreen', edgecolor='black')
        plt.title('2. Tentatives Réussies par User')
        plt.xlabel('Utilisateur')
        plt.ylabel('Nombre de réussites')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
    else:
        plt.title('2. Tentatives Réussies par User (Données manquantes)')

    # 3. Tentatives échouées avec invalid user
    plt.subplot(2, 2, 3)
    if 'message_lower' in df.columns:
        # Filtrer spécifiquement les "invalid user"
        df_invalid = df[df['message_lower'].str.contains('invalid user', na=False)]
        
        # Extraire les noms d'utilisateurs invalides ciblés
        invalid_users = df_invalid['message_lower'].str.extract(r'invalid user\s+([^\s]+)')[0]
        top_invalid = invalid_users.value_counts().head(10)
        
        if top_invalid.empty:
            # Fallback si l'extraction regex donne vide, compter par IP ou message
            top_invalid = df_invalid['ip_address'].value_counts().head(10)
            plt.title('3. Tentatives Échouées (Invalid User - par IP)')
            plt.xlabel('Adresse IP')
        else:
            plt.title('3. Top Utilisateurs Invalides (Invalid User)')
            plt.xlabel('Nom d\'utilisateur visé')
            
        top_invalid.plot(kind='bar', color='orange', edgecolor='black')
        plt.ylabel('Nombre de tentatives')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
    else:
        plt.title('3. Tentatives Échouées avec Invalid User')

    plt.tight_layout(rect=[0, 0, 1, 0.94])
    plt.show()

if __name__ == "__main__":
    generate_dashboard()