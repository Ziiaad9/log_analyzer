import re

def extract_from_row(row):
    # Pattern principal pour extraire date, heure et message
    pattern = re.compile(r'^(\w{3})\s+(\d+)\s+(\d{2}:\d{2}:\d{2}).+?:\s+(.*)$')
    match = re.search(pattern, row)
    
    if match:
        month = match.group(1)
        day = match.group(2)
        time = match.group(3)
        message = match.group(4)
        
        # Extraction robuste de l'IP
        ip_match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', row)
        ip = ip_match.group(0) if ip_match else "N/A"
        
        # Extraction du Port (Groupe 6)
        port_match = re.search(r'port\s+(\d+)', row)
        port = port_match.group(1) if port_match else "N/A"
        
        return {
            "month": month,
            "day": day,
            "time": time,
            "message": message,
            "ip": ip,
            "port": port
        }
    return None