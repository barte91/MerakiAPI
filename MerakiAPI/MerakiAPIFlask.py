#Carica variabili con password
from dotenv import load_dotenv
load_dotenv()

from flask import Flask, jsonify, render_template, request, send_from_directory, send_file
from consolemenu import ConsoleMenu, SelectionMenu
from consolemenu.items import FunctionItem
import os,json,zipfile,io
from config import URL,APIKEY, InveManu_nameFile
from Inventario import *
from UpdatePorts import *
from ChangeIP import *
#from Tools import *
#from Func_AppRoute import *
from Function.FuncGLPI import Func_PY_GLPI as FuncGLPI
from Function.FuncDB import Func_PY_DB as FuncDB
from Function.FuncMeraki import Func_PY_Meraki as FuncMeraki
from Function.FuncJSON import Func_PY_JSON as FuncJSON
from Function.FuncUSER import Func_PY_USER as FuncUser
from Function.FuncMatrix import Func_PY_Matrix as FuncMatrix
from Function.FuncOS import Func_PY_OS as FuncOS
from Function.FuncFILE import Func_PY_FILE as FuncFILE

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
            ListNtw = FuncUser.get_networks_ID(orgID,selected_ntwtype)
        modify_json = request.form['ModifyJson']  # Ottieni il JSON inviato
        #json_script_path = r"JSON_PATH"

        # Converti il JSON string in un oggetto Python
        json_data = json.loads(modify_json)  # Assicurati di importare json in cima al tuo file
        json_value_pkey = json_data[pkey]
        
        #Chiamata per fare Update DATA
        if selected_ntwtype == "SINGLE":    
            ntwID=ListNtw
            request_url=URL + f"/networks/{ntwID}/wireless/ssids/{json_value_pkey}"
            #json_output = FuncJSON.UpdateJsonData(request_url, json_data)
            FuncMeraki.API_UpdateSSID(request_url, json_data,ntwID)
        #Altrimenti passo la list di tutte le reti facenti parte del Tipo selezionato
        else:
            for ntwID, name in ListNtw:
                # Esegui l'aggiornamento dell'SSID usando i dettagli ricevuti
                request_url=URL + f"/networks/{ntwID}/wireless/ssids/{json_value_pkey}"
                #json_output = FuncJSON.UpdateJsonData(request_url, json_data)
                FuncMeraki.API_UpdateSSID(request_url, json_data,ntwID)

        # Chiamata alla funzione CreateSSID e memorizza il risultato
        #json_output = ButtonApplyMod(request_url, json_data, ListNtw, selected_ntwtype)

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    organizations = FuncMeraki.getOrgID_Name()
    return render_template('API-SSID.html', organizations=organizations, json_output=json_output)

###### --------- INIZIO --- FUNZIONI-PAGINA - API - SSID

### - FUNZIONE GENERALE GET NETWORKS
@app.route('/api/get_networks/<orgID>')
def get_networks_endpoint(orgID):
    #return valore della funzione get_networks in Func_AppRoute.py
    return FuncUser.get_networks(orgID)

def get_networks_ID_endpoint(orgID,network_type):
    #return valore della funzione get_networks in Func_AppRoute.py
    return FuncUser.get_networks_ID(orgID,network_type)

### - FUNZIONE GENERALE GET SWITCHES
#@app.route('/api/get_switches/<ntwID>')
#def get_generic_endpoint(ntwID):
#    request_url=URL + f"/networks/{ntwID}/devices"
#    #return valore della funzione get_networks in Func_AppRoute.py
#    ntwDev=FuncUser.get_APIgeneric(request_url)
#    ntwDev=FuncMatrix.FilterListNtwDev(ntwDev,'name','serial','switch','model')
#    ntwDev=FuncMatrix.Add_ListElement(ntwDev,'serial','name','ALL','ALL')
#    return ntwDev

@app.route('/api/get_switches/<ntwIDs>')
def get_sw_ntwidss(ntwIDs):
    ntwID_list = ntwIDs.split(",")
    allDevices = []
    device_type = request.args.get("deviceType")
    if device_type == 'AP':
        FilterString='MR'
    elif device_type == 'SW':
        FilterString='MS'
    else:
        FilterString='ALL'
    for ntwID in ntwID_list:
        request_url=URL + f"/networks/{ntwID}/devices"
        #return valore della funzione get_networks in Func_AppRoute.py
        ntwDev=FuncUser.get_APIgeneric(request_url)
        allDevices.extend(json.loads(ntwDev))
    allDevices=FuncMatrix.FilterListNtwDev_AllFields(allDevices,'model',FilterString)
    #allDevices=FuncMatrix.FilterListNtwDev(allDevices,'name','serial','switch','model')
    allDevices=FuncMatrix.Add_ListElement(allDevices,'serial','name','ALL','ALL')
    return allDevices

@app.route('/api/get_switches/old/<ntwIDs>')
def get_switches(ntwIDs):
    # ntwIDs può essere una singola ID o più ID separati da virgola
    ntwID_list = ntwIDs.split(",") 
    all_switches = []
    for ntwID in ntwID_list:
        try:
            switches = FuncUser.get_ListSwitch_by_NtwID(ntwID)
            all_switches.extend(switches)
        except Exception as e:
            print(f"Errore caricando switch da network {ntwID}: {e}")  
    return jsonify(all_switches)

### - FUNZIONE GENERALE GET SWITCHES

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
    ssid_data = FuncUser.get_APIgeneric(request_url)
    ssid_data_json=jsonify(ssid_data)
    return jsonify(ssid_data)

@app.route('/api/get_ssid_settings/<ntwID>/<ssidNumber>')
def get_ssid_settingsByNumber(ntwID,ssidNumber):
    request_url=URL + f"/networks/{ntwID}/wireless/ssids/{ssidNumber}"
    ssid_data=FuncUser.get_APIgeneric(request_url)
    #ssid_data_json=ssid_data.json
    return ssid_data



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
            ListNtw = FuncUser.get_networks_ID(orgID,selected_ntwtype)
        modify_json = request.form['ModifyJson']  # Ottieni il JSON inviato
        #json_script_path = r"JSON_PATH"

        # Converti il JSON string in un oggetto Python
        json_data = json.loads(modify_json)  # Assicurati di importare json in cima al tuo file
        json_value_pkey = json_data[pkey]

        #Chiamata per fare Update DATA
        if selected_ntwtype == "SINGLE":    
            ntwID=ListNtw
            request_url=URL + f"/networks/{ntwID}/wireless/rfProfiles/{json_value_pkey}"
            json_output = FuncJSON.UpdateJsonData(request_url, json_data)
        #Altrimenti passo la list di tutte le reti facenti parte del Tipo selezionato
        else:
            for ntwID, name in ListNtw:
                # Esegui l'aggiornamento dell'SSID usando i dettagli ricevuti
                request_url=URL + f"/networks/{ntwID}/wireless/rfProfiles/{json_value_pkey}"
                json_output = FuncJSON.UpdateJsonData(request_url, json_data)

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    organizations = FuncMeraki.getOrgID_Name()
    return render_template('API-RadioProfile.html', organizations=organizations, json_output=json_output)

@app.route('/api/get_rf_settings/<ntwID>')
def get_rf_settings(ntwID):
    request_url=URL + f"/networks/{ntwID}/wireless/rfProfiles"
    rf_data = FuncUser.get_APIgeneric(request_url) 
    return jsonify(rf_data)

@app.route('/api/get_rf_settings/<ntwID>/<rfID>')
def get_rf_settingsByNumber(ntwID,rfID):
    request_url=URL + f"/networks/{ntwID}/wireless/rfProfiles/{rfID}"
    rf_data=FuncUser.get_APIgeneric(request_url)
    return jsonify(rf_data)

@app.route('/api/post_rf_profiles/<ntwID>', methods=['POST'])
def POST_rf_profiles(ntwID):
    # Recupera il JSON inviato nel corpo della richiesta
    json_data = request.get_json()
    request_url = f"{URL}/networks/{ntwID}/wireless/rfProfiles"  # URL per creare un nuovo RF Profile
    response = FuncMeraki.Flask_POST_Generic(request_url, APIKEY, json_data)  # Funzione per inviare una richiesta POST
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
        ntwID = request.form.get('ntwID')
        pkey='id'
        #modification_type = request.form['ModifynetworkType']  # Ottieni il valore da ModificationType
        selected_ntwtype = request.form['networkType']
        if selected_ntwtype == "SINGLE": # se la network selezionata è "SINGOLA NETWORK faccio la modifica solo sulla rete selezioanata, else su tutte le reti facenti parte del type
            ListNtw = request.form['ntwID']
        else:
            # Ottieni i network filtrati chiamando get_networks - tutte le network facenti parte del ntwType
            ListNtw = FuncUser.get_networks_ID(orgID,selected_ntwtype)
            # ListNtw deve contenere solo gli ID
            ListNtw = [ntw[0] for ntw in ListNtw]
        # 1.Recupero la lista di tutti gli switch
        all_switches = FuncUser.get_Allswitch_by_NtwType(ListNtw)
        # 2.Recupero la lista di tutti gli switch
        all_ports = FuncUser.get_AllPorts_from_SwitchList(all_switches)
        # 3.Genera CSV e lo fa scaricare
        return FuncUser.generate_switches_csv(all_ports, filename_prefix="Meraki-Sw-")
        a=0

        #modify_json = request.form['ModifyJson']  # Ottieni il JSON inviato
        #json_script_path = r"JSON_PATH"

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    organizations = FuncMeraki.getOrgID_Name()
    return render_template('API-PortDown.html', organizations=organizations)

@app.route('/api/get_ports_down', methods=['GET'])
def get_ports_down():
    down_ports = FuncMeraki.GetSwPorts()  # Funzione che recupera i dati richiesti - ****DA FARE -  NON COMPLETATA ************
    return jsonify(down_ports)

###### PAGINA - Inventario Apparati Meraki
@app.route('/api/API-InventoryMeraki', methods=['GET', 'POST'])
def InveAppMeraki():
    json_output = None
    allDevices = []
    if request.method == 'POST':
        orgID = request.form['orgID']
        ntwID = request.form.get('ntwID')
        pkey='id'
        #Gestione Scelta tipo apparato (switch o AP)
        device_type = request.form.get("deviceType")
        #Imposto nome CSV
        filename_prefix=f"Meraki-{device_type}-"
        #modification_type = request.form['ModifynetworkType']  # Ottieni il valore da ModificationType
        selected_ntwtype = request.form['networkType']
        if selected_ntwtype == "SINGLE": # se la network selezionata è "SINGOLA NETWORK faccio la modifica solo sulla rete selezioanata, else su tutte le reti facenti parte del type
            ListNtw = request.form['ntwID']
        else:
            # Ottieni i network filtrati chiamando get_networks - tutte le network facenti parte del ntwType
            ListNtw = FuncUser.get_networks_ID(orgID,selected_ntwtype)
            # ListNtw deve contenere solo gli ID
            ListNtw = [ntw[0] for ntw in ListNtw]
        for ntw in ListNtw:
            # 1. Recupero switch della singola Nwtwork
            dev=FuncMeraki.API_getDevicesByNtwID(ntw)
            # Aggiungo la lista recuperata a quelli della network precedente --- non serve json.loads(dev) in quanto dev è già una lista!
            allDevices.extend(dev)
        if device_type =='AP':
            allDevices_ap = FuncMatrix.FilterListNtwDev_AllFields (allDevices,'model','MR')
            return FuncUser.generate_switchesPorts_csv2(allDevices_ap, filename_prefix)
        elif device_type =='SW':
            allDevices_switch = FuncMatrix.FilterListNtwDev_AllFields (allDevices,'model','MS')
            # 2.Recupero la lista delle porte di tutti gli switch
            #Creo allDevices_switchPorts che conterrà sia switch che porte
            allDevices_switchPorts = [] 
            for dev in allDevices_switch:
                serial_device= dev["serial"]
                ports=FuncMeraki.API_GetSWPortBySerial(serial_device)
                dev_ports = dev.copy()
                dev_ports["ports"] = ports
                allDevices_switchPorts.append(dev_ports)
            return FuncUser.generate_switchesPorts_csv2(allDevices_switchPorts, filename_prefix)
        #DEBUG=0
        # 3.Genera CSV e lo fa scaricare
        #return FuncUser.generate_switches_csv(all_ports, filename_prefix="Meraki-Sw-")

        
        a=0

        #modify_json = request.form['ModifyJson']  # Ottieni il JSON inviato
        #json_script_path = r"JSON_PATH"

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    organizations = FuncMeraki.getOrgID_Name()
    return render_template('API-InventoryMeraki.html', organizations=organizations)

###### PAGINA - LM Catalyst to Meraki --> Parte Download config
@app.route('/api/LM-CatMeraki', methods=['GET', 'POST'])
def LMCatMeraki():
    json_output = None
    allDevices = []
    if request.method == 'POST':
        orgID = request.form['orgID']
        ntwID = request.form.get('ntwID')
        pkey='id'
        #Gestione Scelta tipo apparato (switch o AP)
        device_type = request.form.get("deviceType")
        #Imposto nome CSV
        filename_prefix=f"Meraki-{device_type}-"
        #modification_type = request.form['ModifynetworkType']  # Ottieni il valore da ModificationType
        selected_ntwtype = request.form['networkType']
        if selected_ntwtype == "SINGLE": # se la network selezionata è "SINGOLA NETWORK faccio la modifica solo sulla rete selezioanata, else su tutte le reti facenti parte del type
            ntw = request.form['ntwID']
            dev=FuncMeraki.API_getDevicesByNtwID(ntw)
            # Aggiungo la lista recuperata a quelli della network precedente --- non serve json.loads(dev) in quanto dev è già una lista!
            allDevices.extend(dev)
        else:
            # Ottieni i network filtrati chiamando get_networks - tutte le network facenti parte del ntwType
            ListNtw = FuncUser.get_networks_ID(orgID,selected_ntwtype)
            # ListNtw deve contenere solo gli ID
            ListNtw = [ntw[0] for ntw in ListNtw]
            for ntw in ListNtw:
                # 1. Recupero switch della singola Nwtwork
                dev=FuncMeraki.API_getDevicesByNtwID(ntw)
                # Aggiungo la lista recuperata a quelli della network precedente --- non serve json.loads(dev) in quanto dev è già una lista!
                allDevices.extend(dev)
        if device_type =='AP':
            allDevices_ap = FuncMatrix.FilterListNtwDev_AllFields (allDevices,'model','MR')
            return FuncUser.generate_switchesPorts_csv2(allDevices_ap, filename_prefix)
        elif device_type =='SW':
            allDevices_switch = FuncMatrix.FilterListNtwDev_AllFields (allDevices,'model','C9')
            # 2.Recupero la lista delle porte di tutti gli switch
            #Creo allDevices_switchPorts che conterrà sia switch che porte
            allDevices_switchPorts = [] 
            for dev in allDevices_switch:
                serial_device= dev["serial"]
                ports=FuncMeraki.API_GetSWPortBySerial(serial_device)
                dev_ports = dev.copy()
                dev_ports["ports"] = ports
                allDevices_switchPorts.append(dev_ports)
            return FuncUser.generate_switchesPorts_zip(allDevices_switchPorts, filename_prefix)
        #DEBUG=0
        # 3.Genera CSV e lo fa scaricare
        #return FuncUser.generate_switches_csv(all_ports, filename_prefix="Meraki-Sw-")

        
        a=0

        #modify_json = request.form['ModifyJson']  # Ottieni il JSON inviato
        #json_script_path = r"JSON_PATH"

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    organizations = FuncMeraki.getOrgID_Name()
    return render_template('LM-CatMeraki.html', organizations=organizations)

###### PAGINA - LM Catalyst to Meraki --> Parte Upload config
@app.route('/api/LM-CatMeraki-upload-switches', methods=['POST'])
def upload_switches():
    if 'file' not in request.files:
        return jsonify({"error": "Nessun file presente"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nome file vuoto"}), 400
    # ──────────────── Dry-run opzionale ────────────────
    dry_run = request.form.get("dry_run", "true").lower() == "true"
    # Estensione
    filename = file.filename.lower()
    if filename.endswith('.csv'):
        return FuncOS.handle_csv_upload(file)
    elif filename.endswith('.zip'):
        return FuncOS.handle_zip_upload(file)
    else:
        return jsonify({"error": "Formato non supportato"}), 400


###### PAGINA - API - GLPI INVENTARIO
@app.route('/api/GLPI-InveManu', methods=['GET', 'POST'])
def GLPI_INVE_MANU():
    if request.method == 'POST':
        entID = request.form['entID']
        negoID = request.form['negoID']
        List_states = json.loads(request.form['statesSelect'])
        #Chiama funzione di Func_PY_GLPI.py
        result_path=FuncGLPI.APP_GLPI_InveManu(entID,negoID,List_states)
        #Crea richiesta per downlod del file
        response=send_file(result_path, as_attachment=True)
        return response

    # Se la richiesta è GET, mostra l'elenco delle organizzazioni
    #Innazitutto cancella eventuale file InveManu - fatto in GET altrimenti dava errori di accesso
    if os.path.exists(InveManu_nameFile):
        os.remove (InveManu_nameFile)
    entities = FuncDB.fetch_Settings_GLPI(" SELECT * FROM glpi_entities",1,0)
    states = FuncDB.fetch_Settings_GLPI("SELECT * FROM glpi_states",1,0)
    return render_template('API-GLPI-InveManu.html', entities=entities, states=states)

@app.route ('/fetch_glpi_locations/<entID>', methods=['GET'])
def get_glpi_locations(entID):
    query='SELECT * FROM glpi_locations WHERE entities_id=' + entID
    return FuncDB.CopiaCampiDB(query,3,0)


@app.route('/api/test')
def test():
    result = CreateSSID(URL, APIKEY, json_script_path)  # Puoi modificare il comportamento se necessario
    return jsonify(result)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        #ssl_context=('certificates/MerakiAPI-Cert.pem', 'certificates/MerakiAPI-key.pem')
    )
