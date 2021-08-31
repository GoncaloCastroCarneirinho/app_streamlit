# -*- coding: utf-8 -*-
"""
Created on Thu May 20 23:15:09 2021

@author: scpgo
"""

import streamlit as st
from pygraphtec import  lee_fichero_sesion
from datetime import timedelta
import datetime

st.set_page_config(layout="wide") #EXPANSIÓN DE INTERFAZ GRÁFICA DE APLICACIÓN

df = lee_fichero_sesion("201112-180010.csv", path_sesiones='dataLogger') #LECTURA Y CREACIÓN DE DATAFRAME

seleccion_variables = st.multiselect("Select variable: ", df.columns.tolist()) #FILTRO PARA SELECCIÓN DE VARIABLES
       
column_1, column_2 = st.beta_columns([1,1]) #ESTRUCTURA POR COLUMNAS PARA FILTRO DE RANGO DE FECHAS

#FILTRO DE RANGO DE FECHAS
fecha_inicial = column_1.date_input('Start date:', df.index.min(), df.index.min(), datetime.date.today()) #FECHA INICIAL
fecha_final = column_2.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today()) #FECHA FINAL
    
filtered_df_date = df.loc[fecha_inicial:fecha_final] #FILTRO DE DATAFRAME POR RANGO DE FECHAS

st.line_chart(filtered_df_date[seleccion_variables])