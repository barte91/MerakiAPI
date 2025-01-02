import pymysql
from operator import itemgetter
from datetime import date,datetime
from config import db_host, db_port, db_user, db_pwd, db_name
from Function.FuncMatrix import Func_PY_Matrix as FuncMatrix


# FUNZIONI PER DATABASE

def connetti_db():
    myDB = pymysql.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name
    )
    return myDB

def CloseConnectionDB(myDB):
    myDB.close()

def CommitDB(myDB):
    myDB.commit()

def createCursorDB(myDB):
    cursor=myDB.cursor()
    return cursor

def CloseCursorDB(cursor):
    cursor.close()

def exec_queryCursorDB(cursor,query,value1,value2):
    cursor.execute(query, (value1, value2))

def close_db(myDB):
    myDB.close()


def exec_query(myDB,query):
    cHandler=myDB.cursor()
    cHandler.execute(query)
    results=cHandler.fetchall()
    return results

def CopiaCampiDB(query,index_secondary_key,index_primary_key):
    secondary_key=[]
    primary_key=[]
    arrDB=[[],[]]
    #operation on GLPI DB
    myDB=connetti_db()
    res_query=exec_query(myDB,query)
    for row in res_query:
        secondary_key.append(row[index_secondary_key])
        primary_key.append(row[index_primary_key])
    close_db(myDB)
    #operation to create array Lista
    lung=len(secondary_key)
    arrDB=[[0]*2]
    i=0
    while i<lung:                      #ciclo con cui si crea l'array 2D - colonna 0 = id colonna 1 = nome
         if i!=0:                      #se i è diverso da 0 aggiuno altro elemento
            arrDB.append([0]*2)
         arrDB[i][1]=secondary_key[i]
         arrDB[i][0]=primary_key[i]
         i=i+1
    arrDB.sort(key=itemgetter(0))      #ordina Array con key la seconda colonna (itemgetter(1))
    return arrDB

def CopiaCampiDB_Filtered(query,index_secondary_key,index_primary_key,filtered_id):
    secondary_key=[]
    primary_key=[]
    arrDB=[[],[]]
    #operation on GLPI DB
    myDB=connetti_db()
    res_query=exec_query(myDB,query)
    for row in res_query:
        secondary_key.append(row[index_secondary_key])
        primary_key.append(row[index_primary_key])
    close_db(myDB)
    #operation to create array Lista
    lung=len(secondary_key)
    arrDB=[[0]*2]
    i=0
    while i<lung:                      #ciclo con cui si crea l'array 2D - colonna 0 = id colonna 1 = nome
         if i!=0:                      #se i è diverso da 0 aggiuno altro elemento
            arrDB.append([0]*2)
         arrDB[i][1]=secondary_key[i]
         arrDB[i][0]=primary_key[i]
         i=i+1
    arrDB.sort(key=itemgetter(0))      #ordina Array con key la seconda colonna (itemgetter(1))
    return arrDB

def CreateAddQuery(arrElem):
    #query1="SELECT * FROM glpi_networkequipments INNER JOIN glpi_entities ON glpi_networkequipments.entities_id=glpi_entities.id WHERE glpi_entities.name 
    #LIKE '%" + ent + "%' AND glpi_networkequipments.is_template='0'"
    add_query=''
    count=0
    for x in arrElem:
        elem=x
        if count==0:
            add_query="glpi_entities.name LIKE '%" + elem + "%'"
        else:
            add_query=add_query+" OR glpi_entities.name LIKE '%" + elem + "%'"
        count=count+1
    return add_query

def CopiaRisQuery_14_filed(query,ind_id,ind_loc,ind_desc,ind_stato,ind_tipo,ind_vendor,ind_modello,ind_ent,arrLoc,arrState,arrType,arrVendor,arrModels,arrEnt):
    ID=[]
    location_id=[]
    location_name=[]
    desc=[]
    stato_id=[]
    stato_name=[]
    tipo_id=[]
    tipo_name=[]
    vendor_id=[]
    vendor_name=[]
    modello_id=[]
    modello_name=[]
    ent_id=[]
    ent_name=[]
    arrDB=[[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    count=0
    #operation on GLPI DB
    myDB=connetti_db()
    res_query=exec_query(myDB,query)
    for row in res_query:
        ID.append(row[ind_id])
        location_id.append(row[ind_loc])
        location_name.append(FuncMatrix.FindElemMatrix(arrLoc,location_id[count],0,1))
        desc.append(row[ind_desc])
        stato_id.append(row[ind_stato])
        stato_name.append(FuncMatrix.FindElemMatrix(arrState,stato_id[count],0,1))
        tipo_id.append(row[ind_tipo])
        tipo_name.append(FuncMatrix.FindElemMatrix(arrType,tipo_id[count],0,1))
        vendor_id.append(row[ind_vendor])
        vendor_name.append(FuncMatrix.FindElemMatrix(arrVendor,vendor_id[count],0,1))
        modello_id.append(row[ind_modello])
        modello_name.append(FuncMatrix.FindElemMatrix(arrModels,modello_id[count],0,1))
        ent_id.append(row[ind_ent])
        ent_name.append(FuncMatrix.FindElemMatrix(arrEnt,ent_id[count],0,1))
        count=count+1
    close_db(myDB)
    #operation to create array Lista
    lung=len(ID)
    arrDB=[[0]*14]
    i=0
    while i<lung:                      #ciclo con cui si crea l'array
         if i!=0:                      #se i è diverso da 0 aggiuno altro elemento
            arrDB.append([0]*14)
         arrDB[i][0]=ID[i]
         arrDB[i][1]=location_id[i]
         arrDB[i][2]=location_name[i]
         arrDB[i][3]=desc[i]
         arrDB[i][4]=stato_id[i]
         arrDB[i][5]=stato_name[i]
         arrDB[i][6]=tipo_id[i]
         arrDB[i][7]=tipo_name[i]
         arrDB[i][8]=vendor_id[i]
         arrDB[i][9]=vendor_name[i]
         arrDB[i][10]=modello_id[i]
         arrDB[i][11]=modello_name[i]
         arrDB[i][12]=ent_id[i]
         arrDB[i][13]=ent_name[i]
         i=i+1
    arrDB.sort(key=itemgetter(0))      #ordina Array con key la seconda colonna (itemgetter(1))
    return arrDB

# FUNZIONI DB - GLPI

def fetch_Settings_GLPI(query, index_primary_key, index_secondary_key):
    arrData = CopiaCampiDB(query, index_secondary_key, index_primary_key)
    return arrData