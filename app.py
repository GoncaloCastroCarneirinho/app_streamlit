# -*- coding: utf-8 -*-
"""
Created on Mon May 10 15:17:03 2021

@author: scpgo
"""

import streamlit as st

from pygraphtec import  lee_fichero_sesion

import pandas as pd

from collections import deque

from datetime import timedelta

import time

import datetime

from lectura_equipos import lee_meteo

import base64

st.set_page_config(layout="wide")

#df = lee_fichero_sesion("201112-165432.csv", path_sesiones='dataLogger')#Se ejecuta la función
df_datalogger = lee_fichero_sesion("201112-180010.csv", path_sesiones='dataLogger') #DATAFRAME DE DE FICHERO DATALOGGER
df_meteo =  lee_meteo(pd.date_range(start='2020/11/12', end='2020/11/16', freq='10T'),path_estacion="dataLogger/") #DATAFRAME DE FICHERO METEO

df_meteo = lee_meteo(df_datalogger.index.round('T'),path_estacion="dataLogger/")
df_meteo.index = df_datalogger.index

df = pd.concat([df_datalogger,df_meteo], axis=1) #CONCATENACIÓN DE DATAFRAMES

# img1_col, view_mode_col, col1, col2, img2_col = st.beta_columns([1,5,16,16,1]) #Estructura superior de las vistas de la app en columnas
col_logo1, view_mode_col, col1, col2, col_logo2 = st.beta_columns([2,2,4.9,4.9,1.5]) #ESTRUCTURA DE LA APP POR COLUMNAS PARA ELECCIÓN DE MODALIDAD DE VISTA Y VARIABLES A SELECCIONAR

i=0

view_mode = view_mode_col.radio("SELECT VIEW MODE", ('Live', 'Resume', 'Data Table')) #MODALIDAD DE APP A SELECCIONAR

st.markdown( #IMAGEN DE FONDO DE LA APP
    f"""
    <style>
    .reportview-container {{
        background-size: 100% 100%;
        background-color: rgba(21,159,228,0.90);
        background-blend-mode: lighten;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

with col_logo2: #IMAGEN DE LA UPM EN LA INTERFAZ
    st.image("upm-light_2.png", use_column_width=True)
    
with col_logo1: #IMAGEN DEL IES-UPM EN LA INTERFAZ
    st.image("IES_2.png", use_column_width=True)

if view_mode == 'Live': #MODALIDAD LIVE
       
    variables_seleccion = col2.multiselect("", df.columns.tolist()) #SELECCIÓN DE MAGNITUDES A REPRESENTAR
    
    sidebar_live = st.sidebar #CREACIÓN DE VENTANA DESPLEGABLE A LA IZQUIERDA
    
    sidebar_live.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>LIVE DATASET", unsafe_allow_html=True,) #TITULO DE INFORMACIÓN EN LA VENTANA DESPLEGABLE
    
    for col in variables_seleccion:
        sidebar_live.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #INFORMACIÓN EN LA VENTANA DESPLEGABLE

    col1.markdown("""<p style='display: block; height:100px; line-height:100px; text-align: center; align: center; font-size: 25px; font-family: calibri; font-weight: bold'>SELECT DATASET TO PLOT</p>""", unsafe_allow_html=True,) #'SELECCIONAR VARIABLES A REPRESENTAR EN MODO LIVE'

    data_collection = deque() #coleccion creada para su relleno con valores de los datos del dataframe
    time_collection = deque() #coleccion creada para su relleno con informacion de fecha y hora del dataframe
    
    i=0

    status_text=st.empty() #CREACION DE VARIABLE CON VALOR ACTUALIZABLE PERMANENTEMENTE
    
    while True: #COMIENZO DEL BUCLE PARA ACTUALIZACIÓN CONTINUA DEL GRÁFICO
        
        j=0
        
        if(i<(len(df)-1)):
            i=i+1
            
        data_collection.append(df[variables_seleccion].values[i]) #RELLENO DE LAS COLECCIONES CON VALORES DE DATOS DEL DATAFRAME
        time_collection.append(df.index[i]) #RELLENO DE LAS COLECCIONES CON INFORMACIÓN DE FECHA Y HORA DEL DATAFRAME
        
        chart_dataframe = pd.DataFrame( #CREACIÓN DE NUEVO DATAFRAME PARA LA REPRESENTACIÓN GRÁFICA EN TIEMPO REAL
             data_collection, #VALORES DE LOS DATOS DEL DATAFRAME
             index = time_collection, #FILAS O ÍNDICE DEL DATAFRAME
             columns = variables_seleccion #COLUMNAS DEL DATAFRAME
             )
        
        table_dataframe = pd.DataFrame( #CREACIÓN DE NUEVO DATAFRAME PARA LA REPRESENTACIÓN EN TABLA EN TIEMPO REAL
            [df[variables_seleccion].values[i]], #VALORES DE LOS DATOS DEL NUEVO DATAFRAME
            index = ["At: " + df.index[i].strftime('%d/%m/%y - %H:%M:%S')], #FILAS O ÍNDICE DEL NUEVO DATAFRAME
            columns = variables_seleccion #columnas del dataframe
            )
        
        if(variables_seleccion is None or len(variables_seleccion)==0): 
            time.sleep(1) #TIEMPO NECESARIO PARA QUE LA APLICACIÓN ARRANQUE SIN DAR ERROR DE 'EMPTY CHART'
            chart = st.line_chart({}) #GRÁFICO VACÍO SI NO SE HA SELECCIONADO INFORMACIÓN A REPRESENTAR
        else:
            chart = st.line_chart(chart_dataframe) #VARIABLES DEL DATAFRAME 'chart_dataframe', SELECCIONADAS Y REPRESENTADAS EN GRÁFICO
            status_text.table(table_dataframe.style.set_properties(**{'font-size': '15px','text-align': 'right'}).set_precision(2)) #VARIABLES DATAFRAME 'table_dataframe' SELECCIONADAS Y REPRESENTADAS EN TABLA
            
            for j in range(1):
                time.sleep(1) #tiempo de actualizacion del gráfico (simulacion de tiempo real)
                st.empty() #por revisar
                
            chart.empty() #vacío de gráfico despues al actualizar
            chart.empty() #vacío de gráfico despues al actualizar        

elif view_mode == 'Resume': #MODALIDAD 'RESUME'
    
    first_variables_set_selected_resume = col1.multiselect("SELECT FIRST SET OF VARIABLES", df.columns.tolist()) #SELECCION DE VARIABLES A REPRESENTAR EN GRÁFICA 1
    
    second_variables_set_selected_resume = col2.multiselect("SELECT SECOND SET OF VARIABLES", df.columns.tolist()) #SELECCION DE VARIABLES A REPRESENTAR EN GRÁFICA 2
    
    #VENTANA INFORMATIVA DESPLEGABLE A LA IZQUIERDA
    
    sidebar_resume = st.sidebar #CREACIÓN DE VENTANA DESPLEGABLE

    sidebar_col1, sidebar_col2 = sidebar_resume.beta_columns([1,1]) #ESTRUCTURACIÓN, POR COLUMNAS, DE VENTANA DESPLEGABLE
    
    sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>DATASET 1", unsafe_allow_html=True,) #TÍTULO 1 DE INFORMACIÓN A PUBLICAR EN VENTANA DESPLEGABLE

    sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>DATASET 2", unsafe_allow_html=True,) #TÍTULO 2 DE INFORMACIÓN A PUBLICAR EN VENTANA DESPLEGABLE

    #FILTRO DE SETS ALTERNATIVOS DE DATOS A REPRESENTAR GRAFICAMENTE

    col1_vacia, empty_column_1, first_set_selection_col, second_set_selection_col, col2_vacia = st.beta_columns([2,2,4.9,4.9,1.5]) #ESTRUCTURACIÓN DEL FILTRO DE SELECCIÓN DE SETS DE DATOS

    with first_set_selection_col: #FILTRO PARA GRÁFICO 1
        
        with st.beta_expander("Pick a dataset to plot:"): #CREACIÓN DE FILTRO O PESTAÑA DESPLEGABLE PARA GRÁFICO 1
            
            set_option_1 = st.selectbox('', ['FIRST DATASET ALREADY SELECTED','FIRST TEMPERATURE DATASET','FIRST HUMIDITY DATASET']) #OPCIONES DE SETS DE DATOS A REPRESENTAR EN GRÁFICO 1

            if set_option_1 == "FIRST DATASET ALREADY SELECTED":
                df_set_filter_1 = df[first_variables_set_selected_resume]
                for col in df_set_filter_1:
                    sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA DESPLEGABLE, DE SET DE DATOS SELECCIONADO

            elif set_option_1 == "FIRST TEMPERATURE DATASET":
                df_set_filter_1 = df[[item for item in df.columns if 'TEMP' in item]] #DATAFRAME INICIAL, FILTRADO POR TEMPERATURAS SEGÚN SET PREDETERMINADO DE TEMPERATURAS
                for col in df_set_filter_1.columns:
                    sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA DESPLEGABLE, DE SET DE TEMPERATURAS PREDETERMINADO
            
            elif set_option_1 == "FIRST HUMIDITY DATASET":
                df_set_filter_1 = df[[item for item in df.columns if 'RH' in item]] #DATAFRAME INICIAL, FILTRADO POR TEMPERATURAS SEGÚN SET PREDETERMINADO DE HUMEDADES
                for col in df_set_filter_1.columns:
                    sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA DESPLEGABLE, DE SET DE HUMEDADES PREDETERMINADO
  
    with second_set_selection_col:
            
        with st.beta_expander("Pick a dataset to plot:"): #CREACIÓN DE FILTRO O PESTAÑA DESPLEGABLE PARA GRÁFICO 2
            
            set_option_2 = st.selectbox('', ['SECOND DATASET ALREADY SELECTED','SECOND TEMPERATURE DATASET','SECOND HUMIDITY DATASET']) #OPCIONES DE SETS DE DATOS A REPRESENTAR EN GRÁFICO 2
            
            if set_option_2 == "SECOND DATASET ALREADY SELECTED":
                df_set_filter_2 = df[second_variables_set_selected_resume] #DATAFRAME INICIAL, FILTRADO POR TEMPERATURAS SEGÚN SET DE VARIABLES SELECCIONADO MANUALMENTE POR USUARIOS
                for col in df_set_filter_2:
                    sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA DESPLEGABLE, DE SET DE DATOS SELECCIONADO

            elif set_option_2 == "SECOND TEMPERATURE DATASET":
                df_set_filter_2 = df[[item for item in df.columns if 'TEMP' in item]] #DATAFRAME INICIAL, FILTRADO POR TEMPERATURAS SEGÚN SET PREDETERMINADO DE TEMPERATURAS
                for col in df_set_filter_2.columns:
                    sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA DESPLEGABLE, DE SET DE TEMPERATURAS PREDETERMINADO
            
            elif set_option_2 == "SECOND HUMIDITY DATASET":
                df_set_filter_2 = df[[item for item in df.columns if 'RH' in item]] #DATAFRAME INICIAL, FILTRADO POR TEMPERATURAS SEGÚN SET PREDETERMINADO DE HUMEDADES
                for col in df_set_filter_2.columns:
                    sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA DESPLEGABLE, DE SET DE HUMEDADES PREDETERMINADO
    
    #FILTRO DE RANGO DE FECHAS                
    
    titulo_filtro_fechas, fecha_inicial, fecha_final = st.beta_columns([1,2,2]) #ESTRUCTURA DE FILTRO POR FECHAS
    
    titulo_filtro_fechas.markdown("<p style='display: block; height: 0px; line-height:115px; text-align: justify; font-size: 25px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</p>", unsafe_allow_html=True,) #TITULO DE FILTRO POR FECHAS
        
    fecha_inicio_resume = fecha_inicial.date_input('Start date:', df.index.min(), df.index.min(), df.index.max()) #SELECCIÓN DE FECHA INICIAL
    
    fecha_fin_resume = fecha_final.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today()) #SELECCIÓN DE FECHA FINAL

    #REPRESENTACIÓN GRÁFICA DEL DATAFRAME CON LOS SETS DE DATOS ELEGIDOS
    
    col1, col_vacia, grafico1_resume, grafico2_resume, col1 = st.beta_columns([2,2,4.9,4.9,1.5]) #ESTRUCTURA DE REPRESENTACIÓN GRÁFICA
    
    df_filter_chart1=df_set_filter_1.loc[fecha_inicio_resume:fecha_fin_resume] #DATAFRAME FILTRADO POR FECHAS (GRÁFICO 1) - LLAMADA A LA FUNCIÓN
    
    df_filter_chart2=df_set_filter_2.loc[fecha_inicio_resume:fecha_fin_resume] #DATAFRAME FILTRADO POR FECHAS (GRÁFICO 2) - LLAMADA A LA FUNCIÓN
    
    #chart1_title = grafico1_resume.markdown("<p style='display: block; text-align: center; font-size: 15px; font-family: calibri; font-weight: bold'>DATASET 1 RESUME</p>", unsafe_allow_html=True,) #TÍTULO DE GRÁFICO 1
    
    Data_chart1 = grafico1_resume.empty() #CREACIÓN DE GRÁFICO 1, INICIALMENTE VACÍO
    
    Data_chart01 = Data_chart1.line_chart(df_filter_chart1) #REPRESENTACIÓN GRÁFICA DE DATAFRAME 1

    #chart2_title = grafico2_resume.markdown("<p style='display: block; text-align: center; font-size: 15px; font-family: calibri; font-weight: bold'>DATASET 2 RESUME</p>", unsafe_allow_html=True,)
    
    Data_chart2 = grafico2_resume.empty() #CREACIÓN DE GRÁFICO 2, INICIALMENTE VACÍO
    
    Data_chart02 = Data_chart2.line_chart(df_filter_chart2) #REPRESENTACIÓN GRÁFICA DE DATAFRAME 2
     
elif view_mode == 'Data Table':
    
    #FILTRO DE SELECCIÓN DE VARIABLES
    
    col1.markdown("""<a style='display: block; height:100px; line-height:100px; text-align: center; font-size: 25px; font-family: calibri; font-weight: bold'>SELECT DATASET TO PUBLISH ON TABLE</a>""", unsafe_allow_html=True,) #TÍTULO DEL FILTRO DE SELECCIÓN DE VARIABLES A REPRESENTAR
    
    variables_set_selected_live = col2.multiselect(" ", df.columns.tolist()) #SELECCIÓN DEL SET DE VARIABLES A REPRESENTAR EN MODO TABLA

    #FILTRO DE RANGO DE FECHAS

    titulo_filtro_fechas, fecha_inicial, fecha_final = st.beta_columns([1,2,2]) #ESTRUCTURA DEL FILTRO DE RANGO DE FECHAS
    
    titulo_filtro_fechas.markdown("""<a style='display: block; height:115px; line-height:115px; text-align: center; font-size: 25px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</a>""", unsafe_allow_html=True,) #TíTULO DE FILTRO DE RANGO DE FECHAS
    
    fecha_inicio_table = fecha_inicial.date_input('Start date:', df.index.min(), df.index.min(), df.index.max()) #SELECCIÓN DE FECHA INICIAL
    
    fecha_fin_table = fecha_final.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today()) #SELECCIÓN DE FECHA FINAL

    #REPRESENTACIÓN EN MODO TABLA DEL DATAFRAME CON EL SET DE DATOS ELEGIDO
    
    df_filtered_table=df.loc[fecha_inicio_table:fecha_fin_table] #DATAFRAME FILTRADO POR FECHAS (GRÁFICO 1) - LLAMADA A LA FUNCIÓN
    
    df_filtered_table.index=df_filtered_table.index.strftime("%d/%m/%y\n%H:%M:%S")
    
    if len(variables_set_selected_live)>0:
        data_table = st.table(df_filtered_table[variables_set_selected_live].style.set_precision(2)) #CREACIÓN DE TABLA CON VALORES DE MAGNITUDES SELECCIONADAS Y CON PRECISIÓN DE 2 DECIMALES