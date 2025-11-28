from consolemenu import ConsoleMenu,SelectionMenu
from consolemenu.items import FunctionItem
from Inventario import *
from UpdatePorts import *
from ChangeIP import *
from Tools import *


if __name__ == '__main__':
    menu = ConsoleMenu("Scegli Operazione da eseguire")
    #Scelte disponibili
    item_inventarioByOrg = FunctionItem("Inventario Porte Enable Down 1 Mese - By Organization", get_invetario,[URL,APIKEY,orgID,xls_path_inv])
    item_inventarioByNtw = FunctionItem("Inventario Porte Enable Down 1 Mese - By Network", get_invetarioByNetwork,[URL,APIKEY,orgID,xls_path_inv])
    item_updateportsByFnNtw = FunctionItem("UpdatePorts By File & Network Name", set_UpdateportsByFile_and_NwName,[URL,APIKEY,orgID,xls_path])
    item_updateportsByFnNtw_v2Template = FunctionItem("V2-Template-UpdatePorts By File & Network Name", set_V2_UpdateportsByFile_and_NwName_withTemplate,[URL,APIKEY,orgID,xls_path])
    item_updateportsByFn = FunctionItem("UpdatePorts By File", set_UpdateportsByFile,[URL,APIKEY,orgID,xls_path])
    item_changeIPByFn = FunctionItem("Change IP By File", set_ChangeIP_ByFile,[URL,APIKEY,orgID,xls_path_chgIP])
    item_createSSID = FunctionItem("Create SSID", lambda: CreateSSID(URL,APIKEY,json_script_path))
    item_ONLYTEST = FunctionItem("TEST", lambda: CreateSSID(URL,APIKEY,json_script_path))
    #Creazione Menù
    menu.append_item(item_inventarioByOrg)
    menu.append_item(item_inventarioByNtw)
    menu.append_item(item_updateportsByFnNtw)
    menu.append_item(item_updateportsByFnNtw_v2Template)
    menu.append_item(item_updateportsByFn)
    menu.append_item(item_changeIPByFn)
    menu.append_item(item_createSSID)
    menu.append_item(item_ONLYTEST)
    menu.show()