from flask import Flask, jsonify, render_template, request
from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem
from Inventario import *
from UpdatePorts import *
from ChangeIP import *
from Tools import *
from Func_AppRoute import *

app = Flask(__name__)

URL = "https://api.meraki.com/api/v1"  # URL MERKI API
APIKEY = {"X-Cisco-Meraki-API-Key": "f25d79a1df42dff69f5337fa61c60c2b798aa404"}  # API PER TECNOMAT
orgID = "280759"  # TECNOMAT ITALIA
xls_path_inv = "C:\\MerakiAPI\\IntToShutInv_"
xls_path_chgIP = "C:\\MerakiAPI\\ChangeIP"
xls_path = "C:\\MerakiAPI"
json_script_path = r"\\192.168.100.65\Archivio Tecnico\Meraki API\SCRIPT\JSON"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/inventario_by_org')
def inventario_by_org():
    result = get_invetario(URL, APIKEY, orgID, xls_path_inv)
    return jsonify(result)

@app.route('/api/inventario_by_ntw')
def inventario_by_ntw():
    result = get_invetarioByNetwork(URL, APIKEY, orgID, xls_path_inv)
    return jsonify(result)

@app.route('/api/update_ports_by_file_ntw')
def update_ports_by_file_ntw():
    result = set_UpdateportsByFile_and_NwName(URL, APIKEY, orgID, xls_path)
    return jsonify(result)

@app.route('/api/v2_template_update_ports_by_file_ntw')
def v2_template_update_ports_by_file_ntw():
    result = set_V2_UpdateportsByFile_and_NwName_withTemplate(URL, APIKEY, orgID, xls_path)
    return jsonify(result)

@app.route('/api/update_ports_by_file')
def update_ports_by_file():
    result = set_UpdateportsByFile(URL, APIKEY, orgID, xls_path)
    return jsonify(result)

@app.route('/api/change_ip_by_file')
def change_ip_by_file():
    result = set_ChangeIP_ByFile(URL, APIKEY, orgID, xls_path_chgIP)
    return jsonify(result)

@app.route('/api/create_ssid', methods=['GET', 'POST'])
def create_ssid():
    json_output = None
    if request.method == 'POST':
        orgID = request.form['orgID']
        ntwID = request.form['ntwID']
        #modification_type = request.form['ModifynetworkType']  # Ottieni il valore da ModificationType
        selected_ntwtype = request.form['networkType']
        if selected_ntwtype == "SINGLE": # se la network selezionata è "SINGOLA NETWORK faccio la modifica solo sulla rete selezioanata, else su tutte le reti facenti parte del type
            ListNtw = request.form['ntwID']
        else:
            # Ottieni i network filtrati chiamando get_networks - tutte le network facenti parte del ntwType
            ListNtw = get_networks_ID(orgID,selected_ntwtype)
        selected_ssid_json = request.form['selectedSSIDJson']  # Ottieni il JSON inviato
        json_script_path = r"\\192.168.100.65\Archivio Tecnico\Meraki API\SCRIPT\JSON"

        # Chiamata alla funzione CreateSSID e memorizza il risultato
        json_output = CreateSSID(URL, APIKEY, json_script_path, orgID, selected_ssid_json,ListNtw,selected_ntwtype)

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    organizations = getOrgID_Name(URL, APIKEY)
    return render_template('create_ssid.html', organizations=organizations, json_output=json_output)

@app.route('/api/get_networks/<orgID>')
def get_networks(orgID):
    network_type = request.args.get('type')
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
        elif network_type == "SRM" and ntw[1].startswith("SRM"):
            filtered_networks.append(ntw)
        elif network_type == "HQ" and ntw[1].startswith("HQ"):
            filtered_networks.append(ntw)
        elif network_type == "TUTTE":  # Non applico alcuna condizione
            filtered_networks.append(ntw)
        elif network_type == "SINGLE":  # Non applico alcuna condizione
            filtered_networks.append(ntw)
    #return valore convertito in JSON
    return jsonify(filtered_networks)

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
        elif network_type == "SRM" and ntw[1].startswith("SRM"):
            filtered_networks.append(ntw)
        elif network_type == "HQ" and ntw[1].startswith("HQ"):
            filtered_networks.append(ntw)
        elif network_type == "TUTTE":  # Non applico alcuna condizione
            filtered_networks.append(ntw)
    #return valore convertito in JSON
    return filtered_networks

@app.route('/api/get_ssid_settings/<ntwID>')
def get_ssid_settings(ntwID):
    ssid_settings = Flask_getSSID_Num_Name(URL, APIKEY, orgID, ntwID)  
    return jsonify(ssid_settings)

@app.route('/api/get_ssid_settings/<ntwID>/<ssidNumber>')
def get_ssid_settingsByNumber(ntwID,ssidNumber):
    ssid_settings = Flask_getSSID_Num_Name_By_NumberSSID(URL, APIKEY, orgID, ntwID,ssidNumber) 
    return jsonify(ssid_settings)

@app.route('/api/test')
def test():
    result = CreateSSID(URL, APIKEY, json_script_path)  # Puoi modificare il comportamento se necessario
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
