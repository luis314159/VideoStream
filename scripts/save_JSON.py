import json


def main():

    # IP que quieres guardar
    ip_data = {
        "ip": "10.137.150.99"
    }

    # Guardar en un archivo JSON
    with open('ip_address.json', 'w') as json_file:
        json.dump(ip_data, json_file)

if __name__ == "__main__":
    main()