from flask import jsonify, request
from Inventario import *
from UpdatePorts import *
from ChangeIP import *
from Tools import *
from MerakiAPIFlask import *
from config import URL,APIKEY

#Get Netwrok per @app.route
def get_networks(orgID):
    network_type = request.args.get('type')
    try:
        networks = getNtwID_Name(URL, APIKEY, orgID)  # Recupera tutte le reti
    except Exception as e:
        print(f"Errore: {e}")  # Stampa l'errore per il debug
        return jsonify({"error": "Errore nel recupero delle reti.", "message": str(e)}), 500
    #Creo Array Network
    filtered_networks = []
    # Filtrare le reti in base al tipo selezionato
    for ntw in networks:
        #if network_type == "SINGLE_NTW" and ntw[1].startswith("SNI"):
        #    filtered_networks.append(ntw)
        if network_type == "SNIPER" and ntw[1].startswith("SNI"):
            filtered_networks.append(ntw)
        elif network_type == "NEGOZIO" and ntw[1].startswith("MAG"):
            filtered_networks.append(ntw)
        elif network_type == "DEPOSITO" and ntw[1].startswith("ENT"):
            filtered_networks.append(ntw)
        elif network_type == "SRM" and (ntw[1].startswith("SRM") or ntw[1].startswith("RM")):
            filtered_networks.append(ntw)
        elif network_type == "FORNITORI" and ntw[1].startswith("FORN"):
            filtered_networks.append(ntw)
        elif network_type == "HQ" and ntw[1].startswith("HQ"):
            filtered_networks.append(ntw)
        elif network_type == "TUTTE":  # Non applico alcuna condizione
            filtered_networks.append(ntw)
        elif network_type == "SINGLE":  # Non applico alcuna condizione
            filtered_networks.append(ntw)
    #return valore convertito in JSON
    return jsonify(filtered_networks)

#Get Netwrok ID per @app.route
def get_networks_ID(orgID,network_type):
    networks = getNtwID_Name(URL, APIKEY, orgID)  # Recupera tutte le reti
    #Creo Array Network
    filtered_networks = []
    # Filtrare le reti in base al tipo selezionato
    for ntw in networks:
        #if network_type == "SINGLE_NTW" and ntw[1].startswith("SNI"):
        #    filtered_networks.append(ntw)
        if network_type == "SNIPER" and ntw[1].startswith("SNI"):
            filtered_networks.append(ntw)
        elif network_type == "NEGOZIO" and ntw[1].startswith("MAG"):
            filtered_networks.append(ntw)
        elif network_type == "DEPOSITO" and ntw[1].startswith("ENT"):
            filtered_networks.append(ntw)
        elif network_type == "SRM" and (ntw[1].startswith("SRM") or ntw[1].startswith("RM")):
            filtered_networks.append(ntw)
        elif network_type == "FORNITORI" and ntw[1].startswith("FORN"):
            filtered_networks.append(ntw)
        elif network_type == "HQ" and ntw[1].startswith("HQ"):
            filtered_networks.append(ntw)
        elif network_type == "TUTTE":  # Non applico alcuna condizione
            filtered_networks.append(ntw)
        elif network_type == "SINGLE":  # Non applico alcuna condizione
            filtered_networks.append(ntw)
    #return valore convertito in JSON
    return filtered_networks
