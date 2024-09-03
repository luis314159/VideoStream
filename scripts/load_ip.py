import json

def load_ip(path:str ="ip_address.json"):
    # Cargar la IP desde el archivo JSON
    with open(path, 'r') as json_file:
        ip_data = json.load(json_file)
        ip = ip_data['ip']
    return ip

