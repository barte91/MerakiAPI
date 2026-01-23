from flask import jsonify
import os,io,zipfile,csv
from Function.FuncFILE import Func_PY_FILE as FuncFILE

# FUNZIONI SU SISTEMA WINDOWS

def getFileName(total_path):
    list_fn=[]
    for path in os.listdir(total_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(total_path, path)):
            list_fn.append(path)
    return list_fn

#Gestione ZIP File caricati (Per LM-Catalyst - to - Meraki)
def handle_zip_upload(file):
    zip_bytes = io.BytesIO(file.read())
    csv_files = []
    with zipfile.ZipFile(zip_bytes) as z:
        for name in z.namelist():
            if name.lower().endswith('.csv'):
                csv_files.append(name)
                content = z.read(name).decode("utf-8")

                reader = csv.DictReader(io.StringIO(content))
                rows = list(reader)

                # QUI fai quello che vuoi con i dati
                print(f"{name} → {len(rows)} righe")
    return jsonify({
        "status": "ok",
        "csv_files": csv_files
    })

#Gestione CSV File caricati (Per LM-Catalyst - to - Meraki)
def handle_csv_upload(file,dry_run):
    content = file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    rows = list(reader)
    return FuncFILE.LM_CatMeraki_apply_ports_config_advanced(rows,dry_run)
    #return FuncFILE.LM_CatMeraki_apply_ports_config(rows)
    #SOLO PER TEST
    #rows = list(reader)
    #return jsonify({
    #    "status": "ok",
    #    "rows_received": len(rows)
    #})
    