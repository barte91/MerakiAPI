import os
import requests,json
from config import URL,APIKEY

# FUNZIONI FILE - JSON

def ReadJSON(json_file):
        with open(json_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

def getJsonField(data, field):
        data_field=data.get(field)
        return data_field

#Invia dati nel JSON tramite API a Meraki - Method PUT
def UpdateJsonData(request_url,data_json):
    response = requests.put(request_url,headers=APIKEY, json=data_json)
    return response

#Invia dati nel JSON tramite API a Meraki - Method PUT
def Flask_POST_Generic(request_url,APIKEY,data_json):
    response = requests.post(request_url,headers=APIKEY, json=data_json)
    return response

