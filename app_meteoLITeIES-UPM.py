# -*- coding: utf-8 -*-
"""
Created on Mon May 10 15:17:03 2021

@author: scpgo
"""

import streamlit as st
import pandas as pd
from collections import deque
from datetime import timedelta
import time
import datetime
from pygraphtec import lee_fichero_sesion, lee_ultimos_datos
from lectura_equipos import lee_meteo
from pygeonica.estacion import lee_canales
import glob

#CONFIGURACIÓN DE PÁGINA WEB E INTERFAZ
st.set_page_config(page_title='meteoLITeIES-UPM', page_icon='ies-upm_page_config.jpg', layout="wide")

#FONDO DE INTERFAZ DE PÁGINA WEB
st.markdown(f"""<style>.reportview-container {{ 
        background-size: 100% 100%;
        background-color: rgba(21,159,228,0.90);
        background-blend-mode: lighten;
        }}</style>""",
        unsafe_allow_html=True)

#DERECHOS DE IMAGEN DE LA APLICACIÓN WEB
st.markdown("""<style>footer {
        display:block; 
        text-align:center;
        }
                      footer:after {
        content:'© 2021 All rights reserved. Universidad Politécnica de Madrid'; 
        visibility:visible; 
        display:block; 
        text-align:center;
        font-size:11px;
        color:white;
        }</style>""", 
        unsafe_allow_html=True)

# #TRATAMIENTO DE DATOS DE ESTACIONES METEOROLÓGICAS Y MÓDULOS FOTOVOLTAICOS DEL IES-UPM
# #GENERACIÓN DE DATAFRAMES DE DATOS - CON CONEXIÓN A RED DEL IES-UPM (MODALIDAD LIVE)
def lee_meteo_live(): #FUNCIÓN PARA CONECTAR A LA RED Y AGRUPAR DATOS OBTENIDOS
    # Diccionario con los nombres de las variables que se desean modificar. Nombre en la estacion: Nombre que se desea que tenga la variable en el fichero generado
    NOMBRES_METEO = {
        "Estado" : 'Limpieza',
        "PIRAN.1" : 'Gh',                  # Global Horizontal
        "PIRAN.2" : 'Dh',                  # Difusa Horizontal
        "PIRAN.3" : 'G(41)',               # Global 41ยบ
        "PIRAN.4" : 'Gn',                  # Global Normal
        "R.Directa1" : 'Bn',               # Directa Normal
        "R.Directa2" : 'Bn_2',             # Directa Normal 2
        "R.Infr.Inc" : 'Pirgeo',           # Pirgeometro
        "T.Carcasa" : 'Temp_Pirgeo',       # Temperatura Carcasa Pirgeometro
    }
    dd = {}
    for id_estacion in [316, 2169]:
        dd.update(lee_canales(id_estacion)[1])
        
    meteo_data = pd.Series(data=[d[0] for d in dd.values()], index=dd.keys())
    meteo_data.name = pd.Timestamp.now()
    meteo_data = meteo_data.rename(NOMBRES_METEO)
    
    return meteo_data

data_meteo_live = lee_meteo_live() #SERIE DE DATOS - ESTACIÓN METEOROLÓGICA
data_datalogger_live = lee_ultimos_datos() #SERIE DE DATOS - MÓDULOS FOTOVOLTAICOS
data_live = pd.concat([data_datalogger_live, data_meteo_live], axis=0) #CONCATENACIÓN DE SERIES DE DATOS

df_live = pd.DataFrame(
                [data_live.data], #VALORES DE LOS DATOS DEL DATAFRAME
                index = ["At: " + pd.Timestamp.now().strftime('%d/%m/%y - %H:%M:%S')], #ÍNDICE DEL DATAFRAME
                columns = data_live.index #COLUMNAS DEL DATAFRAME
                )

#GENERACIÓN DE DATAFRAMES - SIN CONEXIÓN A RED DEL IES-UPM (MODALIDADES LIVE, RESUME Y DATA_TABLE)
df_datalogger = pd.concat(lee_fichero_sesion(name, path_sesiones="") for name in glob.glob("dataLogger/*.csv")) #DATAFRAME DATOS - MÓDULO FOTOVOLTAICO IES-UPM
df_datalogger.columns = 'DATALOGGER: ' + df_datalogger.columns
df_meteo = lee_meteo(df_datalogger.index.round('T'),path_estacion="dataLogger/") #DATAFRAME DATOS - ESTACIÓN METEOROLÓGICA IES-UPM
df_meteo.index = df_datalogger.index
df_meteo.columns = 'METEO: ' + df_meteo.columns
df = pd.concat([df_datalogger,df_meteo], axis=1) #CONCATENACIÓN DE DATAFRAMES

#LOGOTIPOS Y SELECCIÓN DE MODALIDAD DE LA APLICACIÓN WEB
#ESTRUCTURA
ies_logo_col, view_mode_col, variables_selection_col1, variables_selection_col2, upm_logo_col = st.beta_columns([2,2,4.9,4.9,1.2])

with ies_logo_col: #LOGOTIPO IES-UPM
    st.image("logo_IES.png", use_column_width=True)
with upm_logo_col: #LOGOTIPO UPM
    st.image("logo_upm.png", use_column_width=True) 
    
view_mode = view_mode_col.radio("SELECT VIEW MODE", ('Live', 'Resume', 'Data Table')) #SELECCIÓN DE MODALIDAD

if view_mode == 'Live': #MODALIDAD 'LIVE'
    #VARIABLE PARA SELECCIÓN DE TIPO DE MONITORIZACIÓN, EN TIEMPO REAL, DE LAS VARIABLES - TIEMPO REAL O SU SIMULACIÓN
    MODO_DESARROLLO = False #MODO DE SIMULACIÓN, POR DEFECTO
    
    df_live_mode = pd.DataFrame()
    
    if MODO_DESARROLLO is True:
        df_live_mode=df_live #DATAFRAME - TIEMPO REAL
    else:
        df_live_mode=df #DATAFRAME - SIMULACIÓN DE TIEMPO REAL
    
    #FILTRO DE SELECCIÓN DE VARIABLES
    variables_selection_col1.markdown("<p style='display: block; height:100px; line-height:100px; text-align: center; align: center; font-size: 25px; font-family: calibri; font-weight: bold'>SELECT DATASET TO PLOT</p>", unsafe_allow_html=True,) #TÍTULO DEL FILTRO
    variables_selection = variables_selection_col2.multiselect("", df_live_mode.columns.tolist()) #SELECCIÓN DE VARIABLES
    
    #VENTANA DESPLEGABLE INFORMATIVA DE VARIABLES SELECCIONADAS
    live_data_sidebar = st.sidebar #CREACIÓN DE VENTANA
    live_data_sidebar.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>LIVE DATASET", unsafe_allow_html=True,) #TITULO DE INFORMACIÓN EN LA VENTANA
    for col in variables_selection: #PUBLICACIÓN DE INFORMACIÓN EN VENTANA
        live_data_sidebar.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,)
    for j in range(3): #SOLUCIÓN PARA PROBLEMA DE BLOQUE DE COLUMNAS EN VENTANA (problema generado por ejecución consecutiva de modalidades RESUME y LIVE
        live_data_sidebar.empty()
    
    st.empty() #SOLUCIÓN PARA PROBLEMA DE EJECUCIÓN CONSECUTIVA ENTRE MODALIDADES (eliminación de bloques de columnas en modalidad LIVE)
    
    #ACTUALIZACIÓN DE TABLA Y GRÁFICA EN TIEMPO REAL
    live_table_data=st.empty() #ACTUALIZACIÓN DE TABLA
    live_chart_data=st.empty() #ACTUALIZACIÓN DE GRÁFICO
    
    if MODO_DESARROLLO is True: #MONITORIZACIÓN EN TIEMPO REAL 
        #DATAFRAME PARA PUBLICACIÓN EN TABLA
        live_table_dataframe = pd.DataFrame(
                [df_live_mode[variables_selection]], #VALORES DE LOS DATOS DEL DATAFRAME
                index = ["At: " + df_live_mode.index.strftime('%d/%m/%y - %H:%M:%S')], #ÍNDICE DEL DATAFRAME
                columns = variables_selection #COLUMNAS DEL DATAFRAME
                )
        
        #MONITORIZACIÓN DE VARIABLES SELECCIONADAS
        if(variables_selection is None or len(variables_selection)==0): 
            time.sleep(1) #TIEMPO NECESARIO PARA QUE LA APLICACIÓN ARRANQUE SIN ERROR DE 'EMPTY CHART'
            live_chart = st.line_chart({}) #GRÁFICO VACÍO SI NO SE HAN SELECCIONADO MAGNITUDES A REPRESENTAR
        else:
            live_table_data.table(live_table_dataframe.style.set_properties(**{'font-size': '15px','text-align': 'right'}).set_precision(2)) #PUBLICACIÓN EN TABLA
            live_chart = live_chart_data.line_chart(df_live_mode[variables_selection]) #REPRESENTACIÓN GRÁFICA

    else: #MONITORIZACIÓN DE SIMULACIÓN EN TIEMPO REAL
        i=0
        
        #CREACIÓN DE COLECCIONES EXTENSIBLES Y ACTUALIZABLES DE DATOS
        data_collection = deque() #COLECCIÓN A RELLENAR CON VALORES DE LAS VARIABLES O COLUMNAS DEL DATAFRAME
        time_collection = deque() #COLECCIÓN A RELLENAR CON INFORMACIÓN TEMPORAL O ÍNDICE DEL DATAFRAME
        
        while True: #BUCLE INFINITO PARA SIMULACIÓN
            
            j=0
            
            if(i<(len(df)-1)):
                i=i+1
                
            #ACTUALIZACIÓN DE DATOS EN COLECCIONES
            data_collection.append(df[variables_selection].values[i]) #RELLENO DE data_collection CON VALORES DE DATOS DE DATAFRAME INICIAL
            time_collection.append(df.index[i]+timedelta(hours=1)) #RELLENO DE time_collection CON INFORMACIÓN DE ÍNDICE DE DATAFRAME INICIAL
            
            #DATAFRAME PARA REPRESENTACIÓN GRÁFICA
            live_chart_dataframe = pd.DataFrame(
                 data_collection, #VALORES DE LOS DATOS DEL DATAFRAME
                 index = time_collection, #ÍNDICE DEL DATAFRAME
                 columns = variables_selection #COLUMNAS DEL DATAFRAME
                 )
            
            #DATAFRAME PARA PUBLICACIÓN EN TABLA
            live_table_dataframe = pd.DataFrame(
                [df[variables_selection].values[i]], #VALORES DE LOS DATOS DEL DATAFRAME
                index = ["At: " + df.index[i].strftime('%d/%m/%y - %H:%M:%S')], #ÍNDICE DEL DATAFRAME
                columns = variables_selection #COLUMNAS DEL DATAFRAME
                )
        
            #MONITORIZACIÓN DE DATAFRAMES DE VARIABLES SELECCIONADAS
            if(variables_selection is None or len(variables_selection)==0): 
                time.sleep(1) #TIEMPO NECESARIO PARA QUE LA APLICACIÓN ARRANQUE SIN ERROR DE 'EMPTY CHART'
                live_chart = live_chart_data.line_chart({}) #GRÁFICO VACÍO SI NO SE HAN SELECCIONADO MAGNITUDES A REPRESENTAR
            else:
                live_chart = live_chart_data.line_chart(live_chart_dataframe) #REPRESENTACIÓN GRÁFICA
                live_table_data.table(live_table_dataframe.style.set_properties(**{'font-size': '15px','text-align': 'right'}).set_precision(2)) #REPRESENTACIÓN EN TABLA
                
                for j in range(1):
                    time.sleep(1) #TIEMPO DE ACTUALIZACIÓN DE GRÁFICO Y TABLA (SIMULACIÓN DE TIEMPO REAL)
                
elif view_mode == 'Resume': #MODALIDAD 'RESUME'
    
    #FILTRO DE SELECCIÓN MANUAL DE CONJUNTOS DE VARIABLES
    first_variables_set_selected_resume = variables_selection_col1.multiselect("SELECT FIRST SET OF VARIABLES", df.columns.tolist()) #CREACIÓN DE FILTRO 1
    second_variables_set_selected_resume = variables_selection_col2.multiselect("SELECT SECOND SET OF VARIABLES", df.columns.tolist()) #CREACIÓN DE FILTRO 2

    #FILTRO DE SELECCIÓN DE SETS PREDEFINIDOS DE VARIABLES
    #ESTRUCTURA
    empty_col1, empty_col2, first_set_selection_col, second_set_selection_col, empty_col3 = st.beta_columns([2,2,4.9,4.9,1.5]) #ESTRUCTURACIÓN DEL FILTRO DE SELECCIÓN DE SETS DE DATOS

    #CREACIÓN DE FILTRO PARA GRÁFICO 1
    with first_set_selection_col:
        
        with st.beta_expander("Pick a dataset to plot:"):
            
            #FILTRO O PESTAÑA DESPLEGABLE PARA SELECCIÓN
            set_option_1 = st.selectbox('', ['SET ALREADY SELECTED','DATALOGGER: TEMP - MOCKUPS 1&2','DATALOGGER: RH - MOCKUPS 1&2','DATALOGGER: PRESSURE - MOCKUPS 1&2','DATALOGGER: TEMP & RH - ELECT. CABIN.','DATALOGGER: TEMP - FRONTSIDE MOCKUPS 1&2','DATALOGGER: TEMP - BACKSIDE MOCKUPS 1&2','GEONICA: ATMOSPH. TEMP','GEONICA: RH','GEONICA: CELULAS TOP, MID & BOT','GEONICA: IRRADIANCE','GEONICA: WIND SPEED & DIRECTION','GEONICA: SUN ELEV. & ORIENT.','GEONICA: IRRADIANCE & TEMP PIRGEO','GEONICA: ATMOSPH. PRESSURE','GEONICA: PRECIPITATION']) #OPCIONES DE SETS DE DATOS A REPRESENTAR EN GRÁFICO 1

            if set_option_1 == "SET ALREADY SELECTED": #DATASET CON SELECCIÓN MANUAL DE MAGNITUDES
                df_set_filter_1 = df[first_variables_set_selected_resume] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "DATALOGGER: TEMP - MOCKUPS 1&2": #TEMPERATURAS INTERIOR MOCKUPS-DATALOGGER
                df_set_filter_1 = df[[item for item in df.columns if 'M1-TEMP' in item]+
                                     [item for item in df.columns if 'M2-TEMP' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "DATALOGGER: RH - MOCKUPS 1&2": #HUMEDADES INTERIOR MOCKUPS-DATALOGGER
                df_set_filter_1 = df[[item for item in df.columns if 'M1-RH' in item]+
                                     [item for item in df.columns if 'M2-RH' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "DATALOGGER: PRESSURE - MOCKUPS 1&2": #PRESIONES INTERIOR MOCKUPS-DATALOGGER
                df_set_filter_1 = df[[item for item in df.columns if 'M1-SP' in item]+
                                     [item for item in df.columns if 'M2-SP' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "DATALOGGER: TEMP & RH - ELECT. CABIN.": #TEMPERATURA Y HUMEDAD - ARMARIO ELÉCTRICO-DATALOGGER
                df_set_filter_1 = df[[item for item in df.columns if 'C-TEMP' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "DATALOGGER: TEMP - FRONTSIDE MOCKUPS 1&2": #TEMPERATURAS DELANTERA MOCKUPS-DATALOGGER
                df_set_filter_1 = df[[item for item in df.columns if 'M1-Tp FS' in item]+
                                     [item for item in df.columns if 'M2-Tp FS' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "DATALOGGER: TEMP - BACKSIDE MOCKUPS 1&2": #TEMPERATURAS TRASERA MOCKUPS-DATALOGGER
                df_set_filter_1 = df[[item for item in df.columns if 'M1-Tp BS' in item]+
                                     [item for item in df.columns if 'M2-TP BS' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "GEONICA: ATMOSPH. TEMP": #TEMPERATURA ATMOSFÉRICA-GEÓNICA
                df_set_filter_1 = df[[item for item in df.columns if 'Temp. Ai' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "GEONICA: RH": #HUMEDAD RELATIVA-GEÓNICA
                df_set_filter_1 = df[[item for item in df.columns if 'Hum. Rel' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "GEONICA: CELULAS TOP, MID & BOT": #CÉLULAS TOP, MID Y BOT-GEÓNICA
                df_set_filter_1 = df[[item for item in df.columns if 'Celula' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "GEONICA: IRRADIANCE": #IRRADIANCIAS-GEÓNICA
                df_set_filter_1 = df[[item for item in df.columns if 'Bn' in item]+
                                     [item for item in df.columns if 'Gn' in item]+
                                     [item for item in df.columns if 'Gh' in item]+
                                     [item for item in df.columns if 'Dh' in item]+
                                     [item for item in df.columns if 'G(41)' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "GEONICA: WIND SPEED & DIRECTION": #VELOCIDAD Y DIRECCIÓN DEL VIENTO-GEÓNICA
                df_set_filter_1 = df[[item for item in df.columns if 'Vien' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "GEONICA: SUN ELEV. & ORIENT.": #ELEVACIÓN Y ORIENTACIÓN DEL SOL-GEÓNICA
                df_set_filter_1 = df[[item for item in df.columns if 'Sol' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "GEONICA: IRRADIANCE & TEMP PIRGEO": #IRRADIANCIA Y TEMPERATURA PIRGEO-GEÓNICA
                df_set_filter_1 = df[[item for item in df.columns if 'Pirgeo' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "GEONICA: ATMOSPH. PRESSURE": #PRESIÓN-GEÓNICA
                df_set_filter_1 = df[[item for item in df.columns if 'Presion' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_1 == "GEONICA: PRECIPITATION": #PRECIPITACIÓN-GEÓNICA
                df_set_filter_1 = df[[item for item in df.columns if 'Lluvia' in item]] #DATAFRAME INICIAL FILTRADO    
  
    #CREACIÓN DE FILTRO PARA GRÁFICO 2
    with second_set_selection_col:
            
        with st.beta_expander("Pick a dataset to plot:"):
            
            #FILTRO O PESTAÑA DESPLEGABLE PARA SELECCIÓN
            set_option_2 = st.selectbox('', ['SET ALREADY SELECTED ','DATALOGGER: TEMP - MOCKUPS 1&2','DATALOGGER: RH - MOCKUPS 1&2','DATALOGGER: PRESSURE - MOCKUPS 1&2','DATALOGGER: TEMP & RH - ELECT. CABIN.','DATALOGGER: TEMP - FRONTSIDE MOCKUPS 1&2','DATALOGGER: TEMP - BACKSIDE MOCKUPS 1&2','GEONICA: ATMOSPH. TEMP','GEONICA: RH','GEONICA: CELULAS TOP, MID & BOT','GEONICA: IRRADIANCE','GEONICA: WIND SPEED & DIRECTION','GEONICA: SUN ELEV. & ORIENT.','GEONICA: IRRADIANCE & TEMP PIRGEO','GEONICA: ATMOSPH. PRESSURE','GEONICA: PRECIPITATION']) #OPCIONES DE SETS DE DATOS A REPRESENTAR EN GRÁFICO 2
            
            if set_option_2 == "SET ALREADY SELECTED ": #DATASET CON SELECCIÓN MANUAL DE MAGNITUDES
                df_set_filter_2 = df[second_variables_set_selected_resume] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "DATALOGGER: TEMP - MOCKUPS 1&2": #TEMPERATURAS INTERIOR MOCKUPS-DATALOGGER
                df_set_filter_2 = df[[item for item in df.columns if 'M1-TEMP' in item]+
                                     [item for item in df.columns if 'M2-TEMP' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "DATALOGGER: RH - MOCKUPS 1&2": #HUMEDADES INTERIOR MOCKUPS-DATALOGGER
                df_set_filter_2 = df[[item for item in df.columns if 'M1-RH' in item]+
                                     [item for item in df.columns if 'M2-RH' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "DATALOGGER: PRESSURE - MOCKUPS 1&2": #PRESIONES INTERIOR MOCKUPS-DATALOGGER
                df_set_filter_2 = df[[item for item in df.columns if 'M1-SP' in item]+
                                     [item for item in df.columns if 'M2-SP' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "DATALOGGER: TEMP & RH - ELECT. CABIN.": #TEMPERATURA Y HUMEDAD - ARMARIO ELÉCTRICO-DATALOGGER
                df_set_filter_2 = df[[item for item in df.columns if 'C-TEMP' in item]+
                                     [item for item in df.columns if 'C-RH' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "DATALOGGER: TEMP - FRONTSIDE MOCKUPS 1&2": #TEMPERATURAS DELANTERA MOCKUPS-DATALOGGER
                df_set_filter_2 = df[[item for item in df.columns if 'M1-Tp FS' in item]+
                                     [item for item in df.columns if 'M2-Tp FS' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "DATALOGGER: TEMP - BACKSIDE MOCKUPS 1&2": #TEMPERATURAS TRASERA MOCKUPS-DATALOGGER
                df_set_filter_2 = df[[item for item in df.columns if 'M1-Tp BS' in item]+
                                     [item for item in df.columns if 'M2-TP BS' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "GEONICA: ATMOSPH. TEMP": #TEMPERATURA ATMOSFÉRICA-GEÓNICA
                df_set_filter_2 = df[[item for item in df.columns if 'Temp. Ai' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "GEONICA: RH": #HUMEDAD RELATIVA-GEÓNICA
                df_set_filter_2 = df[[item for item in df.columns if 'Hum. Rel' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "GEONICA: CELULAS TOP, MID & BOT": #CÉLULAS TOP, MID Y BOT-GEÓNICA
                df_set_filter_2 = df[[item for item in df.columns if 'Celula' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "GEONICA: IRRADIANCE": #IRRADIANCIAS-GEÓNICA
                df_set_filter_2 = df[[item for item in df.columns if 'Bn' in item]+
                                     [item for item in df.columns if 'Gn' in item]+
                                     [item for item in df.columns if 'Gh' in item]+
                                     [item for item in df.columns if 'Dh' in item]+
                                     [item for item in df.columns if 'G(41)' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "GEONICA: WIND SPEED & DIRECTION": #VELOCIDAD Y DIRECCIÓN DEL VIENTO-GEÓNICA
                df_set_filter_2 = df[[item for item in df.columns if 'Vien' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "GEONICA: SUN ELEV. & ORIENT.": #ELEVACIÓN Y ORIENTACIÓN DEL SOL-GEÓNICA
                df_set_filter_2 = df[[item for item in df.columns if 'Sol' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "GEONICA: IRRADIANCE & TEMP PIRGEO": #IRRADIANCIA Y TEMPERATURA PIRGEO-GEÓNICA
                df_set_filter_2 = df[[item for item in df.columns if 'Pirgeo' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "GEONICA: ATMOSPH. PRESSURE": #PRESIÓN-GEÓNICA
                df_set_filter_2 = df[[item for item in df.columns if 'Presion' in item]] #DATAFRAME INICIAL FILTRADO
            elif set_option_2 == "GEONICA: PRECIPITATION": #PRECIPITACIÓN-GEÓNICA
                df_set_filter_2 = df[[item for item in df.columns if 'Lluvia' in item]] #DATAFRAME INICIAL FILTRADO
    
    #VENTANA DESPLEGABLE INFORMATIVA DE SETS PREDEFINIDOS SELECCIONADOS
    resume_data_sidebar = st.sidebar #CREACIÓN DE VENTANA
    resume_data_sidebar.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>DATASET 1</p>", unsafe_allow_html=True,) #TÍTULO DE INFORMACIÓN 1, EN VENTANA
    resume_data_sidebar.markdown("<p style='display: block; text-align: center; font-size: 17px; font-family: calibri'>"+set_option_1, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA, DE ETIQUETA DE SET PREDEFINIDO SELECCIONADO 1
    resume_data_sidebar.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>DATASET 2</p>", unsafe_allow_html=True,) #TÍTULO DE INFORMACIÓN 2, EN VENTANA
    resume_data_sidebar.markdown("<p style='display: block; text-align: center; font-size: 17px; font-family: calibri'>"+set_option_2, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA, DE ETIQUETA DE SET PREDEFINIDO SELECCIONADO 2
    
    #FILTRO DE RANGO DE FECHAS                
    titulo_filtro_fechas, fecha_inicial, fecha_final = st.beta_columns([1,2,2]) #ESTRUCTURA
    titulo_filtro_fechas.markdown("<p style='display: block; height: 0px; line-height: 115px; font-size: 25px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</p>", unsafe_allow_html=True,) #TÍTULO DE FILTRO
    fecha_inicio_resume = fecha_inicial.date_input('Start date:', df.index.min(), df.index.min(), df.index.max()) #SELECCIÓN DE FECHA INICIAL
    fecha_fin_resume = fecha_final.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today()) #SELECCIÓN DE FECHA FINAL

    #REPRESENTACIÓN GRÁFICA, EN MODO HISTÓRICO, DE DATAFRAME DE SET PREDEFINIDO DE VARIABLES METEOROLÓGICAS SELECCIONADO
    #ESTRUCTURA
    empty_col1, empty_col2, resume_chart_col1, resume_chart_col2, empty_col3 = st.beta_columns([2,2,4.9,4.9,1.2])
    
    #GRÁFICO 1
    df_filter_chart1=df_set_filter_1.loc[fecha_inicio_resume:fecha_fin_resume] #DATAFRAME 1 FILTRADO POR RANGO DE FECHAS
    df_filter_chart1.index=df_filter_chart1.index+timedelta(hours=1) #reajuste temporal de índice de DataFrame 1 para su representación gráfica
    resume_chart1 = resume_chart_col1.line_chart(df_filter_chart1, use_container_width=True) #REPRESENTACIÓN GRÁFICA DE DATAFRAME 1

    #GRÁFICO 2
    df_filter_chart2=df_set_filter_2.loc[fecha_inicio_resume:fecha_fin_resume] #DATAFRAME 2 FILTRADO POR FECHAS
    df_filter_chart2.index=df_filter_chart2.index+timedelta(hours=1) #reajuste temporal de índice de DataFrame 2 para su representación gráfica
    resume_chart2 = resume_chart_col2.line_chart(df_filter_chart2, use_container_width=True) #REPRESENTACIÓN GRÁFICA DE DATAFRAME 2
     
elif view_mode == 'Data Table': #MODALIDAD 'DATA TABLE'
    
    #FILTRO DE SELECCIÓN DE VARIABLES METEOROlÓGICAS A REPRESENTAR EN TABLA
    variables_selection_col1.markdown("<p style='display: block; height:100px; line-height:100px; text-align: center; font-size: 25px; font-family: calibri; font-weight: bold'>SELECT DATASET TO PUBLISH ON TABLE</p>", unsafe_allow_html=True,) #TÍTULO DEL FILTRO
    variables_set_selected_data_table = variables_selection_col2.multiselect(" ", df.columns.tolist()) #CREACIÓN DEL FILTRO

    #FILTRO DE RANGO DE FECHAS
    titulo_filtro_fechas, fecha_inicial, fecha_final = st.beta_columns([1,2,2]) #ESTRUCTURA
    titulo_filtro_fechas.markdown("<p style='display: block; height:115px; line-height:115px; text-align: center; font-size: 25px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</p>", unsafe_allow_html=True,) #TíTULO DEL FILTRO
    fecha_inicio_table = fecha_inicial.date_input('Start date:', df.index.min(), df.index.min(), df.index.max()) #SELECCIÓN DE FECHA INICIAL
    fecha_fin_table = fecha_final.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today()) #SELECCIÓN DE FECHA FINAL

    #REPRESENTACIÓN, EN TABLA Y MODO HISTÓRICO, DE DATAFRAME DE VARIABLES METEOROLÓGICAS SELECCIONADAS
    df_filtered_table=df.loc[fecha_inicio_table:fecha_fin_table] #DATAFRAME FILTRADO POR RANGO DE FECHAS
    df_filtered_table.index=df_filtered_table.index.strftime("%d/%m/%y\n%H:%M:%S") #PERSONALIZACIÓN DE ÍNDICE DE DATAFRAME
    if len(variables_set_selected_data_table)>0:
        data_table = st.table(df_filtered_table[variables_set_selected_data_table].style.set_precision(2)) #REPRESENTACIÓN, EN TABLA, DE DATAFRAME