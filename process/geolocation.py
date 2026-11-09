import requests

IP_CACHE = {}
API_LIMIT_REACHED = False

def get_location(ip):
    global API_LIMIT_REACHED
    
    # Les IPs locales (bhal 127.0.0.1 wla N/A) ma kayt-geolocalisawch
    if ip == "N/A" or ip.startswith("127.") or ip.startswith("10.") or ip.startswith("192.168."):
        return "Local"
        
    # Ila l-IP fayt 9llebna 3liha, n-jbdouha mn l-cache
    if ip in IP_CACHE:
        return IP_CACHE[ip]
        
    # Ila wsslna l limite d l'API (1000/jour), ghay-smehom Limit_Reached bach may-t3tlch
    if API_LIMIT_REACHED:
        return "Limit_Reached"
        
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=2)
        
        if response.status_code == 200:
            data = response.json()
            country = data.get("country", "Unknown")
            IP_CACHE[ip] = country
            return country
            
        elif response.status_code == 429:
            print("\n⚠️ Limite de l'API atteinte. Les IPs restantes seront 'Limit_Reached'.")
            API_LIMIT_REACHED = True
            return "Limit_Reached"
            
    except Exception as e:
        pass 
        
    IP_CACHE[ip] = "Unknown" 
    return "Unknown"

if __name__ == "__main__":
    print(get_location("109.199.110.135"))