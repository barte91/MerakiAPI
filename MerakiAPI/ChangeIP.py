import requests,json,openpyxl,pandas as pd, os
from openpyxl import load_workbook


def set_ChangeIP_ByFile(URL,APIKEY,orgID,xls_path):
    #Richiedo il file da elaborare
    list_fn=getFileName(xls_path)
    fn=AskFileName(list_fn)
    xls_path_fin=xls_path+"/"+fn
    #Richiedo codice network
    user_nwname=AskNwName()
    df_devList=pd.read_excel(open(xls_path_fin,'rb'),sheet_name="Inventory")
    #df_devList=pd.read_excel(open(xls_path_fin,'rb'),sheet_name="Inventory",dtype={"Name":[],"Serial":[],"Model":[], "IPNew":[], "MaskNew":[], "GwNew":[], "NetwName":[]})
    #df_devList=pd.read_excel("C:\MerakiAPI\ChangeIP\ChangeIP-AP-Test.xsx",sheet_name="Inventory",dtype={"Name":[],"Serial":[],"Model":[], "IPNew":[], "MaskNew":[], "GwNew":[], "NetwName":[]})
    #Richiedo la network desiderata
    #ntw=getNetworksID_Name(URL,APIKEY,orgID)
    #ntwName=AskNetworkNameToUser(ntw)
    #Inzio ciclo UpdatePorts
    i=0
    for nwname in df_devList['NetwName']:
        if nwname.startswith(user_nwname):
            serial=df_devList['Serial'][i]
            IPNew=df_devList['IPNew'][i]
            MaskNew=df_devList['MaskNew'][i]
            GwNew=df_devList['GwNew'][i]
            VlanNew=df_devList['vlan'][i]
            #portName="***/" + str(df_devList['PortName'][i])
            UpdateIP(URL,APIKEY,serial,IPNew,MaskNew,GwNew,VlanNew)
        i=i+1

def getFileName(xls_path):
    list_fn=[]
    for path in os.listdir(xls_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(xls_path, path)):
            list_fn.append(path)
    return list_fn

def AskFileName(list_fn):
    #print("Selezionare Network")
    print(*list_fn, sep = "\n")
    fn=input("Digitare il nome del file: ")
    return fn

def AskNwName():
    #print("Selezionare Network\n")
    #print(*list_fn, sep = "\n")
    nw=input("Digitare codice network (esempio: per Caronno digita 104): ")
    return nw

def UpdateIP(URL,APIKEY,serial,IPNew,MaskNew,GwNew,VlanNew):
    #queryURL = URL + f"/devices/{serial}/switch/ports/{portid}?name={portName}&enabled=false&poeEnabled=false"
    VlanNew=str(VlanNew)
    queryURL = URL + f"/devices/{serial}/managementInterface"
    payload = json.dumps({
        "wan1": {
            "wanEnabled": "enabled",
            "usingStaticIp": "true",
            "staticIp": IPNew,
            "staticGatewayIp": GwNew,
            "staticSubnetMask": MaskNew,
            "staticDns": [
                "10.100.5.1",
                "10.100.5.2"
            ],
            #se non serve mettere VLAN mettere None
            "vlan": VlanNew
        },
        "wan2": {
            "wanEnabled": "not configured",
            "vlan": None
        }
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Bearer c12a73de18156681be08428bd345afc748aba00e'
    }
    #payload = '''{"wan1":{"staticGatewayIp":"192.168.139.254","staticIp":"192.139.192","staticSubnetMask":"255.255.255.128","wanEnabled":'enabled',"usingStaticIp":true,"staticDns":["10.100.5.1","10.100.5.2"]},"wan2":{"wanEnabled":'disabled'}}'''

    #response = requests.put(queryURL, headers=APIKEY)

    response = requests.request("PUT", queryURL, headers=headers, data=payload)
    print(response.text)
    a=0
    #{{baseUrl}}/devices/:serial/switch/ports/:portId?name=***&enabled=true
