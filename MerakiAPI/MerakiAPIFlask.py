from flask import Flask, jsonify, render_template, request
from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem
from Inventario import *
from UpdatePorts import *
from ChangeIP import *
from Tools import *

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
        json_script_path = r"\\192.168.100.65\Archivio Tecnico\Meraki API\SCRIPT\JSON"

        # Chiamata alla funzione CreateSSID e memorizza il risultato
        json_output = CreateSSID(URL, APIKEY, json_script_path, orgID, ntwID)

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    organizations = getOrgID_Name(URL, APIKEY)
    return render_template('create_ssid.html', organizations=organizations, json_output=json_output)

@app.route('/api/get_networks/<orgID>', methods=['GET'])
def get_networks(orgID):
    networks = Flask_getNtwID_Name(URL, APIKEY, orgID)  # Ottieni le reti per l'organizzazione selezionata
    return jsonify(networks)  # Restituisce un JSON con le reti

@app.route('/api/get_ssid_settings/<ntwID>')
def get_ssid_settings(ntwID):
    ssid_settings = Flask_getSSID_Num_Name(URL, APIKEY, orgID, ntwID)  # Assicurati di avere orgID disponibile
    return jsonify(ssid_settings)

@app.route('/api/test')
def test():
    result = CreateSSID(URL, APIKEY, json_script_path)  # Puoi modificare il comportamento se necessario
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
