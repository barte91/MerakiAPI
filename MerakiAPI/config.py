#Carica variabili con password
from dotenv import load_dotenv
load_dotenv()

import os

#MERAKI
URL = os.getenv("MERAKI_API_URL")
HEADER = os.getenv("MERAKI_API_HEADER")
KEY = os.getenv("MERAKI_KEY")
APIKEY = {HEADER: KEY}

#ZABBIX
ZABURL = os.getenv("ZABBIX_API_URL")
ZABKEY = os.getenv("ZABBIX_KEY")
ZABHEADERS = {
    "Authorization": f"Bearer {ZABKEY}",
    "Content-Type": "application/json-rpc"
}


xls_path_inv = os.getenv("xls_path_inv")
xls_path_chgIP = os.getenv("xls_path_chgIP")
xls_path = os.getenv("xls_path")
json_script_path = os.getenv("json_script_path")

# VARIABLE DB
db_host= os.getenv("db_host")
db_port= os.getenv("db_port")
db_user= os.getenv("db_user")
db_pwd= os.getenv("db_pwd")
db_name= os.getenv("db_name")

#VARIBAILI NOMI FILE EXCEL
InveManu_nameFile=os.getenv("InveManu_nameFile")

#COLORI EXCEL
ExOrange=os.getenv("ExOrange")
ExBlack=os.getenv("ExBlack")

