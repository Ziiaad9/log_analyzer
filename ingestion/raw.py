import os
import gzip

def towRows(path):
    all_rows = []
    files = os.listdir(path)

    for file in files:
        file_path = os.path.join(path, file)
        
        # Ignorer les dossiers s'il y en a par erreur
        if os.path.isdir(file_path):
            continue
            
        opener = gzip.open(file_path, mode='rt', encoding='utf-8') if file.endswith('.gz') else open(file_path, 'r', encoding='utf-8')
        
        try:
            with opener as f:
                # Ajoute les lignes du fichier courant à la liste globale
                all_rows.extend(f.readlines())
        except Exception as e:
            print(f"Erreur lors de la lecture de {file}: {e}")
            
    return all_rows

if __name__ == '__main__':
    # Affiche les 10 premières lignes de tous les fichiers combinés
    print(towRows('./data')[:10])