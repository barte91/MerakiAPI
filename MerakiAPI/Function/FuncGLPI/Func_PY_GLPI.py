import pandas as pd
import os
from Function.FuncDB.Func_PY_DB import *
from Function.FuncExcel.Func_PY_Excel import *
from config import InveManu_path


def APP_GLPI_InveManu(entities,location,state):
    #Read Variable passed on form
    user_location=location
    user_entities=entities
    user_state=state
    #dataframe di Test
    data = [
        {'Location': user_location, 'Entity': user_entities, 'State': user_state}
    ]
    df=pd.DataFrame(data)
    #Salva DF in file Excel
    df.to_excel(InveManu_path, index=False, engine='openpyxl')
    #Restituisci percorso del file Excel
    return InveManu_path
    #Extract array from query on GLPI DB
    #arrEntities=Func_PY_DB.CopiaCampiDB("SELECT * FROM glpi_entities",1,0)