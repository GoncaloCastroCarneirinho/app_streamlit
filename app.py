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
from pygraphtec import lee_fichero_sesion, lee_ultima_sesion
from lectura_equipos import lee_meteo
import glob
import os

st.set_page_config(page_title='meteoIES-UPM', page_icon='ies-upm_page_config.jpg', layout="wide") #CONFIGURACIÓN DE PÁGINA WEB
st.markdown(f"""<style>.reportview-container {{ 
        background-size: 100% 100%;
        background-color: rgba(21,159,228,0.90);
        background-blend-mode: lighten;
        }}</style>""",
        unsafe_allow_html=True) #IMAGEN DE FONDO DE INTERFAZ

#df = lee_fichero_sesion("201112-165432.csv", path_sesiones='dataLogger')#Se ejecuta la función
print(lee_fichero_sesion(name, path_sesiones='dataLogger') for name in glob.glob("*.csv"))

#df_datalogger = pd.concat(lee_fichero_sesion(name, path_sesiones="dataLogger") for name in glob.glob("*.csv"))
#df_datalogger = pd.concat([lee_fichero_sesion("201112-180010.csv", path_sesiones='dataLogger'), lee_fichero_sesion("201112-165432.csv", path_sesiones='dataLogger')],axis=0)#DATAFRAME DE FICHERO DATALOGGER
df_datalogger = lee_fichero_sesion("201112-180010.csv", path_sesiones='dataLogger')#Se ejecuta la función
df_meteo = lee_meteo(pd.date_range(start='2020/11/12', end='2020/11/16', freq='10T'),path_estacion="dataLogger/") #DATAFRAME DE FICHERO METEO

df_meteo = lee_meteo(df_datalogger.index.round('T'),path_estacion="dataLogger/")
df_meteo.index = df_datalogger.index

df_datalogger.columns = df_datalogger.columns + '-DATALOGGER'
df_meteo.columns = df_meteo.columns + '-METEO'

df = pd.concat([df_datalogger,df_meteo], axis=1) #CONCATENACIÓN DE DATAFRAMES

col_logo1, view_mode_col, selection_col1, selection_col2, col_logo2 = st.beta_columns([2,2,4.9,4.9,1.2]) #ESTRUCTURA DE LA APP POR COLUMNAS PARA ELECCIÓN DE MODALIDAD DE VISTA Y VARIABLES A SELECCIONAR

with col_logo2: #IMAGEN DE LA UPM EN LA INTERFAZ
    st.image("upm-light_2.png", use_column_width=True)    
with col_logo1: #IMAGEN DEL IES-UPM EN LA INTERFAZ
    st.image("IES_2.png", use_column_width=True)
    
view_mode = view_mode_col.radio("SELECT VIEW MODE", ('Live', 'Resume', 'Data Table')) #MODALIDAD A SELECCIONAR

if view_mode == 'Live': #MODALIDAD 'LIVE'

    i=0

    #SELECCIÓN DE SET DE MAGNITUDES
    selection_col1.markdown("""<p style='display: block; height:100px; line-height:100px; text-align: center; align: center; font-size: 25px; font-family: calibri; font-weight: bold'>SELECT DATASET TO PLOT</p>""", unsafe_allow_html=True,) #TÍTULO PARA SELECCIÓN DE MAGNITUDES METEOROLÓGICAS
    magnitudes_seleccion = selection_col2.multiselect("", df.columns.tolist()) #SELECCIÓN DE MAGNITUDES A REPRESENTAR
    
    #VENTANA INFORMATIVA DESPLEGABLE
    sidebar_live = st.sidebar #CREACIÓN DE VENTANA DESPLEGABLE
    sidebar_live.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>LIVE DATASET", unsafe_allow_html=True,) #TITULO DE INFORMACIÓN EN LA VENTANA DESPLEGABLE
    for col in magnitudes_seleccion: #PUBLICACIÓN DE MAGNITUDES SELECCIONADAS
        sidebar_live.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #INFORMACIÓN EN LA VENTANA DESPLEGABLE

    #COLECCIONES EXTENSIBLE Y ACTUALIZABLE, EN TIEMPO REAL, DE VALORES A REPRESENTAR GRÁFICAMENTE
    data_collection = deque() #COLECCIÓN A RELLENAR CON VALORES DE LOS DATOS (COLUMNAS) DEL DATAFRAME
    time_collection = deque() #COLECCIÓN A RELLENAR CON INFORMACIÓN TEMPORAL (ÍNDICE) DEL DATAFRAME
    
    #ACTUALIZACIÓN DE PUBLICACIÓN EN TIEMPO REAL
    table_data=st.empty() #PUBLICACIÓN EN TABLA
    chart_data=st.empty() #REPRESENTACIÓN GRÁFICA
    
    while True: #BUCLE PARA ACTUALIZACIÓN CONTINUA DE PUBLICACIÓN DE DATOS DE MAGNITUDES SELECCIONADAS
        
        j=0
        
        if(i<(len(df)-1)):
            i=i+1
            
        #ACTUALIZACIÓN DE DATOS EN COLECCIONES
        data_collection.append(df[magnitudes_seleccion].values[i]) #RELLENO DE data_collection CON VALORES DE DATOS DE DATAFRAME INICIAL
        time_collection.append(df.index[i]) #RELLENO DE time_collection CON INFORMACIÓN DE ÍNDICE DE DATAFRAME INICIAL
        
        #DATAFRAME PARA REPRESENTACIÓN GRÁFICA EN TIEMPO REAL
        chart_dataframe = pd.DataFrame(
             data_collection, #VALORES DE LOS DATOS DEL DATAFRAME
             index = time_collection, #FILAS O ÍNDICE DEL DATAFRAME
             columns = magnitudes_seleccion #COLUMNAS DEL DATAFRAME
             )
        
        #DATAFRAME PARA PUBLICACIÓN EN TABLA EN TIEMPO REAL
        table_dataframe = pd.DataFrame(
            [df[magnitudes_seleccion].values[i]], #VALORES DE LOS DATOS DEL DATAFRAME
            index = ["At: " + df.index[i].strftime('%d/%m/%y - %H:%M:%S')], #FILAS O ÍNDICE DEL DATAFRAME
            columns = magnitudes_seleccion #COLUMNAS DEL DATAFRAME
            )
        
        #REPRESENTACIÓN, EN TIEMPO REAL, DE MAGNITUDES SELECCIONADAS
        if(magnitudes_seleccion is None or len(magnitudes_seleccion)==0): 
            time.sleep(1) #TIEMPO NECESARIO PARA QUE LA APLICACIÓN ARRANQUE SIN ERROR DE 'EMPTY CHART'
            chart = chart_data.line_chart({}) #GRÁFICO VACÍO SI NO SE HAN SELECCIONADO MAGNITUDES A REPRESENTAR
        else:
            chart = chart_data.line_chart(chart_dataframe) #REPRESENTACIÓN GRÁFICA DE MAGNITUDES
            table_data.table(table_dataframe.style.set_properties(**{'font-size': '15px','text-align': 'right'}).set_precision(2)) #PUBLICACIÓN, EN TABLA, DE MAGNITUDES Y PRECISIÓN DE 2 DECIMALES EN SUS VALORES
            
            for j in range(1):
                time.sleep(1) #TIEMPO DE ACTUALIZACIÓN DE GRÁFICO Y TABLA (SIMULACIÓN DE TIEMPO REAL)
     
elif view_mode == 'Resume': #MODALIDAD 'RESUME'
    
    first_variables_set_selected_resume = selection_col1.multiselect("SELECT FIRST SET OF VARIABLES", df.columns.tolist()) #SELECCION DE VARIABLES A REPRESENTAR EN GRÁFICA 1
    second_variables_set_selected_resume = selection_col2.multiselect("SELECT SECOND SET OF VARIABLES", df.columns.tolist()) #SELECCION DE VARIABLES A REPRESENTAR EN GRÁFICA 2

    #FILTRO DE SETS ALTERNATIVOS DE DATOS A REPRESENTAR GRAFICAMENTE
    #ESTRUCTURA
    empty_column_1, empty_column_2, first_set_selection_col, second_set_selection_col, empty_column_3 = st.beta_columns([2,2,4.9,4.9,1.5]) #ESTRUCTURACIÓN DEL FILTRO DE SELECCIÓN DE SETS DE DATOS

    #SELECCIÓN DE DATASETS PARA GRÁFICO 1
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
  
    #SELECCIÓN DE DATASETS PARA GRÁFICO 2
    with second_set_selection_col:
            
        with st.beta_expander("Pick a dataset to plot:"):
            
            #FILTRO O PESTAÑA DESPLEGABLE PARA SELECCIÓN
            set_option_2 = st.selectbox('', ['SET ALREADY SELECTED','DATALOGGER: TEMP - MOCKUPS 1&2','DATALOGGER: RH - MOCKUPS 1&2','DATALOGGER: PRESSURE - MOCKUPS 1&2','DATALOGGER: TEMP & RH - ELECT. CABIN.','DATALOGGER: TEMP - FRONTSIDE MOCKUPS 1&2','DATALOGGER: TEMP - BACKSIDE MOCKUPS 1&2','GEONICA: ATMOSPH. TEMP','GEONICA: RH','GEONICA: CELULAS TOP, MID & BOT','GEONICA: IRRADIANCE','GEONICA: WIND SPEED & DIRECTION','GEONICA: SUN ELEV. & ORIENT.','GEONICA: IRRADIANCE & TEMP PIRGEO','GEONICA: ATMOSPH. PRESSURE','GEONICA: PRECIPITATION']) #OPCIONES DE SETS DE DATOS A REPRESENTAR EN GRÁFICO 2
            
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
    
    #VENTANA INFORMATIVA DESPLEGABLE A LA IZQUIERDA
    sidebar_resume = st.sidebar #CREACIÓN DE VENTANA DESPLEGABLE
    # sidebar_col1, sidebar_col2 = sidebar_resume.beta_columns([1,1]) #ESTRUCTURA POR COLUMNAS
    # sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>DATASET 1", unsafe_allow_html=True,) #TÍTULO 1 DE INFORMACIÓN A PUBLICAR EN VENTANA DESPLEGABLE
    # sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>DATASET 2", unsafe_allow_html=True,) #TÍTULO 2 DE INFORMACIÓN A PUBLICAR EN VENTANA DESPLEGABLE
    # for col in df_set_filter_1.columns: #PUBLICACIÓN DE MAGNITUDES SELECCIONADAS EN COLUMNA 1
    #     sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA DESPLEGABLE, DE SET PREDETERMINADO DE MAGNITUDES SELECCIONADAS
    # for col in df_set_filter_2.columns: #PUBLICACIÓN DE MAGNITUDES SELECCIONADAS EN COLUMNA 2
    #     sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA DESPLEGABLE, DE SET PREDETERMINADO DE MAGNITUDES SELECCIONADAS
    sidebar_resume.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>DATASET 1", unsafe_allow_html=True,)    
    sidebar_resume.markdown("<p style='display: block; text-align: center; font-size: 17px; font-family: calibri'>"+set_option_1, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA DESPLEGABLE, DE SET PREDETERMINADO DE MAGNITUDES SELECCIONADAS
    sidebar_resume.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>DATASET 2", unsafe_allow_html=True,)    
    sidebar_resume.markdown("<p style='display: block; text-align: center; font-size: 17px; font-family: calibri'>"+set_option_2, unsafe_allow_html=True,) #PUBLICACIÓN, EN VENTANA DESPLEGABLE, DE SET PREDETERMINADO DE MAGNITUDES SELECCIONADAS
    
    #FILTRO DE RANGO DE FECHAS                
    titulo_filtro_fechas, fecha_inicial, fecha_final = st.beta_columns([1,2,2]) #ESTRUCTURA DE FILTRO POR FECHAS
    titulo_filtro_fechas.markdown("<p style='display: block; height: 0px; line-height:115px; text-align: justify; font-size: 25px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</p>", unsafe_allow_html=True,) #TITULO DE FILTRO POR FECHAS
    fecha_inicio_resume = fecha_inicial.date_input('Start date:', df.index.min(), df.index.min(), df.index.max()) #SELECCIÓN DE FECHA INICIAL
    fecha_fin_resume = fecha_final.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today()) #SELECCIÓN DE FECHA FINAL

    #REPRESENTACIÓN GRÁFICA DEL DATAFRAME CON LOS SETS DE DATOS ELEGIDOS
    #ESTRUCTURA
    col1, col_vacia, grafico1_resume, grafico2_resume, col2 = st.beta_columns([2,2,4.9,4.9,1.2])
    
    #GRÁFICO 1
    df_filter_chart1=df_set_filter_1.loc[fecha_inicio_resume:fecha_fin_resume] #DATAFRAME FILTRADO POR FECHAS
    #chart1_title = grafico1_resume.markdown("<p style='display: block; text-align: center; font-size: 14px; font-family: calibri; font-weight: bold'>"+set_option_1, unsafe_allow_html=True,) #TÍTULO DE GRÁFICO 1
    #chart1 = grafico1_resume.empty() #CREACIÓN DE GRÁFICO, INICIALMENTE VACÍO
    Data_chart1 = grafico1_resume.line_chart(df_filter_chart1, use_container_width=True) #REPRESENTACIÓN GRÁFICA DE DATAFRAME

    #GRÁFICO 2
    df_filter_chart2=df_set_filter_2.loc[fecha_inicio_resume:fecha_fin_resume] #DATAFRAME 2 FILTRADO POR FECHAS
    #chart2_title = grafico2_resume.markdown("<p style='display: block; text-align: center; font-size: 14px; font-family: calibri; font-weight: bold'>"+set_option_2, unsafe_allow_html=True,)
    #chart2 = grafico2_resume.empty() #CREACIÓN DE GRÁFICO, INICIALMENTE VACÍO
    Data_chart2 = grafico2_resume.line_chart(df_filter_chart2, use_container_width=True) #REPRESENTACIÓN GRÁFICA DE DATAFRAME
     
elif view_mode == 'Data Table': #MODALIDAD 'DATA TABLE'
    
    #FILTRO DE SELECCIÓN DE VARIABLES
    col1.markdown("""<a style='display: block; height:100px; line-height:100px; text-align: center; font-size: 25px; font-family: calibri; font-weight: bold'>SELECT DATASET TO PUBLISH ON TABLE</a>""", unsafe_allow_html=True,) #TÍTULO DEL FILTRO DE SELECCIÓN DE VARIABLES A REPRESENTAR
    variables_set_selected_live = selection_col2.multiselect(" ", df.columns.tolist()) #SELECCIÓN DEL SET DE VARIABLES A REPRESENTAR EN MODO TABLA

    #FILTRO DE RANGO DE FECHAS
    titulo_filtro_fechas, fecha_inicial, fecha_final = st.beta_columns([1,2,2]) #ESTRUCTURA DEL FILTRO DE RANGO DE FECHAS
    titulo_filtro_fechas.markdown("""<a style='display: block; height:115px; line-height:115px; text-align: center; font-size: 25px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</a>""", unsafe_allow_html=True,) #TíTULO DE FILTRO DE RANGO DE FECHAS
    fecha_inicio_table = fecha_inicial.date_input('Start date:', df.index.min(), df.index.min(), df.index.max()) #SELECCIÓN DE FECHA INICIAL
    fecha_fin_table = fecha_final.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today()) #SELECCIÓN DE FECHA FINAL

    #REPRESENTACIÓN EN MODO TABLA DEL DATAFRAME CON EL SET DE DATOS ELEGIDO
    df_filtered_table=df.loc[fecha_inicio_table:fecha_fin_table] #DATAFRAME FILTRADO POR FECHAS
    df_filtered_table.index=df_filtered_table.index.strftime("%d/%m/%y\n%H:%M:%S")
    
    if len(variables_set_selected_live)>0:
        data_table = st.table(df_filtered_table[variables_set_selected_live].style.set_precision(2)) #CREACIÓN DE TABLA CON VALORES DE MAGNITUDES SELECCIONADAS Y CON PRECISIÓN DE 2 DECIMALES