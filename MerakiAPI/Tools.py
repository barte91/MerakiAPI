import os
import requests,json,openpyxl,pandas as pd, os
from openpyxl import load_workbook
from config import URL,APIKEY
import meraki


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


## PORTS - GET

def GetSwPorts():
    a=0


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

# FUNZIONI SU LIST-DICT-TUPLE

def FilterListNtwDev(data,col1,col2,filter_param,filter_col):
    # Filtra i dati per switch se richiesto
    filtered_data = []
    for d in data:
        if filter_param == 'switch' and d.get(filter_col) and d[filter_col].startswith('MS'):
            #filtered_data.append((d[col1], d[col2]))
            filtered_data.append(d)
        if filter_param == 'ap' and d.get(filter_col) and d[filter_col].startswith('MR'):
            #filtered_data.append((d[col1], d[col2]))
            filtered_data.append(d)
        if filter_param == 'nofilter':
            #filtered_data.append((d[col1], d[col2]))
            filtered_data.append(d)
    return filtered_data  # Restituisce le porte filtrate

def Add_ListElement(list,primary_key,secondary_key,primary_key_value,secondary_key_value):
    addElement={primary_key: primary_key_value, secondary_key: secondary_key_value }
    list.append(addElement)
    return list


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

#ButtonApplyMod - EX CreateSSID
def ButtonApplyMod(req_url, json_data, ListNtw, ntwType):
    if ntwType == "SINGLE":    
        ntwID=ListNtw
        response = UpdateJsonData(req_url, json_data)
    #Altrimenti passo la list di tutte le reti facenti parte del Tipo selezionato
    else:
        for ntwID, name in ListNtw:
            # Esegui l'aggiornamento dell'SSID usando i dettagli ricevuti
            response = UpdateJsonData(req_url, json_data)



#Invia dati nel JSON tramite API a Meraki - Method PUT
def UpdateJsonData(request_url,data_json):
    response = requests.put(request_url,headers=APIKEY, json=data_json)
    return response

#Invia dati nel JSON tramite API a Meraki - Method PUT
def Flask_POST_Generic(request_url,APIKEY,data_json):
    response = requests.post(request_url,headers=APIKEY, json=data_json)
    return response

# FUNZIONI VARIE UNUSED - SOLO SCOPO DIDATTICO

    #SSID_path = "SSID"
    #json_script_path = os.path.join(json_script_path, SSID_path)

    #ntwID = network_type.get('ID')
    # Converti il JSON string in un oggetto Python
    #json_data = json.loads(modify_json)  # Assicurati di importare json in cima al tuo file

    # Se desideri, puoi anche fare controlli qui sul contenuto del JSON
    #if 'number' in ssid_data:
    #    ssid_number = ssid_data['number']
    #    ssid_data.pop('number', None)  # Rimuovi 'number' se non necessario
    #else:
    #    return {"error": "Il campo 'number' non è presente nel JSON."}

    # Salva il file JSON, se necessario
    #with open(os.path.join(json_script_path, 'SSID_to_create.json'), 'w', encoding='utf-8') as json_file:
    #    json.dump(ssid_data, json_file, indent=4, ensure_ascii=False)
    #se abbiamo selezionato la singola rete allora passo ID della rete selezioanta

    # Gestisci la risposta
    #if response.status_code == 200:
    #    return {"success": True, "message": "Aggiornamento riuscito!", "data": response.json()}
    #else:
    #    return {"error": response.status_code, "message": response.text}