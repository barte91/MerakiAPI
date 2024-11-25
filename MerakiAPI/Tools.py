import os
import requests,json,openpyxl,pandas as pd, os
from openpyxl import load_workbook
import meraki


# MERAKI API - ORGANIZATION

## ORG - GET

def getOrgID_Name(URL,APIKEY):
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

def UpdateSSID(URL,APIKEY,ntwID,ssid_number,data_json):
    queryURL = URL + f"/networks/{ntwID}/wireless/ssids/{ssid_number}"
    response = requests.put(
        queryURL,headers=APIKEY, json=data_json)
        #headers={
        #"Content-Type": "application/json",
        #"Authorization": f"Bearer {APIKEY}"
        #},
        #json=data_json
        #)
    return response


# FUNZIONI ITERAZIONE CON UTENTE

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

# FUNZIONI SU SISTEMA WINDOWS

def getFileName(total_path):
    list_fn=[]
    for path in os.listdir(total_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(total_path, path)):
            list_fn.append(path)
    return list_fn


# FUNZIONI FILE - JSON

def ReadJSON(json_file):
        with open(json_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

def getJsonField(data, field):
        data_field=data.get(field)
        return data_field

# FUNZIONI COMPLESSE

def CreateSSID(URL, APIKEY, json_script_path, orgID, selected_ssid_json,ntwType):
    SSID_path = "SSID"
    json_script_path = os.path.join(json_script_path, SSID_path)

    #ntwID = network_type.get('ID')
    # Converti il JSON string in un oggetto Python
    ssid_data = json.loads(selected_ssid_json)  # Assicurati di importare json in cima al tuo file

    # Se desideri, puoi anche fare controlli qui sul contenuto del JSON
    if 'number' in ssid_data:
        ssid_number = ssid_data['number']
        ssid_data.pop('number', None)  # Rimuovi 'number' se non necessario
    else:
        return {"error": "Il campo 'number' non è presente nel JSON."}

    # Salva il file JSON, se necessario
    #with open(os.path.join(json_script_path, 'SSID_to_create.json'), 'w', encoding='utf-8') as json_file:
    #    json.dump(ssid_data, json_file, indent=4, ensure_ascii=False)
    
    for ntwID, name in ntwType:
        # Esegui l'aggiornamento dell'SSID usando i dettagli ricevuti
        response = UpdateSSID(URL, APIKEY, ntwID, ssid_number, ssid_data)

    # Gestisci la risposta
    #if response.status_code == 200:
    #    return {"success": True, "message": "Aggiornamento riuscito!", "data": response.json()}
    #else:
    #    return {"error": response.status_code, "message": response.text}


    a=0

