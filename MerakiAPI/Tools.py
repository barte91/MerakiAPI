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

def CreateSSID(URL,APIKEY,json_script_path, orgID, ntwID):
    SSID_path= "SSID"
    json_script_path=os.path.join(json_script_path,SSID_path)
    PrintOrgID_Name(URL,APIKEY) # STAMPO LE ORGANIZATION CON I RELATIVIT ID
    orgID=AskOrgIDToUser()
    PrintNtwID_Name(URL,APIKEY,orgID) # STAMPO LE NETWORK CON I RELATIVIT ID
    ntwID=AskNtwIDToUser()
    Save_SSID_JSON(URL,APIKEY,orgID,ntwID, json_script_path) # SALVO IL FILE JSON IN \\192.168.100.65\Archivio Tecnico\Meraki API\SCRIPT\JSON\SSID
    PrintSSID_Num_Name(URL,APIKEY,orgID,ntwID)  # STAMPO SSID CON I RELATIVIT NUMBER
    
    #Richiedo il file JSON da utilizzare - Quello che screiverà i dati
    list_fn=getFileName(json_script_path)
    fn = list_fn[0]  # Qui potresti voler selezionare un file specifico o personalizzare ulteriormente
    json_input_path = os.path.join(json_script_path, fn)
    data_json = ReadJSON(json_input_path)  # Leggi i dati dal file JSON

    ssid_number= getJsonField(data_json, "number")
    data_json.pop("number", None)  # Rimuovi il campo 'number' dal JSON da inviare (non necessario per l'API PUT)

    response=UpdateSSID(URL,APIKEY,ntwID,ssid_number,data_json)
    # Gestisci la risposta
    if response.status_code == 200:
       print("Aggiornamento riuscito!")
       print("Risposta:", response.json())
    else:
       print(f"Errore: {response.status_code}")
       print("Messaggio:", response.text)


    a=0

