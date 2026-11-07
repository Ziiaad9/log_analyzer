import re


def extract_from_row(row):
    # Pattern avec un 5ème groupe optionnel pour l'IP à la fin de la ligne
    pattern = re.compile(r'^(\w{3})\s+(\d+)\s+(\d{2}:\d{2}:\d{2}).+?:\s+(.+?)(?:from\s+(\d+\.\d+\.\d+\.\d+))?$')
    match = re.search(pattern, row)
    if match:
        print(
            f'month: {match.group(1)}\n'
            f'day of month: {match.group(2)}\n'
            f'time: {match.group(3)}\n'
            f'message: {match.group(4)}\n'
            f'ip: {match.group(5) if match.lastindex >= 5 and match.group(5) else "N/A"}'
        )