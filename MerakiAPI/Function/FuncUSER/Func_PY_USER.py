from flask import jsonify, request,send_file
from config import URL,APIKEY, xls_path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests,json,csv,io, datetime, zipfile
from Function.FuncMeraki import Func_PY_Meraki as FuncMeraki
from Function.FuncJSON import Func_PY_JSON as FuncJSON

#Get Netwrok per @app.route
def get_networks(orgID):
    network_type = request.args.get('type')
    try:
        #networks = FuncMeraki.getNtwID_Name(URL, APIKEY, orgID)  # Recupera tutte le reti
        networks = FuncMeraki.API_GetOrgNetworks(orgID) # Recupera tutte le reti
    except Exception as e:
        print(f"Errore: {e}")  # Stampa l'errore per il debug
        return jsonify({"error": "Errore nel recupero delle reti.", "message": str(e)}), 500
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
        elif network_type == "SRM" and (ntw[1].startswith("SRM") or ntw[1].startswith("RM")):
            filtered_networks.append(ntw)
        elif network_type == "FORNITORI" and ntw[1].startswith("FORN"):
            filtered_networks.append(ntw)
        elif network_type == "HQ" and ntw[1].startswith("HQ"):
            filtered_networks.append(ntw)
        elif network_type == "TUTTE":  # Non applico alcuna condizione
            filtered_networks.append(ntw)
        elif network_type == "SINGLE":  # Non applico alcuna condizione
            filtered_networks.append(ntw)
    #return valore convertito in JSON
    return jsonify(filtered_networks)

#Get Netwrok ID per @app.route
def get_networks_ID(orgID,network_type):
    networks = FuncMeraki.getNtwID_Name(URL, APIKEY, orgID)  # Recupera tutte le reti
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
        elif network_type == "SRM" and (ntw[1].startswith("SRM") or ntw[1].startswith("RM")):
            filtered_networks.append(ntw)
        elif network_type == "FORNITORI" and ntw[1].startswith("FORN"):
            filtered_networks.append(ntw)
        elif network_type == "HQ" and ntw[1].startswith("HQ"):
            filtered_networks.append(ntw)
        elif network_type == "TUTTE":  # Non applico alcuna condizione
            filtered_networks.append(ntw)
        #elif network_type == "SINGLE":  # Non applico alcuna condizione
        #   filtered_networks.append(ntw)
    #return valore convertito in JSON
    return filtered_networks

# FUNZIONE GET - API GENERIC @app.route

def get_APIgeneric( queryURL):
    response = requests.get(queryURL, headers=APIKEY)
    #response = requests.request("GET", queryURL, headers=APIKEY)
    if response.status_code == 200:
        # Ottieni i dati JSON dalla risposta
        data=response.text
        return data  # Restituisci direttamente i dettagli SSID
    else:
        return {"error": response.status_code, "message": response.text}


def AskOrgIDToUser(): #RICHIEDO ID ORG A UTENTE
    orgName=input("Digitare ID organization desiderata: ")
    return orgName

def AskNtwIDToUser(): #RICHIEDO NOME NETWORK A UTENTE
    ntwName=input("Digitare la network desiderata (scrivi ALL per tutte): ")
    return ntwName

def AskFileName(list_fn):
    #print("Selezionare Network")
    print(*list_fn, sep = "\n")
    fn=input("Digitare il nome del file: ")
    return fn

#ButtonApplyMod - EX CreateSSID
def ButtonApplyMod(req_url, json_data, ListNtw, ntwType):
    if ntwType == "SINGLE":    
        ntwID=ListNtw
        response = FuncJSON.UpdateJsonData(req_url, json_data)
    #Altrimenti passo la list di tutte le reti facenti parte del Tipo selezionato
    else:
        for ntwID, name in ListNtw:
            # Esegui l'aggiornamento dell'SSID usando i dettagli ricevuti
            response = FuncJSON.UpdateJsonData(req_url, json_data)

def get_SwitchDetails_by_Serial_parallel(serial):
    """
    Recupera i dettagli di uno switch dato il serial.
    Gestisce eventuali errori e ritorna None se fallisce.
    """
    try:
        sw_detail = FuncMeraki.API_GetSwitchDetailsBySerial(serial)
        if sw_detail:
            return sw_detail
    except Exception as e:
        print(f"Errore API_GetSwitchDetails per serial {serial}: {e}")
    return None


def get_ListSwitch_by_NtwID(ntwID, max_workers=10):
    """
    Restituisce la lista di switch presenti in una singola network Meraki.
    
    Args:
        ntwID (str): ID della network Meraki
    
    Returns:
        list[dict]: lista di switch con serial, name, model, lanIp, network_name e tags
    """
    switch_list = []
    try:
        switches = FuncMeraki.API_GetSwByNtwID(ntwID)  # tutti i dispositivi della network
        network_name = FuncMeraki.getNtwNameByID(ntwID)       # chiamiamo solo una volta per network

       # Parallelizza il recupero dettagli switch
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(get_SwitchDetails_by_Serial_parallel, serial): serial for serial, _ in switches}

            for future in as_completed(futures):
                serial = futures[future]
                sw_detail = future.result()
                if sw_detail and sw_detail["model"].startswith("MS"):
                    sw_detail["network_name"] = network_name
                    switch_list.append(sw_detail)

        #for serial, name in switches:
        #    sw_detail = FuncMeraki.get_SwitchDetails_by_Serial(serial)
        #    if sw_detail and sw_detail["model"].startswith("MS"):
        #        sw_detail["network_name"] = network_name
        #        switch_list.append(sw_detail)

    except Exception as e:
        print(f"Errore elaborando switch in network {ntwID} - ListSwitchByNtwID: {e}")

    return switch_list


def get_Allswitch_by_NtwType(ListNtw, max_workers=10):
    """
    Restituisce la lista di switch per un tipo di network (più network).
    
    Args:
        ListNtw (list[str]): Lista di network ID appartenenti allo stesso tipo
    
    Returns:
        list[dict]: Lista di switch compresa di Network Name
    """
    all_switches = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Lancia tutte le chiamate API in parallelo
        future_to_ntw = {executor.submit(get_ListSwitch_by_NtwID, ntwID): ntwID for ntwID in ListNtw}

        for future in as_completed(future_to_ntw):
            ntwID = future_to_ntw[future]
            try:
                switches = future.result()
                all_switches.extend(switches)
            except Exception as e:
                print(f"Errore recuperando switch da network {ntwID} - AllSwitchByNtwType: {e}")
    return all_switches
    #for ntwID in ListNtw:
    #    switches = get_ListSwitch_by_NtwID(ntwID)
    #    all_switches.extend(switches)




def get_AllPorts_from_SwitchList(switch_list):
    """
    Per ogni switch nel switch_list, recupera la lista porte.
    Restituisce una lista di dict con tutte le info utili.
    """
    all_ports = []

    for sw in switch_list:
        serial = sw.get("serial")
        if not serial:
            continue

        try:
            ports = FuncMeraki.getDeviceSwitchPortsBySerial(serial)
        except:
            ports = []

        for p in ports:
            if p.get("profile", {}).get("enabled") is True:
                profile_id = p.get("profile", {}).get("id")
                profile_name= FuncMeraki.API_GetPortProfileName(sw.get("network_id"),profile_id)
            all_ports.append({
                "network_name": sw.get("network_name"),
                "switch_name": sw.get("name"),
                "serial": serial,
                "tags_switch": "|".join(sw.get("tags", [])),
                "port_number": p.get("portId"),
                "port_name": p.get("name", ""),
                "enabled": p.get("enabled"),
                "type": p.get("type"),
                "vlan": p.get("vlan"),
                "allowedVlans": p.get("allowedVlans"),
                "poeEnabled": p.get("poeEnabled"),
                "isolationEnabled": p.get("isolationEnabled"),
                "rstpEnabled": p.get("rstpEnabled"),
                "stpGuard": p.get("stpGuard"),
                "profile_enabled": p.get("profile_enabled"),
                "profile_name": profile_name
            })
    return all_ports

#################### GENERAZIONE CSV
def generate_switches_csv(list, filename_prefix):
    """
    Genera un CSV dai dettagli degli switch e lo ritorna come file scaricabile Flask.
    """
    # Timestamp: YYYY-MM-DD
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{filename_prefix}_{timestamp}.csv"

    output = io.StringIO()

    # Campi 
    fieldnames = [
        "network_name",
        "switch_name",
        "serial",
        "tags_switch",
        "port_number",
        "port_description",
        "enabled",
        "poe_enabled",
        "type",
        "vlan",
        "speed",
        "duplex",
        "status"
    ]

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for port in list:
        writer.writerow({
            "network_name": port.get("network_name", ""),
            "switch_name": port.get("switch_name", ""),
            "serial": port.get("serial", ""),
            "tags_switch": port.get("tags_switch", ""),
            "port_number": port.get("port_number", ""),
            "port_description": port.get("port_name", ""),  # Meraki = name
            "enabled": port.get("enabled", ""),
            "poe_enabled": port.get("poeEnabled", ""),
            "type": port.get("type", ""),
            "vlan": port.get("vlan", ""),
            "speed": port.get("speed", ""),
            "duplex": port.get("duplex", ""),
            "status": port.get("status", "")
        })

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

def generate_switch_ports_csv(data_list, filename_prefix):
    """
    Genera un CSV flatten: una riga per ogni porta di ogni switch.
    """
    #Genero nome file con Timestamp YYYY-MM-DD
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{filename_prefix}_{timestamp}.csv"

   # 1 Raccogliamo TUTTE le chiavi presenti in TUTTI i dizionari
    fieldnames = set()
    for item in data_list:
        fieldnames.update(item.keys())
    fieldnames = list(fieldnames)

    # 2 Creazione CSV
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    # 3 Normalizzo ogni valore per il CSV
    for item in data_list:
        row = {}
        for key in fieldnames:
            value = item.get(key, "")
            # LISTA → separatore | se lista semplice
            if isinstance(value, list):
                if len(value) == 0:
                    row[key]=""
                elif all(isinstance(x, (str, int, float, bool)) for x in value):
                    # lista semplice → val1 | val2 | val3
                    row[key] = " | ".join(str(x) for x in value)
                else:
                    # lista di dict → JSON compatto
                    row[key] = json.dumps(value, separators=(',', ':'))
            # DICT → JSON compatto
            elif isinstance(value, dict):
                row[key] = json.dumps(value, separators=(',', ':'))
            else:
                # Valori già normali
                row[key] = value
        writer.writerow(row)
    output.seek(0)

    # 4️ Restituiamo il CSV come download
    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        download_name=filename,
        as_attachment=True
        )

def generate_switchesPorts_csv1(AllDevices_switchPorts, filename_prefix):
    """
    Genera un CSV con una riga per ogni porta di ogni switch.
    - AllDevices_switchPorts: lista di dict, ogni dict è un device che contiene (tra gli altri) la chiave 'ports' = [ {port}, ... ]
    - filename_prefix: prefisso per il nome file (es. "Meraki-Sw-")
    """

    # --- 1) Normalizziamo i campi device e individuiamo i campi "port" ---
    device_fieldnames = set()   # campi del device (senza 'ports')
    port_fieldnames = set()     # campi presenti in un port (assumiamo uniformità)

    for device in AllDevices_switchPorts:
        for k, v in device.items():
            if k == "ports":
                # se esiste almeno una porta, estraiamo i suoi campi per costruire le colonne delle porte
                if v and isinstance(v, list) and isinstance(v[0], dict):
                    for pk in v[0].keys():
                        port_fieldnames.add(pk)
            else:
                # Consideriamo campi device qualsiasi altro campo
                device_fieldnames.add(k)

    # Ordiniamo i fieldnames in modo prevedibile
    # Prediligiamo alcuni campi device comuni in testa (se esistono)
    preferred_device_order = ["network_name", "name", "switch_name", "serial", "model", "lanIp", "networkId", "address", "mac", "tags"]
    ordered_device_fields = [f for f in preferred_device_order if f in device_fieldnames]
    # poi aggiungiamo gli altri campi rimanenti
    ordered_device_fields += sorted(list(device_fieldnames - set(ordered_device_fields)))

    # Per le porte scegliamo un ordine logico comune
    preferred_port_order = ["portId", "name", "enabled", "poeEnabled", "type", "vlan", "speed", "duplex", "status", "profile"]
    ordered_port_fields = [f for f in preferred_port_order if f in port_fieldnames]
    ordered_port_fields += sorted(list(port_fieldnames - set(ordered_port_fields)))

    # Costruiamo fieldnames finali: campi device + campi port (prefissati con "port_" per chiarezza)
    csv_fieldnames = []
    for f in ordered_device_fields:
        # rinominiamo alcuni campi per uniformità: preferiamo "switch_name" al campo "name"
        if f == "name":
            csv_fieldnames.append("switch_name")
        else:
            csv_fieldnames.append(f)
    for pf in ordered_port_fields:
        csv_fieldnames.append(f"port_{pf}")  # es: port_portId, port_name, port_enabled

    # --- 2) Creazione buffer e writer CSV ---
    output = io.StringIO()
    # uso utf-8-sig per Excel (BOM) — però send_file richiederà l'encoding in bytes poi
    writer = csv.DictWriter(output, fieldnames=csv_fieldnames, extrasaction='ignore')
    writer.writeheader()

    # --- 3) Popolamento righe: una riga per ogni porta ---
    for device in AllDevices_switchPorts:
        # Prepara i valori device base (stabili per tutte le porte)
        device_row_base = {}
        for f in ordered_device_fields:
            # Mappa "name" -> "switch_name"
            raw_key = "name" if f == "switch_name" else f
            val = device.get(raw_key, "")

            # Se è lista e il campo è tags -> separatore |
            if isinstance(val, list):
                if raw_key.lower() == "tags":
                    device_row_base["tags"] = "|".join(str(x) for x in val)
                else:
                    # altre liste -> JSON string
                    device_row_base[raw_key] = json.dumps(val, ensure_ascii=False)
            else:
                # None -> ""
                device_row_base[raw_key if raw_key != "name" else "switch_name"] = "" if val is None else val

        # Recupera la lista porte (se non presente si scrive comunque una riga "vuota" con dati device e port_... vuoti)
        ports = device.get("ports")
        if not ports or not isinstance(ports, list):
            # nessuna porta: scriviamo comunque una riga con campi port vuoti
            row = {}
            # inseriamo i campi device (riscrivendo le chiavi come in csv_fieldnames)
            for key in ordered_device_fields:
                if key == "name":
                    row["switch_name"] = device_row_base.get("switch_name", "")
                else:
                    row[key] = device_row_base.get(key, "")
            # campi port vuoti
            for pf in ordered_port_fields:
                row[f"port_{pf}"] = ""
            writer.writerow(row)
            continue

        # Altrimenti cicliamo ogni porta e scriviamo una riga per ciascuna
        for p in ports:
            row = {}
            # Inseriamo campi device
            for key in ordered_device_fields:
                if key == "name":
                    row["switch_name"] = device_row_base.get("switch_name", "")
                else:
                    row[key] = device_row_base.get(key, "")

            # Inseriamo campi port prefissati
            for pf in ordered_port_fields:
                val = p.get(pf, "")
                # Se è lista -> JSON string (salvo tags speciali se ce ne fossero)
                if isinstance(val, list):
                    # se il campo si chiama 'tags' (rare nelle porte) usa '|', altrimenti JSON
                    if pf.lower() == "tags":
                        row[f"port_{pf}"] = "|".join(str(x) for x in val)
                    else:
                        row[f"port_{pf}"] = json.dumps(val, ensure_ascii=False)
                else:
                    # None -> ""
                    row[f"port_{pf}"] = "" if val is None else val

            writer.writerow(row)

    # --- 4) Preparazione file e restituzione ---
    output.seek(0)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{filename_prefix}{timestamp}.csv"

    # convertiamo in bytes con BOM utf-8-sig per Excel (opzionale)
    csv_bytes = output.getvalue().encode("utf-8-sig")
    return send_file(
        io.BytesIO(csv_bytes),
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )
 
def generate_switchesPorts_csv_Split(allDevices_switchPorts, filename_prefix):
    """
    Genera un CSV che contiene:
    - 1 riga PER OGNI PORTA
    - campi dello switch + campi della porta
    - tutte le liste convertite in "a|b|c"
    """

    # Nome file con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}{timestamp}.csv"

    output = io.StringIO()

    rows = []
    all_columns = set()

    # ─────────────────────────────────────────────────────────────
    # 1. ESPLODO GLI SWITCH: UNA RIGA PER OGNI PORTA
    # ─────────────────────────────────────────────────────────────
    for sw in allDevices_switchPorts:
        ports = sw.get("ports", [])

        # Per evitare errori, se non ci sono porte crea almeno una riga
        if not ports:
            ports = [{}]

        for p in ports:
            row = {}

            # Aggiungo tutti i campi dello switch
            for key, value in sw.items():
                if key != "ports":          # le porte sono gestite sotto
                    row[key] = normalize_value(value)
                    all_columns.add(key)

            # Esplodiamo completamente la porta con flatten_port_dict
            port_flat = {}
            flatten_port_dict("port_", p, port_flat)

            # Aggiungo al row
            for k, v in port_flat.items():
                row[k] = v
                all_columns.add(k)

            rows.append(row)

    # ─────────────────────────────────────────────────────────────
    # 2. ORDINO LE COLONNE PER COERENZA
    # ─────────────────────────────────────────────────────────────
    fieldnames = sorted(list(all_columns))

    # ─────────────────────────────────────────────────────────────
    # 3. SCRITTURA CSV
    # ─────────────────────────────────────────────────────────────
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for r in rows:
        writer.writerow(r)

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

def normalize_value(value):
    """
    Normalizza un valore qualunque per essere inserito nel CSV.
    - Stringhe → rimozione virgole
    - numeri → lasciati invariati
    - liste semplici (solo stringhe o numeri) → "a|b|c"
    - liste complesse → JSON compatto
    - dict → JSON compatto
    - None → stringa vuota
    """

    # None → campo vuoto
    if value is None:
        return ""

    # --- STRINGHE ---
    if isinstance(value, str):
        # Rimuove solo le virgole che creano problemi nel CSV
        return value.replace(",", " ")

    # Dizionario → converti in JSON compatto
    if isinstance(value, dict):
        return json.dumps(value, separators=(",", ":"))
        #return None

    # Lista
    if isinstance(value, list):
        # se tutti gli elementi sono stringhe o numeri: unisci con |
        if all(isinstance(x, (str, int, float)) for x in value):
            return "|".join(str(x) for x in value)

        # altrimenti lista complessa → converti JSON
        return json.dumps(value, separators=(",", ":"))

    # stringhe, numeri: restituisci come sono
    return value

def flatten_port_dict(prefix, data, result):
    """
    Esplode ricorsivamente un dict annidato dentro le porte.
    Esempio:
      profile = {"enabled": true, "id": "X"}
    genera:
      port_profile_enabled = True
      port_profile_id = X
    """
    for key, value in data.items():

        new_key = f"{prefix}{key}"

        if isinstance(value, dict):
            # Ricorsione = esplode ulteriormente
            flatten_port_dict(f"{new_key}_", value, result)

        elif isinstance(value, list):
            # liste → unite con |
            if all(isinstance(x,(str,int,float)) for x in value):
                result[new_key] = "|".join(str(x) for x in value)
            else:
                result[new_key] = json.dumps(value, separators=(",", ":"))

        elif isinstance(value, str):
            # stringhe senza virgole
            result[new_key] = value.replace(",", " ")

        elif value is None:
            result[new_key] = ""

        else:
            # numeri e bool
            result[new_key] = value


def generate_switchesPorts_csv2(allDevices_switchPorts, filename_prefix):
    """
    Genera un CSV che contiene:
    - 1 riga PER OGNI PORTA
    - campi dello switch + campi della porta
    - tutte le liste convertite in "a|b|c"
    """

    # Nome file con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{filename_prefix}{timestamp}.csv"

    output = io.StringIO()

    rows = []
    all_columns = set()

    # ─────────────────────────────────────────────────────────────
    # 1. ESPLODO GLI SWITCH: UNA RIGA PER OGNI PORTA
    # ─────────────────────────────────────────────────────────────
    for sw in allDevices_switchPorts:
        ports = sw.get("ports", [])

        # Per evitare errori, se non ci sono porte crea almeno una riga
        if not ports:
            ports = [{}]

        for p in ports:
            row = {}

            # Aggiungo tutti i campi dello switch
            for key, value in sw.items():
                if key != "ports":          # le porte sono gestite sotto
                    row[key] = normalize_value(value)
                    all_columns.add(key)

            # Esplodiamo completamente la porta con flatten_port_dict
            port_flat = {}
            flatten_port_dict("port_", p, port_flat)

            # Aggiungo al row
            for k, v in port_flat.items():
                row[k] = v
                all_columns.add(k)

            rows.append(row)

    # ─────────────────────────────────────────────────────────────
    # 2. ORDINO LE COLONNE PER COERENZA
    # ─────────────────────────────────────────────────────────────
    fieldnames = sorted(list(all_columns))

    # ─────────────────────────────────────────────────────────────
    # 3. SCRITTURA CSV
    # ─────────────────────────────────────────────────────────────
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for r in rows:
        writer.writerow(r)

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name=filename
    )

########### GENERA CSV PER OGNI SWITCH CON CONFIG PORTE - SERVONO QUESTE 2 FUNZIONI PERCHE DEVE CREARE UNO ZIP #########
def generate_single_switch_csv(sw, filename_prefix):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    switch_name = sw.get("name", sw.get("serial", "unknown"))
    filename = f"{filename_prefix}{switch_name}_{timestamp}.csv"

    output = io.StringIO()
    rows = []
    all_columns = set()

    ports = sw.get("ports", [])
    if not ports:
        ports = [{}]

    for p in ports:
        row = {}

        # campi switch
        for key, value in sw.items():
            if key != "ports":
                row[key] = normalize_value(value)
                all_columns.add(key)

        # campi porta (flatten)
        port_flat = {}
        flatten_port_dict("port_", p, port_flat)

        for k, v in port_flat.items():
            row[k] = v
            all_columns.add(k)

        rows.append(row)

    fieldnames = sorted(all_columns)
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for r in rows:
        writer.writerow(r)

    output.seek(0)
    return filename, output.getvalue()

def generate_switchesPorts_zip(allDevices_switchPorts, filename_prefix):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for sw in allDevices_switchPorts:
            filename, csv_content = generate_single_switch_csv(sw, filename_prefix)
            zipf.writestr(filename, csv_content)

    zip_buffer.seek(0)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"{filename_prefix}ALL_SWITCHES_{timestamp}.zip"

    return send_file(
        zip_buffer,
        mimetype="application/zip",
        as_attachment=True,
        download_name=zip_name
    )


def normalize_value(value):
    """
    Normalizza un valore qualunque per essere inserito nel CSV.
    - Stringhe → rimozione virgole
    - numeri → lasciati invariati
    - liste semplici (solo stringhe o numeri) → "a|b|c"
    - liste complesse → JSON compatto
    - dict → JSON compatto
    - None → stringa vuota
    """

    # None → campo vuoto
    if value is None:
        return ""

    # --- STRINGHE ---
    if isinstance(value, str):
        # Rimuove solo le virgole che creano problemi nel CSV
        return value.replace(",", " ")

    # Dizionario → converti in JSON compatto
    if isinstance(value, dict):
        return json.dumps(value, separators=(",", ":"))
        #return None

    # Lista
    if isinstance(value, list):
        # se tutti gli elementi sono stringhe o numeri: unisci con |
        if all(isinstance(x, (str, int, float)) for x in value):
            return "|".join(str(x) for x in value)

        # altrimenti lista complessa → converti JSON
        return json.dumps(value, separators=(",", ":"))

    # stringhe, numeri: restituisci come sono
    return value

def flatten_port_dict(prefix, data, result):
    """
    Esplode ricorsivamente un dict annidato dentro le porte.
    Esempio:
      profile = {"enabled": true, "id": "X"}
    genera:
      port_profile_enabled = True
      port_profile_id = X
    """
    for key, value in data.items():

        new_key = f"{prefix}{key}"

        if isinstance(value, dict):
            # Ricorsione = esplode ulteriormente
            flatten_port_dict(f"{new_key}_", value, result)

        elif isinstance(value, list):
            # liste → unite con |
            if all(isinstance(x,(str,int,float)) for x in value):
                result[new_key] = "|".join(str(x) for x in value)
            else:
                result[new_key] = json.dumps(value, separators=(",", ":"))

        elif isinstance(value, str):
            # stringhe senza virgole
            result[new_key] = value.replace(",", " ")

        elif value is None:
            result[new_key] = ""

        else:
            # numeri e bool
            result[new_key] = value