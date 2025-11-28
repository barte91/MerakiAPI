from flask import jsonify, request
from config import URL,APIKEY, xls_path
import requests,json,csv
from Function.FuncMeraki import Func_PY_Meraki as FuncMeraki
from Function.FuncJSON import Func_PY_JSON as FuncJSON

#Get Netwrok per @app.route
def get_networks(orgID):
    network_type = request.args.get('type')
    try:
        #networks = FuncMeraki.getNtwID_Name(URL, APIKEY, orgID)  # Recupera tutte le reti
        networks = FuncMeraki.API_GetOrgNetworks(orgID) # Recupera tutte le reti
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
    networks = FuncMeraki.getNtwID_Name(URL, APIKEY, orgID)  # Recupera tutte le reti
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
        #elif network_type == "SINGLE":  # Non applico alcuna condizione
        #   filtered_networks.append(ntw)
    #return valore convertito in JSON
    return filtered_networks

# FUNZIONE GET - API GENERIC @app.route

def get_APIgeneric( queryURL):
    response = requests.get(queryURL, headers=APIKEY)
    #response = requests.request("GET", queryURL, headers=APIKEY)
    if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        data=response.text
        return data  # Restituisci direttamente i dettagli SSID
    else:
        return {"error": response.status_code, "message": response.text}


def AskOrgIDToUser(): #RICHIEDO ID ORG A UTENTE
    orgName=input("Digitare ID organization desiderata: ")
    return orgName

def AskNtwIDToUser(): #RICHIEDO NOME NETWORK A UTENTE
    ntwName=input("Digitare la network desiderata (scrivi ALL per tutte): ")
    return ntwName

def AskFileName(list_fn):
    #print("Selezionare Network")
    print(*list_fn, sep = "\n")
    fn=input("Digitare il nome del file: ")
    return fn

#ButtonApplyMod - EX CreateSSID
def ButtonApplyMod(req_url, json_data, ListNtw, ntwType):
    if ntwType == "SINGLE":    
        ntwID=ListNtw
        response = FuncJSON.UpdateJsonData(req_url, json_data)
    #Altrimenti passo la list di tutte le reti facenti parte del Tipo selezionato
    else:
        for ntwID, name in ListNtw:
            # Esegui l'aggiornamento dell'SSID usando i dettagli ricevuti
            response = FuncJSON.UpdateJsonData(req_url, json_data)

def get_ListSwitch_by_NtwID(ntwID):
    """
    Restituisce la lista di switch presenti in una singola network Meraki.
    
    Args:
        ntwID (str): ID della network Meraki
    
    Returns:
        list[dict]: lista di switch con serial, name, model, lanIp, network_name e tags
    """
    switch_list = []
    try:
        switches = FuncMeraki.API_GetSwByNtwID(ntwID)  # tutti i dispositivi della network
        network_name = FuncMeraki.getNtwNameByID(ntwID)       # chiamiamo solo una volta per network

        for serial, name in switches:
            sw_detail = FuncMeraki.get_SwitchDetails_by_Serial(serial)
            if sw_detail and sw_detail["model"].startswith("MS"):
                sw_detail["network_name"] = network_name
                switch_list.append(sw_detail)

    except Exception as e:
        print(f"Errore elaborando switch in network {ntwID}: {e}")

    return switch_list


def get_Allswitch_by_NtwType(ListNtw):
    """
    Restituisce la lista di switch per un tipo di network (più network).
    
    Args:
        ListNtw (list[str]): Lista di network ID appartenenti allo stesso tipo
    
    Returns:
        list[dict]: Lista di switch compresa di Network Name
    """
    all_switches = []
    for ntwID in ListNtw:
        switches = get_ListSwitch_by_NtwID(ntwID)
        all_switches.extend(switches)



