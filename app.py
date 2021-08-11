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
df_datalogger = lee_fichero_sesion("201112-180010.csv", path_sesiones='dataLogger') #Dataframe de Datalogger
#df = pd.concat([df1,df0])
# df.columns += '_meteo1'
df_meteo =  lee_meteo(pd.date_range(start='2020/11/12', end='2020/11/16', freq='1T'),path_estacion="dataLogger/") #Dataframe de Meteo
df = pd.concat([df_datalogger,df_meteo], axis=1, join='outer') #Unión de Dataframes
#df = df0.append(df1, sort=False)
#df = df0.merge(df1, right_index=True, left_index=True, how='outer')
#df = df0.join(df1,how='outer')
#df_meteo2 += '_meteo2'

#df = df0.append(df1,ignore_index=True)
#df = pd.concat([df1,df0], axis=1)

view_mode_col, col2, select_variables_col = st.beta_columns([2,6,6]) #Estructura superior de las vistas de la app en columnas

i=0

view_mode = view_mode_col.radio("SELECT VIEW MODE", ('Live', 'Resume', 'Data Table')) #Opciones de vista de app

main_bg = "logo_IES.jpg"
main_bg_ext = "jpg"

st.markdown( #imagen de fondo de app
    f"""
    <style>
    .reportview-container {{
        background-image: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
        background-size: 100% 100%;
        background-color: rgba(255,255,255,0.90);
        background-blend-mode: lighten;
    }}
    .stButton>button{{
    color: #11A27B;
    box-sizing: 5%;
    height: 5em;
    width: 5em;
    font-size:50px;
    border: 7px solid;
    border-radius: 10px;
    padding: 30px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

if view_mode == 'Live': #modalidad LIVE
       
    variables_seleccion = select_variables_col.multiselect("", df.columns.tolist()) #seleccion de variables a representar
    
    sidebar_live = st.sidebar #ventana despegable a la izquierda
    
    sidebar_live.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>VARIABLES SET", unsafe_allow_html=True,) #titulo de la informacion de la ventana despegable
    
    for col in variables_seleccion:
        sidebar_live.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #informacion en la ventana despegable

    col2.markdown("""<p style='display: block; height:100px; line-height:100px; text-align: center; align: center; font-size: 25px; font-family: calibri; font-weight: bold'>SELECT SET OF VARIABLES TO PLOT LIVE</p>""", unsafe_allow_html=True,) #'SELECCIONAR VARIABLES A REPRESENTAR EN MODO LIVE'

    # with column_2:
    #     st.image("logo_upm.png",width=300) #logo UPM

    data_collection = deque() #coleccion creada para su relleno con valores de los datos del dataframe
    time_collection = deque() #coleccion creada para su relleno con informacion de fecha y hora del dataframe
    
    i=0

    status_text=st.empty() #creacion de variable con valor actualizable permanentemente
    
    while True: #bucle para actualizacion continua del gráfico
        
        j=0
        
        if(i<(len(df)-1)):
            i=i+1
            
        data_collection.append(df[variables_seleccion].values[i]) #relleno de las colecciones con valores de datos del dataframe
        time_collection.append(df.index[i]) #relleno de las colecciones con informacion de fecha y hora del dataframe
        
        chart_dataframe = pd.DataFrame( #creacion de nuevo dataframe para la representacion gráfica en tiempo real
             data_collection, #valores del dataframe
             index = time_collection, #filas del dataframe
             columns = variables_seleccion #columnas del dataframe
             )
        
        table_dataframe = pd.DataFrame( #creacion de nuevo dataframe para la representacion en tabla en tiempo real
            [df[variables_seleccion].values[i]], #valores del dataframe
            index = ["At: " + df.index[i].strftime('%d/%m/%y - %H:%M:%S')], #filas del dataframe
            columns = variables_seleccion #columnas del dataframe
            )
        
        if(variables_seleccion is None or len(variables_seleccion)==0): 
            time.sleep(1) #tiempo necesario para que la aplicación arranque sin dar error de 'empty chart'
            chart = st.line_chart({}) #gráfico vacío si no se ha seleccionado información a representar
        else:
            chart = st.line_chart(chart_dataframe) #variables dataframe 'chart_dataframe' seleccionadas y representadas en gráfico
            status_text.table(table_dataframe.style.set_properties(**{'font-size': '15px','text-align': 'right'}).set_precision(2)) #variables dataframe 'table_dataframe' seleccionadas y representadas en tabla
            
            for j in range(1):
                time.sleep(1) #tiempo de actualizacion del gráfico (simulacion de tiempo real)
                st.empty() #por revisar
                
            chart.empty() #vacío de gráfico despues al actualizar
            chart.empty() #vacío de gráfico despues al actualizar        

elif view_mode == 'Resume':
    
    column1_resume, variables_set_selection_col, column3_resume = st.beta_columns([2,6,6]) #estructuración de otra fila de columnas en la vista RESUME
    
    sidebar_col1, sidebar_col2 = st.sidebar.beta_columns([1,1]) #estructuración en columnas de ventana despegable a la izquierda
    
    sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>VARIABLES SET 1", unsafe_allow_html=True,) #titulo 1 de informacion a publicar en ventana despegable

    sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>VARIABLES SET 2", unsafe_allow_html=True,) #titulo 2 de informacion a publicar en ventana despegable

    first_variables_set_selected_resume = col2.multiselect("SELECT FIRST SET OF VARIABLES", df.columns.tolist()) #seleccion de primero set de variables a representar graficamente

    with variables_set_selection_col: #funcionalidades en la columna 'column2_resume'
        
        with variables_set_selection_col.beta_expander("Pick a plot option:"): #creacion de filtro desplegable para elegir diferentes sets de variables a representar graficamente
            
            options_list_0 = st.selectbox('', ['FIRST SET ALREADY SELECTED','FIRST TEMPERATURE SET','FIRST HUMIDITY SET']) #opciones de sets alternativos de variables a representar
            
            variables_set_0 = list #creacion de lista vacia para relleno con variables
            
            if  options_list_0 == "FIRST SET ALREADY SELECTED":
                variables_set_0=first_variables_set_selected_resume
            elif options_list_0 == "FIRST TEMPERATURE SET":
                variables_set_0=options_list_0
            elif options_list_0 == "FIRST HUMIDITY SET":
                variables_set_0=options_list_0
                
            if variables_set_0 == first_variables_set_selected_resume:
            
                df_filt0 = df[[item for item in first_variables_set_selected_resume if 'TEMP' in item]] #creacion de dataframe personalizado para representaciones grafica y modo tabla de variables seleccionadas en el filtro principal
                for col in df_filt0:
                    sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #publicacion en la ventana desplegable de variables representadas
                df_filt0 = df[[item for item in first_variables_set_selected_resume if 'RH' in item]] #creacion de dataframe personalizado para representaciones grafica y modo tabla
                for col in df_filt0:
                    sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #publicacion en la ventana desplegable de variables representadas
                        
            elif variables_set_0 == options_list_0:
            
                if variables_set_0 == "FIRST TEMPERATURE SET":
                    df_filt0 = df[[item for item in df.columns if 'TEMP' in item]] #creacion de dataframe personalizado para representaciones grafica y modo tabla de set alternativo 'TEMPERATURAS' de variables
                    for col in df_filt0.columns:
                        sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #publicacion en la ventana desplegable de variables representadas
                elif variables_set_0 == "FIRST HUMIDITY SET":
                    df_filt0 = df[[item for item in df.columns if 'RH' in item]] #creacion de dataframe personalizado para representaciones grafica y modo tabla de set alternativo 'HUMEDADES' de variables
                    for col in df_filt0.columns:
                        sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #publicacion en la ventana desplegable de variables representadas
    
    second_variables_set_selected = select_variables_col.multiselect("SELECT SECOND SET OF VARIABLES", df.columns.tolist()) #seleccion de primero set de variables a representar graficamente
    
    with column3_resume:
            
        with st.beta_expander("Pick a plot option:"): #creacion de filtro desplegable para elegir diferentes sets de variables a representar graficamente
            
            options_list = st.selectbox('', ['SECOND SET ALREADY SELECTED','SECOND TEMPERATURE SET','SECOND HUMIDITY SET']) #opciones de sets alternativos de variables a representar
            
            variables_set_1 = list #creacion de lista vacia para relleno con variables
            
            if  options_list == "SECOND SET ALREADY SELECTED":
                variables_set_1=second_variables_set_selected
            elif options_list == "SECOND TEMPERATURE SET":
                variables_set_1=options_list
            elif options_list == "SECOND HUMIDITY SET":
                variables_set_1=options_list
                
            if variables_set_1 == second_variables_set_selected:
            
                df_filt1 = df[[item for item in second_variables_set_selected if 'TEMP' in item]] #creacion de dataframe personalizado para representaciones grafica y modo tabla de set alternativo 'TEMPERATURAS' de variables
                for col in df_filt1:
                    sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #publicacion en la ventana desplegable de variables representadas
                df_filt1 = df[[item for item in second_variables_set_selected if 'RH' in item]] #creacion de dataframe personalizado para representaciones grafica y modo tabla de set alternativo 'HUMEDADES' de variables
                for col in df_filt1:
                    sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #publicacion en la ventana desplegable de variables representadas
                        
            elif variables_set_1 == options_list:
            
                if variables_set_1 == "SECOND TEMPERATURE SET":
                    df_filt1 = df[[item for item in df.columns if 'TEMP' in item]] #creacion de dataframe personalizado para representaciones grafica y modo tabla de set alternativo 'TEMPERATURAS' de variables
                    for col in df_filt1.columns:
                        sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #publicacion en la ventana desplegable de variables representadas
                elif variables_set_1 == "SECOND HUMIDITY SET":
                    df_filt1 = df[[item for item in df.columns if 'RH' in item]] #creacion de dataframe personalizado para representaciones grafica y modo tabla de set alternativo 'HUMEDADES' de variables
                    for col in df_filt1.columns:                  
                        sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,) #publicacion en la ventana desplegable de variables representadas
                    
    titulo_filtro_fechas, fecha_inicial, fecha_final = st.beta_columns([1,2,2]) #columnas para filtros de fechas
    
    titulo_filtro_fechas.markdown("<p style='display: block; height: 0px; line-height:115px; text-align: justify; font-size: 25px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</p>", unsafe_allow_html=True,) #titulo de opciones de fechas a filtrar en representacion gráfica
    
    columna_vacia, grafico1_resume, grafico2_resume = st.beta_columns((2,6,6)) #estructura en columnas para representacion grafica de datos
    
    fecha_inicio_resume = fecha_inicial.date_input('Start date:', df.index.min(), df.index.min(), df.index.max()) #seleccionar fecha inicial
    
    fecha_fin_resume = fecha_final.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today()) #seleccionar fecha final

    def df_filter_date(message, df):#Función para filtrar el Dataframe por fechas
    
        filtered_df_date = df.loc[fecha_inicio_resume:fecha_fin_resume]#Se filtra el Dataframe df, pasado como argumento entre los valores date_1 y date_2

        return filtered_df_date#Se devuelve el Dataframe filtrado
    
    filtered_df_date = df_filter_date('Select dates range to filter dataframe',df) #elige dataframe inicial a filtrar sobre el rango de fechas seleccionado
    
    df_filter_chart2=df_filt1.loc[fecha_inicio_resume:fecha_fin_resume] #filtra, por fechas, el dataframe seleccionado a representar en el primer grafico
    
    df_filter_chart1=df_filt0.loc[fecha_inicio_resume:fecha_fin_resume] #filtra, por fechas, el dataframe seleccionado a representar en el primer grafico
    
    chart1_title = grafico1_resume.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>SET 1 RESUME</p>", unsafe_allow_html=True,) #titulo de primer grafico
    
    Data_chart1 = grafico1_resume.empty() #creacion de primer grafico, inicialmente vacio
    
    if variables_set_0==first_variables_set_selected_resume:
        
        Data_chart01 = Data_chart1.line_chart(filtered_df_date[first_variables_set_selected_resume]) #representacion grafica (grafico 1) de dataframe 1 filtrado por fechas
        
    elif variables_set_0==options_list_0:
        
        Data_chart02 = Data_chart1.line_chart(df_filter_chart1) #representacion grafica (grafico 1) de dataframe 2 filtrado por fechas
 
    Data_chart1_title = grafico2_resume.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>SET 2 RESUME</p>", unsafe_allow_html=True,)
    
    Data_chart2 = grafico2_resume.empty()
    
    if variables_set_1==second_variables_set_selected:
        
        Data_chart11 = Data_chart2.line_chart(filtered_df_date[second_variables_set_selected]) #representacion grafica (grafico 2) de dataframe 1 filtrado por fechas
        
    elif variables_set_1==options_list:
        
        Data_chart12 = Data_chart2.line_chart(df_filter_chart2) #representacion grafica (grafico 2) de dataframe 2 filtrado por fechas
            
elif view_mode == 'Data Table':
    
    variables_set_selected_live = select_variables_col.multiselect(" ", df.columns.tolist()) #seleccion de primero set de variables a representar en modo tabla
    
    col2.markdown("""<a style='display: block; height:100px; line-height:100px; text-align: center; font-size: 25px; font-family: calibri; font-weight: bold'>SELECT SET OF VARIABLES TO SHOW ON TABLE</a>""", unsafe_allow_html=True,) #"ELEGIR VARIABLES A REPRESENTAR EN TABLA"

    titulo_filtro_fechas, fecha_inicial, fecha_final = st.beta_columns([1,2,2]) #columnas para filtros de fechas
    
    titulo_filtro_fechas.markdown("""<a style='display: block; height:115px; line-height:115px; text-align: center; font-size: 25px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</a>""", unsafe_allow_html=True,) #titulo de opciones de fechas a filtrar en representacion gráfica
    
    fecha_inicio_table = fecha_inicial.date_input('Start date:', df.index.min(), df.index.min(), df.index.max()) #seleccionar fecha inicial
    
    fecha_fin_table = fecha_final.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today()) #seleccionar fecha final

    def df_filter_date(message, df):#Función para filtrar el Dataframe por fechas
    
        filtered_df_date = df.loc[fecha_inicio_table:fecha_fin_table]#Se filtra el Dataframe df, pasado como argumento entre los valores date_1 y date_2

        return filtered_df_date#Se devuelve el Dataframe filtrado
    
    filtered_df_date = df_filter_date('Select dates range to filter dataframe',df) #elige dataframe inicial a filtrar sobre el rango de fechas seleccionado
    
    filtered_df_date.index=filtered_df_date.index.strftime("%d/%m/%y\n%H:%M:%S") #personalizar fecha y hora en filas de la tabla
    
    df_filtered_table=df.loc[fecha_inicio_table:fecha_fin_table] #filtra, por fechas, el dataframe seleccionado a representar en la tabla
    
    if len(variables_set_selected_live)>0:
        data_table = st.table(filtered_df_date[variables_set_selected_live].style.set_precision(2)) #creacion de tabla con valores de variables seleccionadas y con precision de 2 decimales