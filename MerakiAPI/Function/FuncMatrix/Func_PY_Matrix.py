import pymysql, openpyxl, sys, shutil,os
import pandas as pd
from openpyxl import Workbook, worksheet, styles
from openpyxl.styles import Font, Border, Alignment, Color, Side,PatternFill, NamedStyle
from openpyxl.worksheet.dimensions import ColumnDimension
from openpyxl.worksheet.cell_range import CellRange
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows
from operator import itemgetter
from datetime import date,datetime
import random

#FUNZIONI PER ARRAY-MATRICI

def FindElemMatrix(matrix,elem,index_to_find,index_to_return):
    count=0
    for x in matrix:
        if(matrix[count][index_to_find]==elem):
            elem_find=matrix[count][index_to_return]
            return elem_find
        count=count+1
    elem_find='empty'
    return elem_find

#This function convert cod form MultiSelectBox to name (Entities,state...)
def ConvertArray(arrayUser,arrQuery):
    arrName=[]
    arrName=[0]
    count=0
    for x in arrayUser:
        cod=int(x)
        name=FindElemMatrix(arrQuery,cod,0,1)
        if count!=0:
            arrName.append([0])
        arrName[count]=name
        count=count+1
    return arrName

def ExtractMatrix_2_index(arrayTotale,index1,index2):
    arrModels=[[],[]]
    lunghezza=len(arrayTotale)
    arrModels=[[0]*2]
    i=0
    for x in arrayTotale:                      #ciclo con cui si crea l'array 2D - colonna 0 = Tipo 1 = Modello
         if i!=0:                           #se i è diverso da 0 aggiuno altro elemento
            arrModels.append([0]*2)
         arrModels[i][0]=arrayTotale[i][index1]
         arrModels[i][1]=arrayTotale[i][index2]
         i=i+1
    #arrModels.sort(key=itemgetter(0))       #ordina Array secondo il tipo
    return arrModels

def DeleteDuplicateMatrix(matrix,index_to_check,index2):
    matrixFinal=[[],[]]
    count=0
    count_final=0
    matrix.sort(key=itemgetter(index_to_check))
    matrixFinal=[[0]*2]
    lungh=len(matrix)-1
    for x in matrix:
        if count!=lungh:
            if(matrix[count][index_to_check]!=matrix[count+1][index_to_check]):
                if (count_final!=0):
                    matrixFinal.append([0]*2)
                matrixFinal[count_final][index_to_check]=matrix[count][index_to_check]
                matrixFinal[count_final][index2]=matrix[count][index2]
                count_final=count_final+1
            count=count+1
        else:
            #if(matrix[count][index_to_check]!=matrix[count-1][index_to_check]):
                matrixFinal.append([0]*2)
                matrixFinal[count_final][index_to_check]=matrix[count][index_to_check]
                matrixFinal[count_final][index2]=matrix[count][index2]
    return matrixFinal

# FUNZIONE SEARCH
def SearchElemArray(elem,array):
    i=0
    elem=elem[0]
    for x in array:
        name=array[i][1]
        cod=array[i][0]
        if(elem==name):
            found=1
            return cod
        i=i+1
    found=0
    return found

# FUNZIONE SEARCH
#-----deprecated----
def SearchElemArrayNew(elem,array):

    # Verifica se l'elemento è presente
    if elem in array:
        # Trova l'indice dell'elemento
        index = array.index(elem)
        # Restituisci l'elemento con indice 0
        cod = array[index - 1]  # Torna l'elemento alla sua sinistra (indice 0)
        return 1
    else:
        return 0

