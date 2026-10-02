from flask import jsonify, send_file
from datetime import datetime
import re,csv,io,requests,urllib3

from Function.FuncJSON import Func_PY_JSON as FuncJSON
from config import ZABURL,ZABHEADERS

# Disabilita il warning HTTPS non verificato
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        verify=False,
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

# FUNZIONI GENERICHE PER RECUPERO HOST E TEMPLATE ZABBIX

#Funzione per unire HostID Zabbix a Name e Serial Meraki
def zabbix_GetCriticalPortsTemplate():
    params = {
        "output": [
            "templateid",
            "host",
            "name"
        ],
        "filter": {
            "host": [
                "BARTE-Meraki-SW-Monitoring-CriticalPorts-SNMPv3"
            ]
        }
    }
    return zabbix_SendAPI("template.get", params)

def zabbix_GetPortAdminStatusItems(templateid):
    params = {
        "output": [
            "itemid",
            "hostid",
            "name",
            "key_",
            "lastvalue",
            "lastclock"
        ],
        "templateids": [
            templateid
        ],
        "search": {
            "key_": "net.if.adminstatus["
        },
        "searchByAny": False
    }
    return zabbix_SendAPI("item.get", params)

def zabbix_GetPortAdminStatusItemsByHosts(hostids):

    params = {
        "output": [
            "itemid",
            "hostid",
            "name",
            "key_",
            "lastvalue",
            "lastclock"
        ],
        "hostids": hostids,
        "search": {
            "key_": "net.if.adminstatus["
        },
        "searchByAny": False
    }

    return zabbix_SendAPI("item.get", params)

# Recupera HostID e ItemID per una specifica chiave Zabbix (zabbix_key) per un elenco di host (hostids)
def zabbix_GetKeyItemsByHosts(hostids, zabbix_key):
    params = {
        "output": [
            "itemid",
            "hostid",
            "name",
            "key_",
            "lastvalue",
            "lastclock"
        ],
        "hostids": hostids,
        "search": {
            "key_": zabbix_key
        },
        "searchByAny": False
    }

    return zabbix_SendAPI("item.get", params)

def zabbix_GetItemsHistory(itemids, time_from):

    params = {
        "output": "extend",
        "history": 3,
        "itemids": itemids,
        "time_from": time_from,
        "sortfield": "clock",
        "sortorder": "ASC"
    }

    return zabbix_SendAPI(
        "history.get",
        params
    )

def zabbix_GetItemHistory(itemid, time_from):

    params = {
        "output": "extend",
        "history": 3,
        "itemids": [itemid],
        "time_from": time_from,
        "sortfield": "clock",
        "sortorder": "ASC"
    }

    return zabbix_SendAPI("history.get", params)

def zabbix_GetHostsByTemplate(templateid):
    params = {
        "output": [
            "hostid",
            "host",
            "name"
        ],
        "templateids": [
            templateid
        ]
    }
    return zabbix_SendAPI("host.get", params)

def zabbix_GetHostGroups():
    params = {
        "output": [
            "groupid",
            "name"
        ],
        "sortfield": "name",
        "sortorder": "ASC"
    }

    return zabbix_SendAPI("hostgroup.get", params)

def zabbix_GetHostsByGroup(groupid):

    params = {
        "output": [
            "hostid",
            "host",
            "name",
            "status"
        ],
        "groupids": [groupid],
        "filter": {
            "status": "0"
        },
        "tags": [
            {
                "tag": "devtype",
                "value": "switch"
            }
        ],
        "evaltype": 0,
        "sortfield": "name",
        "sortorder": "ASC"
    }

    return zabbix_SendAPI(
        "host.get",
        params
    )

# FUNZIONE CONVERTI ID IN NOMI ESPLICITI

def ConvertLinkStatus(value):
    status = {
        "1": "UP",
        "2": "DOWN"
    }
    return status.get(str(value), f"UNKNOWN ({value})")

# FUNZIONE PER CREARE GERARCHIA HOSTGROUPS

def BuildHostGroupHierarchy(groups):
    hierarchy = {}
    for group in groups:
        name = group["name"]
        groupid = group["groupid"]
        parts = name.split("/")
        # Consideriamo solo gruppi con almeno 2 livelli
        if len(parts) < 1:
            continue
        bu = parts[0] #bu=BUSINESS UNIT (LM,TM....)
        if bu not in hierarchy:
            hierarchy[bu] = {
                "groupid": None,
                "types": {}
            }
        # BU
        if len(parts) == 1:
            hierarchy[bu]["groupid"] = groupid
            continue
        group_type = parts[1]
        if group_type not in hierarchy[bu]["types"]:
            hierarchy[bu]["types"][group_type] = {
                "groupid": None,
                "locations": {}
            }
        # Tipo
        if len(parts) == 2:
            hierarchy[bu]["types"][group_type]["groupid"] = groupid
            continue
        # Location
        location = "/".join(parts[2:])
        hierarchy[bu]["types"][group_type]["locations"][location] = {
            "groupid": groupid
        }
    return hierarchy

#Aggiungi voce "ALL" a tutte le selezioni per gerarchia HOSTGROUPS
def AddAllToHostGroupHierarchy(hierarchy):
    result = {
        "ALL": {
            "groupid": None,
            "types": {}
        }
    }
    for bu, bu_data in hierarchy.items():
        result[bu] = {
            "groupid": bu_data["groupid"],
            "types": {
                "ALL": {
                    "groupid": None,
                    "locations": {}
                }
            }
        }
        for group_type, type_data in bu_data["types"].items():

            result[bu]["types"][group_type] = {
                "groupid": type_data["groupid"],
                "locations": {
                    "ALL": {
                        "groupid": None
                    }
                }
            }
            for location, location_data in type_data["locations"].items():

                result[bu]["types"][group_type]["locations"][location] = {
                    "groupid": location_data["groupid"]
                }

    return result

    
