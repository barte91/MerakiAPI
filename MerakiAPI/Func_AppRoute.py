from flask import jsonify, request
from Inventario import *
from UpdatePorts import *
from ChangeIP import *
from Tools import *
from MerakiAPIFlask import *

#def get_ssid_settings_by_number(ntwID, ssidNumber):
#    orgID = request.args.get('orgID')  # Assicurati di ottenere l'ID dell'organizzazione
#    ssid_settings = Flask_getSSID_Num_Name(URL, APIKEY, orgID, ntwID)  # Ottieni tutte le impostazioni SSID per la rete
    # Filtra per trovare l'SSID specificato dal numero
#    for ssid in ssid_settings:
#        if ssid['number'] == ssidNumber:
#            return jsonify(ssid)
#    return jsonify({"error": "SSID non trovato"}), 404
