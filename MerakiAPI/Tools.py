import os
import requests,json,openpyxl,pandas as pd, os
from openpyxl import load_workbook
from config import URL,APIKEY
import meraki
from Function.FuncGLPI.Func_PY_GLPI import *
from Function.FuncDB.Func_PY_DB import *





# FUNZIONI ITERAZIONE CON UTENTE









# FUNZIONI FILE - JSON



# FUNZIONI COMPLESSE










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