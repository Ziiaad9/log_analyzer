import requests
import json

def get_location(ip):
    # Ila kant l'IP local (bhal 127.0.0.1) wla N/A, ma n-3yytoch l'API
    if ip == "N/A" or ip.startswith("127.") or ip.startswith("10.") or ip.startswith("192.168."):
        return "Local"
        
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            data = response.json()
            # K-t-returni l'pays (ex: "Morocco", "France", etc.) wla "Unknown"
            return data.get("country", "Unknown")
    except Exception as e:
        print(f"Erreur géolocalisation pour {ip}: {e}")
        
    return "Unknown"

if __name__ == "__main__":
    # Test dyal l'fonction b IP bhal li darto f l'qissm
    print(get_location("109.199.110.135"))