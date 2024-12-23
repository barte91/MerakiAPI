import pymysql
from operator import itemgetter
from datetime import date,datetime
from config import db_host, db_port, db_user, db_pwd, db_name


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