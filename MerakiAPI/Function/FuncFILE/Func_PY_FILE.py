from Function.FuncMeraki import Func_PY_Meraki as FuncMeraki
from MerakiConfig.LMConfPortByName import PORT_PROFILES_STORE, PORT_PROFILES_ENT
from flask import jsonify, send_file
from datetime import datetime
import re,csv,io

##VARIABILI GLOBALI - | Programma Catalyst to Meraki
#Variabile globale per individuare porte con nome tipo "Gi1/0/13" - quelle vuote, da shuttare
PORT_ONLY_REGEX = re.compile(r"^[A-Za-z]{1,3}\d+(?:/\d+)+$")
#Variabile GLOBAL per resettare file CSV No Profile
LAST_NO_PROFILE_CSV = None

#PROVVISORIO - LM CAT TO MERAKI - STANDARD --> Prendo config da CSV e la scrivo su API
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

# Costruzione del payload da inviare per configurare porta switch
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
        #ignora campi vuoti
        if csv_key in row and row[csv_key] not in [None, ""]:
            payload[api_key] = normalize_csv_value(row[csv_key])

    return payload




#PROVVISORIO - LM CAT TO MERAKI - ADVANCED --> Prendo config da CSV, leggo port_name e in base alla prota applico un profilo specifico
def LM_CatMeraki_apply_ports_config_advanced(rows, dry_run: bool):
    results = []

    stats = {
        "total_rows": 0,
        "profile_applied": 0,
        "shut_applied": 0,
        "no_profile": 0,
        "errors": 0
    }
    if dry_run is None:
        mer_dashboard=FuncMeraki.API_MerakiIntialize()
    for row in rows:
        stats["total_rows"] += 1

        serial = row.get("serial")
        port_id = row.get("port_portId")
        raw_port_name = row.get("port_name")

        port_name = normalize_port_name_value(raw_port_name)
        port_enabled = normalize_csv_value(row.get("port_enabled"))

        if not serial or not port_id:
            stats["errors"] += 1
            results.append({
                "status": "ERROR",
                "serial": serial or "",
                "port": port_id or "",
                "port_name": port_name or "",
                "enabled": port_enabled,
                "poeEnabled": "",
                "type": "",
                "vlan": "",
                "allowedVlans": ""
            })
            continue

        payload, profile = build_port_payload_with_profile(row)

        # ─────────────── SHUT ───────────────
        if profile == "shut":
            stats["shut_applied"] += 1
            #if dry_run is None:
                #FuncMeraki.API_UpdateSwitchPort(serial, port_id, payload,mer_dashboard)
            results.append(build_output_row(serial, port_id, port_name, "PROFILE-APPLIED-SHUT", payload))
            #continue

        # ─────────────── NO PROFILE ───────────────
        if not payload:
            stats["no_profile"] += 1
            results.append(build_output_row(serial, port_id, port_name, "NO-PROFILE", {}))
            continue

        # ─────────────── PROFILO APPLICATO ───────────────
        stats["profile_applied"] += 1

        status_text = f"PROFILE-APPLIED-{profile}"
        if dry_run is None:
            try:
                FuncMeraki.API_UpdateSwitchPort(serial, port_id, payload,mer_dashboard)
                status_text += "-APPLIED"
            except Exception as e:
                stats["errors"] += 1
                results.append(build_output_row(serial, port_id, port_name, f"ERROR-{str(e)}", {}))
                continue
        else:
            status_text += "-DRYRUN"

        results.append(build_output_row(serial, port_id, port_name, status_text, payload))

    # ─────────────── GENERA CSV COMPLETO ───────────────
    full_csv = generate_full_csv(results, stats)
    global LAST_FULL_CSV
    LAST_FULL_CSV = full_csv

    return jsonify({
        "stats": stats,
        "results": results,
        "full_csv": full_csv
    })


# ─────────────── BUILD OUTPUT ROW ───────────────
def build_output_row(serial, port_id, port_name, status, payload):
    return {
        "serial": serial,
        "port_id": port_id,
        "port_name": port_name,
        "status": status,
        "enabled": payload.get("enabled") if payload else "",
        "poeEnabled": payload.get("poeEnabled") if payload else "",
        "type": payload.get("type") if payload else "",
        "vlan": payload.get("vlan") if payload else "",
        "allowedVlans": payload.get("allowedVlans") if payload else ""
    }


#Costruzione Payload in base al profilo deciso dal port name ridato dal detect_port_profile
def build_port_payload_with_profile(row):

    # Recupero nome switch per differenziare tra ENT/STORE ecc
    sw_name= row.get("name")

    #Assegno port profile in base al nome switch
    PortProfiles=detect_type_port_profile(sw_name)

    # Normalizzazione dati CSV
    port_name = normalize_port_name_value(row.get("port_name"))
    port_enabled = normalize_csv_value(row.get("port_enabled"))
    
    # 1️. LOGICA SHUT
    # porta senza nome + disabilitata
    if port_enabled is False and port_name == "":
        payload = PortProfiles["shut"]["payload"].copy()
        return payload, "shut"

    # 2️. Rilevamento profilo da nome porta
    profile = detect_port_profile(port_name, PortProfiles)

    if not profile:
        return None, None

    # 3️. Payload base dal profilo
    payload = PortProfiles[profile]["payload"].copy()

    # 4️. Campi dinamici dal CSV
    payload["name"] = port_name
    payload["enabled"] = port_enabled

    if "port_rstpEnabled" in row:
        payload["rstpEnabled"] = normalize_csv_value(row["port_rstpEnabled"])
    if "port_stpGuard" in row:
        payload["stpGuard"] = normalize_csv_value(row["port_stpGuard"])
    if "port_poeEnabled" in row:
        payload["poeEnabled"] = normalize_csv_value(row["port_poeEnabled"])

    return payload, profile

#
def detect_type_port_profile(sw_name):
    #Assegno port profile in base al nome switch
    prefix = sw_name[:3]

    if prefix == "MAG":
        PortProfiles = PORT_PROFILES_STORE
    elif prefix == "ENT":
        PortProfiles = PORT_PROFILES_ENT
    elif prefix == "RDC":
        PortProfiles = PORT_PROFILES_RDC
    elif prefix == "SRM":
        PortProfiles = PORT_PROFILES_SRM
    else:
        raise ValueError(f"Prefisso non riconosciuto: {prefix}")
    return PortProfiles

#Prende nome e applica profilo
def detect_port_profile(port_name: str, PortProfiles) -> str | None:
    if not port_name:
        return None

    name = port_name.lower()

    for profile, cfg in sorted(
        PortProfiles.items(),
        key=lambda x: x[1].get("priority", 0),
        reverse=True
    ):
        pattern = cfg.get("pattern")
        if pattern and re.search(pattern, name):
            return profile

    return None



#----------------------------NORMALIZZAZIONE VALORI------------------------------------------------

# Normalizza valori, in CSV sono String, API Meraki richiede boolean/int
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


def normalize_port_name_value(port_name: str | None) -> str | None:
    if not port_name:
        return port_name

    name = port_name.strip()

    # 1. Rimuove prefisso tipo "Gi1/0/24 - "
    name = re.sub(r"^[A-Za-z]{1,3}\d+(?:/\d+)+\s*-\s*", "", name).strip()

    # 2️. Se rimane solo il nome fisico → consideralo vuoto
    if PORT_ONLY_REGEX.match(name):
        return ""

    return name

#--------------------EXPORT CSV---------------------------------------------------------------------

def generate_no_profile_csv(no_profile_rows, stats):
    import io, csv

    output = io.StringIO()

    # colonne come nella tabella
    fieldnames = [
        "serial",
        "port_id",
        "port_name",
        "status",
        "enabled",
        "poeEnabled",
        "type",
        "vlan",
        "allowedVlans"
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    # Righe NO-PROFILE
    for row in no_profile_rows:
        writer.writerow({
            "serial": row.get("serial", ""),
            "port_id": row.get("port", ""),  # se nel tuo dict è 'port'
            "port_name": row.get("port_name", ""),
            "status": "NO-PROFILE",
            "enabled": row.get("port_enabled", ""),
            "poeEnabled": "",
            "type": "",
            "vlan": "",
            "allowedVlans": ""
        })

    # Riga vuota
    writer.writerow({})

    # Riga statistiche
    writer.writerow({
        "serial": "STATS",
        "port_id": "",
        "port_name": (
            f"total={stats['total_rows']} | "
            f"profile_applied={stats['profile_applied']} | "
            f"shut={stats['shut_applied']} | "
            f"no_profile={stats['no_profile']} | "
            f"errors={stats['errors']}"
        ),
        "status": "",
        "enabled": "",
        "poeEnabled": "",
        "type": "",
        "vlan": "",
        "allowedVlans": ""
    })

    return output.getvalue()

def generate_full_csv(results, stats):
    import io, csv

    output = io.StringIO()

    fieldnames = [
        "serial",
        "port_id",
        "port_name",
        "status",
        "enabled",
        "poeEnabled",
        "type",
        "vlan",
        "allowedVlans"
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for row in results:
        writer.writerow({
            "serial": row.get("serial", ""),
            "port_id": row.get("port", ""),
            "port_name": row.get("port_name", ""),
            "status": row.get("status", ""),
            "enabled": row.get("enabled", ""),
            "poeEnabled": row.get("poeEnabled", ""),
            "type": row.get("type", ""),
            "vlan": row.get("vlan", ""),
            "allowedVlans": row.get("allowedVlans", "")
        })

    # Riga vuota
    writer.writerow({})

    # Riga statistiche
    writer.writerow({
        "serial": "STATS",
        "port_id": "",
        "port_name": (
            f"total={stats['total_rows']} | "
            f"profile_applied={stats['profile_applied']} | "
            f"shut={stats['shut_applied']} | "
            f"no_profile={stats['no_profile']} | "
            f"errors={stats['errors']}"
        ),
        "status": "",
        "enabled": "",
        "poeEnabled": "",
        "type": "",
        "vlan": "",
        "allowedVlans": ""
    })

    return output.getvalue()

#-------- NORMALIZZAZIONE OUTPUT ----------------------
def build_output_row(
    serial,
    port_id,
    port_name,
    status,
    payload=None
):
    return {
        "serial": serial,
        "port_id": port_id,
        "port_name": port_name,
        "status": status,
        "enabled": payload.get("enabled") if payload else None,
        "poeEnabled": payload.get("poeEnabled") if payload else None,
        "type": payload.get("type") if payload else None,
        "vlan": payload.get("vlan") if payload else None,
        "allowedVlans": payload.get("allowedVlans") if payload else None,
    }