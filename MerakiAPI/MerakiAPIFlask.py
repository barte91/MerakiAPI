from flask import Flask, jsonify, render_template, request, send_from_directory, send_file
from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem
import os
from config import URL,APIKEY
from Inventario import *
from UpdatePorts import *
from ChangeIP import *
from Tools import *
from Func_AppRoute import *
from Function.FuncGLPI.Func_PY_GLPI import *
from Function.FuncDB.Func_PY_DB import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#@app.route('/templates/<path:filename>')
#def send_js(filename):
#    return send_from_directory('static', filename)


######### PAGINA - inventario_by_org
#@app.route('/api/inventario_by_org')
#def inventario_by_org():
#    result = get_invetario(URL, APIKEY, orgID, xls_path_inv)
#    return jsonify(result)



###### PAGINA - inventario_by_ntw
#@app.route('/api/inventario_by_ntw')
#def inventario_by_ntw():
#    result = get_invetarioByNetwork(URL, APIKEY, orgID, xls_path_inv)
#    return jsonify(result)


######### PAGINA - update_ports_by_file_ntw
#@app.route('/api/update_ports_by_file_ntw')
#def update_ports_by_file_ntw():
#    result = set_UpdateportsByFile_and_NwName(URL, APIKEY, orgID, xls_path)
#    return jsonify(result)

######### PAGINA - v2_template_update_ports_by_file_ntw
#@app.route('/api/v2_template_update_ports_by_file_ntw')
#def v2_template_update_ports_by_file_ntw():
#    result = set_V2_UpdateportsByFile_and_NwName_withTemplate(URL, APIKEY, orgID, xls_path)
#    return jsonify(result)

######### PAGINA - update_ports_by_file
#@app.route('/api/update_ports_by_file')
#def update_ports_by_file():
#    result = set_UpdateportsByFile(URL, APIKEY, orgID, xls_path)
#    return jsonify(result)

######### PAGINA - change_ip_by_file
#@app.route('/api/change_ip_by_file')
#def change_ip_by_file():
#    result = set_ChangeIP_ByFile(URL, APIKEY, orgID, xls_path_chgIP)
#    return jsonify(result)

###### PAGINA - API - SSID
@app.route('/api/API-SSID', methods=['GET', 'POST'])
def API_SSID():
    json_output = None
    if request.method == 'POST':
        orgID = request.form['orgID']
        ntwID = request.form['ntwID']
        pkey='number'
        #modification_type = request.form['ModifynetworkType']  # Ottieni il valore da ModificationType
        selected_ntwtype = request.form['networkType']
        if selected_ntwtype == "SINGLE": # se la network selezionata è "SINGOLA NETWORK faccio la modifica solo sulla rete selezioanata, else su tutte le reti facenti parte del type
            ListNtw = request.form['ntwID']
        else:
            # Ottieni i network filtrati chiamando get_networks - tutte le network facenti parte del ntwType
            ListNtw = get_networks_ID(orgID,selected_ntwtype)
        modify_json = request.form['ModifyJson']  # Ottieni il JSON inviato
        #json_script_path = r"\\192.168.100.65\Archivio Tecnico\Meraki API\SCRIPT\JSON"

        # Converti il JSON string in un oggetto Python
        json_data = json.loads(modify_json)  # Assicurati di importare json in cima al tuo file
        json_value_pkey = json_data[pkey]
        
        #Chiamata per fare Update DATA
        if selected_ntwtype == "SINGLE":    
            ntwID=ListNtw
            request_url=URL + f"/networks/{ntwID}/wireless/ssids/{json_value_pkey}"
            json_output = UpdateJsonData(request_url, json_data)
        #Altrimenti passo la list di tutte le reti facenti parte del Tipo selezionato
        else:
            for ntwID, name in ListNtw:
                # Esegui l'aggiornamento dell'SSID usando i dettagli ricevuti
                request_url=URL + f"/networks/{ntwID}/wireless/ssids/{json_value_pkey}"
                json_output = UpdateJsonData(request_url, json_data)

        # Chiamata alla funzione CreateSSID e memorizza il risultato
        #json_output = ButtonApplyMod(request_url, json_data, ListNtw, selected_ntwtype)

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    organizations = getOrgID_Name()
    return render_template('API-SSID.html', organizations=organizations, json_output=json_output)

###### --------- INIZIO --- FUNZIONI-PAGINA - API - SSID

### - FUNZIONE GENERALE GET NETWORKS
@app.route('/api/get_networks/<orgID>')
def get_networks_endpoint(orgID):
    #return valore della funzione get_networks in Func_AppRoute.py
    return get_networks(orgID)

def get_networks_ID_endpoint(orgID,network_type):
    #return valore della funzione get_networks in Func_AppRoute.py
    return get_networks_ID(orgID,network_type)

### - FUNZIONE GENERALE GET SWITCHES
@app.route('/api/get_switches/<ntwID>')
def get_generic_endpoint(ntwID):
    request_url=URL + f"/networks/{ntwID}/devices"
    #return valore della funzione get_networks in Func_AppRoute.py
    ntwDev=get_APIgeneric(request_url)
    ntwDev=FilterListNtwDev(ntwDev,'name','serial','switch','model')
    ntwDev=Add_ListElement(ntwDev,'serial','name','ALL','ALL')
    return ntwDev


#@app.route('/api/get_ssid_settings/<ntwID>')
#def get_ssid_settings(ntwID):
#    ssid_settings = Flask_getSSID_Num_Name(URL, APIKEY, orgID, ntwID)  
#    return jsonify(ssid_settings)

#@app.route('/api/get_ssid_settings/<ntwID>/<ssidNumber>')
#def get_ssid_settingsByNumber(ntwID,ssidNumber):
#    ssid_settings = Flask_getSSID_Num_Name_By_NumberSSID(URL, APIKEY, orgID, ntwID,ssidNumber)
#    return jsonify(ssid_settings)



#@app.route('/api/get_ssid_settings/<ntwID>')
#def get_ssid_settings(ntwID):
#    request_url=URL + f"/networks/{ntwID}/wireless/ssids/"
#    data=get_APIgeneric(request_url,'number','name','nofilter','nofilter')
#    ssid_settings = Flask_extractDataGeneric(data)
#    a=jsonify(ssid_settings)
#    return jsonify(ssid_settings)

#@app.route('/api/get_ssid_settings/<ntwID>/<ssidNumber>')
#def get_ssid_settingsByNumber(ntwID,ssidNumber):
#    request_url=URL + f"/networks/{ntwID}/wireless/ssids/{ssidNumber}"
#    data=get_APIgeneric(request_url,'number','name','nofilter','nofilter')
#    ssid_settings=Flask_extractDataGeneric(data)
#    return jsonify(ssid_settings)

@app.route('/api/get_ssid_settings/<ntwID>')
def get_ssid_settings(ntwID):
    request_url=URL + f"/networks/{ntwID}/wireless/ssids/"
    ssid_data = get_APIgeneric(request_url) 
    return jsonify(ssid_data)

@app.route('/api/get_ssid_settings/<ntwID>/<ssidNumber>')
def get_ssid_settingsByNumber(ntwID,ssidNumber):
    request_url=URL + f"/networks/{ntwID}/wireless/ssids/{ssidNumber}"
    ssid_data=get_APIgeneric(request_url)
    return jsonify(ssid_data)


#@app.route('/download_json/<ntwID>/<ssidNumber>', methods=['GET'])
#def download_json(ntwID,ssidNumber):
#    ssid_settings = Flask_getSSID_Num_Name_By_NumberSSID(URL, APIKEY, orgID, ntwID,ssidNumber)
#    return jsonify(ssid_settings)
###### --------- FINE --- FUNZIONI-PAGINA - API - SSID

###### PAGINA - API - RADIO PROFILE
@app.route('/api/API-RadioProfile', methods=['GET', 'POST'])
def API_RadioProfile():
    json_output = None
    if request.method == 'POST':
        orgID = request.form['orgID']
        ntwID = request.form['ntwID']
        pkey='id'
        #modification_type = request.form['ModifynetworkType']  # Ottieni il valore da ModificationType
        selected_ntwtype = request.form['networkType']
        if selected_ntwtype == "SINGLE": # se la network selezionata è "SINGOLA NETWORK faccio la modifica solo sulla rete selezioanata, else su tutte le reti facenti parte del type
            ListNtw = request.form['ntwID']
        else:
            # Ottieni i network filtrati chiamando get_networks - tutte le network facenti parte del ntwType
            ListNtw = get_networks_ID(orgID,selected_ntwtype)
        modify_json = request.form['ModifyJson']  # Ottieni il JSON inviato
        #json_script_path = r"\\192.168.100.65\Archivio Tecnico\Meraki API\SCRIPT\JSON"

        # Converti il JSON string in un oggetto Python
        json_data = json.loads(modify_json)  # Assicurati di importare json in cima al tuo file
        json_value_pkey = json_data[pkey]

        #Chiamata per fare Update DATA
        if selected_ntwtype == "SINGLE":    
            ntwID=ListNtw
            request_url=URL + f"/networks/{ntwID}/wireless/rfProfiles/{json_value_pkey}"
            json_output = UpdateJsonData(request_url, json_data)
        #Altrimenti passo la list di tutte le reti facenti parte del Tipo selezionato
        else:
            for ntwID, name in ListNtw:
                # Esegui l'aggiornamento dell'SSID usando i dettagli ricevuti
                request_url=URL + f"/networks/{ntwID}/wireless/rfProfiles/{json_value_pkey}"
                json_output = UpdateJsonData(request_url, json_data)

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    organizations = getOrgID_Name()
    return render_template('API-RadioProfile.html', organizations=organizations, json_output=json_output)

@app.route('/api/get_rf_settings/<ntwID>')
def get_rf_settings(ntwID):
    request_url=URL + f"/networks/{ntwID}/wireless/rfProfiles"
    rf_data = get_APIgeneric(request_url) 
    return jsonify(rf_data)

@app.route('/api/get_rf_settings/<ntwID>/<rfID>')
def get_rf_settingsByNumber(ntwID,rfID):
    request_url=URL + f"/networks/{ntwID}/wireless/rfProfiles/{rfID}"
    rf_data=get_APIgeneric(request_url)
    return jsonify(rf_data)

@app.route('/api/post_rf_profiles/<ntwID>', methods=['POST'])
def POST_rf_profiles(ntwID):
    # Recupera il JSON inviato nel corpo della richiesta
    json_data = request.get_json()
    request_url = f"{URL}/networks/{ntwID}/wireless/rfProfiles"  # URL per creare un nuovo RF Profile
    response = Flask_POST_Generic(request_url, APIKEY, json_data)  # Funzione per inviare una richiesta POST
    # Controlla il codice di stato della risposta
    if response.status_code in (200, 201):
        return jsonify(response.json())  # Restituisce i dati della risposta come JSON
    else:
        return jsonify({"error": response.status_code, "message": response.text}), response.status_code  # Restituisce errore con il codice di stato

###### PAGINA - Port Donw Meraki
@app.route('/api/API-PortDown', methods=['GET', 'POST'])
def PortDownMeraki():
    json_output = None
    if request.method == 'POST':
        orgID = request.form['orgID']
        ntwID = request.form['ntwID']
        pkey='id'
        #modification_type = request.form['ModifynetworkType']  # Ottieni il valore da ModificationType
        selected_ntwtype = request.form['networkType']
        if selected_ntwtype == "SINGLE": # se la network selezionata è "SINGOLA NETWORK faccio la modifica solo sulla rete selezioanata, else su tutte le reti facenti parte del type
            ListNtw = request.form['ntwID']
        else:
            # Ottieni i network filtrati chiamando get_networks - tutte le network facenti parte del ntwType
            ListNtw = get_networks_ID(orgID,selected_ntwtype)
        #modify_json = request.form['ModifyJson']  # Ottieni il JSON inviato
        #json_script_path = r"\\192.168.100.65\Archivio Tecnico\Meraki API\SCRIPT\JSON"

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    organizations = getOrgID_Name()
    return render_template('API-PortDown.html', organizations=organizations)

@app.route('/api/get_ports_down', methods=['GET'])
def get_ports_down():
    down_ports = GetSwPorts()  # Funzione che recupera i dati richiesti
    return jsonify(down_ports)

###### PAGINA - API - GLPI INVENTARIO
@app.route('/api/GLPI-InveManu', methods=['GET', 'POST'])
def GLPI_INVE_MANU():
    if request.method == 'POST':
        entID = request.form['entID']
        negoID = request.form['negoID']
        List_states = request.form['statesSelect']
        #Chiama funzione di Func_PY_GLPI.py
        result_path=APP_GLPI_InveManu(entID,negoID,List_states)
        try:
            #Crea richiesta per download file
            response=send_file(result_path, as_attachment=True)
            # Ritardo di 100 millisecondi
            time.sleep(0.1)  
        finally:
            #Blocco per eliminare il file creato dal server
            try:
                os.remove(result_path)
            except Exception as e:
                print(f"Errore durante la rimozione del file: {e}")  # Log dell'errore
        return response

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    entities = fetch_Settings_GLPI(" SELECT * FROM glpi_entities",1,0)
    states = fetch_Settings_GLPI("SELECT * FROM glpi_states",1,0)
    return render_template('API-GLPI-InveManu.html', entities=entities, states=states)

@app.route ('/fetch_glpi_locations/<entID>', methods=['GET'])
def get_glpi_locations(entID):
    query='SELECT * FROM glpi_locations WHERE entities_id=' + entID
    return CopiaCampiDB(query,3,0)


@app.route('/api/test')
def test():
    result = CreateSSID(URL, APIKEY, json_script_path)  # Puoi modificare il comportamento se necessario
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
