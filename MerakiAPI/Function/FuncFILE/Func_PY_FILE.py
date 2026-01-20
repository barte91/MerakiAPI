from Function.FuncMeraki import Func_PY_Meraki as FuncMeraki
from flask import jsonify


#PROVVISORIO - LM CAT TO MERAKI
def LM_CatMeraki_apply_ports_config(rows, dry_run=True):
    results = []
    for row in rows:
        serial = row.get("serial")
        port_id = row.get("port_portId")
        #Gestione errore - No Serial or PortID
        if not serial or not port_id:
            results.append({
                "status": "error",
                "reason": "serial o portId mancanti",
                "row": row
            })
            continue
        payload = build_port_payload(row)

        if dry_run:
            results.append({
                "status": "dry-run",
                "serial": serial,
                "port": port_id,
                "payload": payload
            })
        else:
            resp = FuncMeraki.API_UpdateSwitchPort(
                serial=serial,
                port_id=port_id,
                payload=payload
            )
            results.append(resp)

    return jsonify(results)

def build_port_payload(row):
    payload = {}

    mapping = {
        "port_enabled": "enabled",
        "port_type": "type",
        "port_vlan": "vlan",
        "port_voiceVlan": "voiceVlan",
        "port_allowedVlans": "allowedVlans",
        "port_poeEnabled": "poeEnabled"
    }

    for csv_key, api_key in mapping.items():
        if csv_key in row and row[csv_key] not in [None, ""]:
            payload[api_key] = normalize_csv_value(row[csv_key])

    return payload

def normalize_csv_value(value):
    if isinstance(value, str):
        v = value.lower()
        if v == "true":
            return True
        if v == "false":
            return False
        if v.isdigit():
            return int(v)
    return value