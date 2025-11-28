import os
import requests,json,openpyxl,pandas as pd, os
import meraki
from config import URL,KEY,APIKEY

# MERAKI API - ORGANIZATION

## ORG - GET

def getOrgID_Name():
    """Fetch the list of organizations for the authenticated user."""
    queryURL = f'{URL}/organizations'
    response = requests.get(queryURL, headers=APIKEY)
    if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        organizations = response.json()
        # Stampa ID e Nome delle organizzazioni
        for org in organizations:
            return [(org['id'], org['name']) for org in organizations]

def Flask_getOrgID_Name(URL,APIKEY):
    """Fetch the list of organizations for the authenticated user."""
    queryURL = f'{URL}/organizations'
    response = requests.get(queryURL, headers=APIKEY)
    if response.status_code == 200:
        organizations = response.json()
        return [(org['id'], org['name']) for org in organizations]
    else:
        return []

## ORG - PRINT

def PrintOrgID_Name(URL,APIKEY):
    org = getOrgID_Name(URL,APIKEY)
    if org: # Se org non è None e ha risultati
        for org_id, org_name in org:
            print(f"\tNome: {org_name},\n\tID:{org_id}\n")     

# MERAKI API - NETWORK

## NETWORK - GET
def getNtwID_Name(URL,APIKEY,orgID):
    queryURL = URL + f"/organizations/{orgID}/networks"
    response = requests.get(queryURL, headers=APIKEY)
    if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        networks = response.json()
        # Stampa ID e Nome delle organizzazioni
        for ntw in networks:
            return [(ntw['id'], ntw['name']) for ntw in networks]

def Flask_getNtwID_Name(URL, APIKEY, orgID):
    queryURL = URL + f"/organizations/{orgID}/networks"
    response = requests.get(queryURL, headers=APIKEY)
    if response.status_code == 200:
        networks = response.json()
        return [(ntw['id'], ntw['name']) for ntw in networks]
    else:
        return []

## NETWORK - PRINT

def PrintNtwID_Name(URL,APIKEY,orgID):
    ntw = getNtwID_Name(URL,APIKEY,orgID)
    if ntw: # Se org non è None e ha risultati
        for ntw_id, ntw_name in ntw:
            print(f"\tNome: {ntw_name},\n\tID:{ntw_id}\n")
            

# MERAKI - API -GENERALIZZATE

## GET

def Flask_get_Generic(queryURL,col1,col2):
    response = requests.get(queryURL, headers=APIKEY)
    if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        data = response.json()
        return data
        # Stampa ID e Nome delle organizzazioni
        #for d in data:
        #    return [(d[col2], d[col1]) for d in data]
        #return data  # Restituisci direttamente i dettagli SSID
    else:
        return {"error": response.status_code, "message": response.text}

"""
def Flask_get_Generic_old( queryURL):
    response = requests.get(queryURL, headers=APIKEY)
    if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        data = response.json()
        return data  # Restituisci direttamente i dettagli SSID
    else:
        return {"error": response.status_code, "message": response.text}
"""

def Flask_extractDataGeneric(data):
        for d in data:
            return [(d[0], d[1]) for d in data]
# MERAKI API - SSID

## SSID - GET

def getSSID_Num_Name(URL,APIKEY,orgID,ntwID):
    queryURL = URL + f"/networks/{ntwID}/wireless/ssids"
    response = requests.get(queryURL, headers=APIKEY)
    if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        ssids = response.json()

        # Stampa number e Nome delle ssids
        for ssid in ssids:
            return [(ssid['number'], ssid['name']) for ssid in ssids]

def Flask_getSSID_Num_Name(URL, APIKEY, orgID, ntwID):
    queryURL = URL + f"/networks/{ntwID}/wireless/ssids"
    response = requests.get(queryURL, headers=APIKEY)
    if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        ssids = response.json()
        return ssids  # Restituisci direttamente i dettagli SSID
    else:
        return {"error": response.status_code, "message": response.text}

def Flask_getSSID_Num_Name_By_NumberSSID(URL, APIKEY, orgID, ntwID,ssidNumber):
    queryURL = URL + f"/networks/{ntwID}/wireless/ssids/{ssidNumber}"
    response = requests.get(queryURL, headers=APIKEY)
    if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        ssids = response.json()
        return ssids  # Restituisci direttamente i dettagli SSID
    else:
        return {"error": response.status_code, "message": response.text}


## SSID - SAVE

def Save_SSID_JSON(URL,APIKEY,orgID,ntwID,json_path):
    queryURL = URL + f"/networks/{ntwID}/wireless/ssids"
    response = requests.get(queryURL, headers=APIKEY)
    if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        ssids = response.json()

        #Salvo il file JSON
        json_path=os.path.join(json_path,"Template-SSID.json")
        if json_path:
               with open(json_path, 'w', encoding='utf-8') as json_file:
                    json.dump(ssids, json_file, indent=4, ensure_ascii=False)


## SSID - PRINT

def PrintSSID_Num_Name(URL,APIKEY,orgID,ntwID):
    ssid = getSSID_Num_Name(URL,APIKEY,orgID,ntwID)
    if ssid: # Se org non è None e ha risultati
        for ssid_num, ssid_name in ssid:
            print(f"\tNome: {ssid_name},\n\tNUMBER: {ssid_num}\n")


## SSID - PUT (PDATE)

def UpdateSSID(request_url,APIKEY,data_json):
    #queryURL = URL + f"/networks/{ntwID}/wireless/ssids/{ssid_number}"
    response = requests.put(
        request_url,headers=APIKEY, json=data_json)
        #headers={
        #"Content-Type": "application/json",
        #"Authorization": f"Bearer {APIKEY}"
        #},
        #json=data_json
        #)
    return response

######## MERAKI API DIRETTE #################

def API_UpdateSSID(request_url,data_json,ntwId):
    dashboard=meraki.DashboardAPI(KEY)
    number=data_json['number']
    response = dashboard.wireless.updateNetworkWirelessSsid(ntwId, **data_json)

def API_GetOrgNetworks(orgID):
    dashboard=meraki.DashboardAPI(KEY)
    response = dashboard.organizations.getOrganizationNetworks(orgID)
    #if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        #organizations = response.json()
        # Stampa ID e Nome delle organizzazioni
    # Crea una lista di tuple (ID, Nome)
    orgs = [(org['id'], org['name']) for org in response]
    # Ordina la lista in base al nome dell'organizzazione
    orgs_sorted = sorted(orgs, key=lambda x: x[1])
    return orgs_sorted
    #for org in response:
    #    return [(org['id'], org['name']) for org in response]
 
## API - VARIE
#
def API_GetSwByNtwID(ntwID):
    """
    Restituisce tutti gli switch di una network Meraki.
    Args:
        ntwID (str): ID della network Meraki
    Returns:
        list[tuple]: lista di tuple (serial, name)
    """
    try:
        dashboard = meraki.DashboardAPI(KEY)
        devices = dashboard.networks.getNetworkDevices(ntwID)  # ottieni tutti i dispositivi della network
        # Filtra solo gli switch
        sw = [(d['serial'], d['name']) for d in devices if d['model'].startswith('MS')]  # MS = Meraki Switch
        # Ordina per nome
        ListSw = sorted(sw, key=lambda x: x[1])
        return ListSw
    except Exception as e:
        print(f"Errore in API_GetSwByNtwID per network {ntwID}: {e}")
        return []   
    
## PORTS - GET

def GetSwPorts():
    a=0
