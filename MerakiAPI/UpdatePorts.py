import requests,json,openpyxl,pandas as pd, os
from openpyxl import load_workbook
import meraki



def set_UpdateportsByFile(URL,APIKEY,orgID,xls_path):
    #Richiedo il file da elaborare
    list_fn=getFileName(xls_path)
    fn=AskFileName(list_fn)
    xls_path_fin=xls_path+"/"+fn
    df_swListTot=pd.read_excel(open(xls_path_fin,'rb'),sheet_name="Inventory",dtype={"Name":[],"Serial":[],"Model":[], "IP":[], "NetwName":[], "portID":[], "Enabled":[], "Status":[], "PortName":[], "PoeEnable":[]})
    #Richiedo la network desiderata
    #ntw=getNetworksID_Name(URL,APIKEY,orgID)
    #ntwName=AskNetworkNameToUser(ntw)
    #Inzio ciclo UpdatePorts
    i=0
    for nwname in df_swListTot['NetwName']:
        #if nwname==ntwName:
            serial=df_swListTot['Serial'][i]
            portID=df_swListTot['portID'][i]
            portName="***/" + str(df_swListTot['PortName'][i])
            UpdatePort(URL,APIKEY,serial,portID,portName)
            i=i+1
        #i+=1

def set_UpdateportsByFile_and_NwName(URL,APIKEY,orgID,xls_path):
    #Richiedo il file da elaborare
    list_fn=getFileName(xls_path)
    fn=AskFileName(list_fn)
    xls_path_fin=xls_path+"/"+fn
    df_swListTot=pd.read_excel(open(xls_path_fin,'rb'),sheet_name="Inventory",dtype={"Name":[],"Serial":[],"Model":[], "IP":[], "NetwName":[], "portID":[], "Enabled":[], "Status":[], "PortName":[], "PoeEnable":[]})
    #Richiedo la network desiderata
    ntw=getNetworksID_Name(URL,APIKEY,orgID)
    ntwName=AskNetworkNameToUser(ntw)
    #Inzio ciclo UpdatePorts
    i=0
    for nwname in df_swListTot['NetwName']:
        if nwname==ntwName:
            serial=df_swListTot['Serial'][i]
            portID=df_swListTot['portID'][i]
            portName="***/" + str(df_swListTot['PortName'][i])
            UpdatePort(URL,APIKEY,serial,portID,portName)
        i+=1

def set_V2_UpdateportsByFile_and_NwName_withTemplate(URL,APIKEY,orgID,xls_path):
    #Richiedo il file da elaborare
    file_list = getFileName(xls_path)
    selected_file = AskFileName(file_list)
    xls_full_path = f"{xls_path}/{selected_file}"

    # Load data from the "Inventory" sheet in the Excel file
    df_inventory = pd.read_excel(xls_full_path, sheet_name="Inventory")

    # Request the target network name from the user
    network_info = getNetworksID_Name(URL, APIKEY, orgID)
    target_network_name = AskNetworkNameToUser(network_info)

    # Begin updating ports
    for i, row in df_inventory.iterrows():
        a=row['NetwName']
        if target_network_name=='ALL' or row['NetwName'] == target_network_name:
            port_name_ori = row['PortName']
            serial = str(row['Serial']).strip()
            port_id = row['portID']

            # Prepend the "***/" prefix if not already present
            if not port_name_ori.startswith("***/") :
                port_name = f"***/{port_name_ori}"
            else:
                port_name=port_name_ori
            
            # Call the UpdatePort function with the modified port name
            # Escludo quelle Router / Server e Firewall
            if not port_name_ori.startswith("RTR") and not port_name_ori.startswith("FW") and not port_name_ori.startswith("SERVER") and not port_name_ori.startswith("BCK"):
                UpdatePortV2(URL, APIKEY, serial, port_id, port_name)


def AskNetworkNameToUser(ntw):
    #print("Selezionare Network")
    print(*ntw["Name"], sep = "\n")
    ntwName=input("Digitare la network desiderata (scrivi ALL per tutte): ")
    return ntwName

def AskFileName(list_fn):
    #print("Selezionare Network")
    print(*list_fn, sep = "\n")
    fn=input("Digitare il nome del file: ")
    return fn

def getFileName(xls_path):
    list_fn=[]
    for path in os.listdir(xls_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(xls_path, path)):
            list_fn.append(path)
    return list_fn

def getNetworksID_Name(URL,APIKEY,orgID):
    """
    Use Organization ID to pull list of networks we have access to
    """
    queryURL = URL + f"/organizations/{orgID}/networks"
    response = requests.get(queryURL, headers=APIKEY)
    data = json.loads(response.text)
    network = {"ID":[],"Name":[]};
    for ntw in data:
        network["ID"].append(ntw["id"])
        network["Name"].append(ntw["name"])
    return network

def UpdatePort(URL,APIKEY,serial,portid,portName):
    queryURL = URL + f"/devices/{serial}/switch/ports/{portid}?name={portName}&enabled=false&poeEnabled=false"
    response = requests.put(queryURL, headers=APIKEY)
    a=0
    #{{baseUrl}}/devices/:serial/switch/ports/:portId?name=***&enabled=true

def UpdatePortV2(URL,APIKEY,serial,portid,portName):
    API_KEY="f25d79a1df42dff69f5337fa61c60c2b798aa404"
    dashboard = meraki.DashboardAPI(API_KEY)
    
    # Step 1: Remove the port profile
    dashboard.switch.updateDeviceSwitchPort(
    serial=serial,
    portId=portid,
    profile={
        "enabled": False}
    )
    
    # Step 2: Cambio Nome su porta e metto porta in Disabled
    dashboard.switch.updateDeviceSwitchPort(
        serial=serial,
        portId=portid,
        name=portName,
        enabled=False,
        poeEnabled=False
    )
    #queryURL = URL + f"/devices/{serial}/switch/ports/{portid}?name={portName}&enabled=false&poeEnabled=false"
    #response = requests.put(queryURL, headers=APIKEY)
    a=0
    #{{baseUrl}}/devices/:serial/switch/ports/:portId?name=***&enabled=true



