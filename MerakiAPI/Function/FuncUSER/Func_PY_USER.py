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
    Restituisce la lista di switch presenti in una network.  
    Args:
        ntwID (str): ID della network Meraki
    Returns:
        list[dict]: lista di switch con serial e name
    """
    try:
        # Chiama la funzione già esistente in FuncMeraki
        switches = FuncMeraki.API_GetSwByNtwID(ntwID)  # ritorna lista di tuple (id, nome)
        # Converti in lista di dizionari per uniformità JSON
        switch_list = []
        for sw in switches:
            switch_list.append({
                "serial": sw[0],
                "name": sw[1],
                "network_name": network_name,
                "tags": sw.get("tags","")
            })
        return switch_list
    except Exception as e:
        print(f"Errore in get_ListSwitch_byNtwID per network {ntwID}: {e}")
        return []

def get_Allswitch_by_NtwType(ListNtw):
    """
    Restituisce la lista di switch presenti nel network Type  
    Args:
        ListNtw (dict): ListaNetwork by NtwType
    Returns:
        all_switches (dict): Lista switch compresa di Network Name 
    """
    for ntw in ListNtw:
        if isinstance(ntw, tuple):
            ntwID = ntw[0]
            ntwName = ntw[1]
        else:
            ntwID = ntw
            # Recupera il nome network dal dashboard
            ntwName = FuncMeraki.getNtwNameByID(ntwID)
        switches = get_ListSwitch_byNtwID(ntwID)
        for sw in switches:
            sw['network_name'] = ntwName  # aggiunge il nome della network allo switch
        all_switches.extend(switches)
    return all_switches

import csv
from config import xls_path  # percorso dove salvare il CSV
from Function.FuncMeraki import DashboardAPI  # o importa la tua istanza Meraki

def export_switch_ports_to_csv(switch_list, filename="SwitchPorts.csv"):
    """
    Genera un CSV con tutte le porte degli switch selezionati.
    Args:
        switch_list (list[dict]): lista di switch, es: [{"serial": "...", "name": "...", "network_name": "...", "tags": "..."}]
        filename (str): nome del file CSV da salvare
    """
    # Percorso completo del file
    file_path = f"{xls_path}/{filename}"
    # Intestazioni CSV
    headers = ["NomeNetwork", "NomeSwitch", "SerialeSwitch", "TAGSwitch", "NumeroPorta", "DescrizionePorta"]
    with open(file_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for sw in switch_list:
            serial = sw.get("serial")
            switch_name = sw.get("name")
            network_name = sw.get("network_name", "")
            tag = sw.get("tags", "")
            # Ottieni le porte dello switch tramite Meraki API
            try:
                ports=FuncMeraki.getDeviceSwitchPortsBySerial(serial)
                # ports è una lista di dizionari
                for port in ports:
                    writer.writerow({
                        "NomeNetwork": network_name,
                        "NomeSwitch": switch_name,
                        "SerialeSwitch": serial,
                        "TAGSwitch": tag,
                        "NumeroPorta": port.get("portId"),
                        "DescrizionePorta": port.get("name")
                    })
            except Exception as e:
                print(f"Errore ottenendo porte dello switch {serial}: {e}")
    print(f"CSV generato correttamente in {file_path}")
    return file_path