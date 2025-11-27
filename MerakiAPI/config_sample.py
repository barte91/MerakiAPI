import os

URL = os.getenv("MERAKI_API_URL")
APIKEY = os.getenv("MERAKI_API_KEY")
KEY = os.getenv("MERAKI_KEY")

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