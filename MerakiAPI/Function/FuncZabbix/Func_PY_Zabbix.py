from flask import jsonify, send_file
from datetime import datetime
import re,csv,io,requests

from Function.FuncJSON import Func_PY_JSON as FuncJSON
from config import ZABURL,ZABHEADERS

def GetInventory():
    a=0

def SendAPI(rows, dry_run):
    b=0

# Funzione per lanciare API su Zabbix Generica
def zabbix_SendAPI(method, params=None, request_id=1):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params or {},
        "id": request_id
    }
    r = requests.post(
        ZABURL,
        headers=ZABHEADERS,
        json=payload,
        timeout=10
    )
    r.raise_for_status()
    data = r.json()
    
    #DEBUG
    #print("RESPONSE:", data)

    if "error" in data:
        raise RuntimeError(f"Zabbix API error: {data['error']}")
    return data["result"]

#Funzione ADD Macro in HOST
def zabbix_AddMacro_to_Host_By_Meraki(merHost,orgId):
    #Get HostID e HostName da Zabbix
    zabHost=zabbix_SendAPI("host.get",{"output": ["hostid", "host"],"selectInterfaces": ["interfaceid", "ip"]})

    #---VARIABILI DICHIARATE SOLO PER TEST
    #hostid="13344"  #SNI001SW001A
    #macro="{$SERZAB}"
    #value="SERIALEDAZABBIX"
    #---FINE VARIABILI DICHIARATE SOLO PER TEST

    
    mapped_host=map_meraki_to_zabbix(merHost,zabHost)
    for host, data in mapped_host.items():
        #Update MACRO HOST
        hostid=data["hostid"]
        macros = []

        # Macro SERIAL
        macros.append(
            zabbix_ParamsAddMacro(
                "{$SERIAL}",
                data["serial"]
            )
        )
        # Macro ORGANIZATION_ID
        macros.append(
            zabbix_ParamsAddMacro(
                "{$ORGANIZATION_ID}",
                str(orgId)
            )
        )

        
        params = {
            "hostid": hostid,
            "macros": macros
        }
        #macro="{$SERIAL}"
        #value=data["serial"]
        #params=zabbix_ParamsAddMacro(hostid,macro,value)
        #params=zabbix_ParamsAddMacro(hostid,macros)
        zabHostUpdate=zabbix_SendAPI("host.update", params)
    return zabHostUpdate
    #return {
    #    "updated_hosts": len(mapped_hosts),
    #    "organization_id": orgId
    #}


#Funzione per creare Param per Update di una macro di 1 Host in Zabbix - 1 
#def zabbix_ParamsAddMacro(hostid,macro,value):
#    paramMacroSerial={
#        "hostid": hostid,
#        "macros": [
#            {
#                "macro": macro,
#                "value": value
#            }
#        ]
#    }
#    return paramMacroSerial

def zabbix_ParamsAddMacro(macro, value):
    return {
        "macro": macro,
        "value": value
    }


#Funzione per unire HostID Zabbix a Name e Serial Meraki
def map_meraki_to_zabbix(merHosts, zabHosts):
    mapping = {}
    zabHost = {h["host"]: h for h in zabHosts}
    for merHost in merHosts:
        merHost_name = merHost.get("name")
        merHost_serial = merHost.get("serial")

        if merHost_name in zabHost:
            mapping[merHost_name] = {
                "hostid": zabHost[merHost_name]["hostid"],
                "serial": merHost_serial
            }
    return mapping

    
