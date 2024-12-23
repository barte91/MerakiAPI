from Function.FuncDB.Func_PY_DB import *
from Function.FuncExcel.Func_PY_Excel import *


def APP_GLPI_InveManu(entID,negoID,List_states):
    a=0
    #db_conn=connetti_db()

def TEST():
    #Read Variable passed on form
    user_location=location
    user_entities=entities
    user_state=state
    #Extract array from query on GLPI DB
    arrEntities=Func_PY_DB.CopiaCampiDB("SELECT * FROM glpi_entities",1,0)