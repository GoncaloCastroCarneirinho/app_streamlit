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
df0 = lee_fichero_sesion("201112-180010.csv", path_sesiones='dataLogger')
#df = pd.concat([df1,df0])
# df.columns += '_meteo1'
df1 =  lee_meteo(pd.date_range(start='2020/11/12', end='2020/11/16', freq='10T'),path_estacion="dataLogger/")
#df = pd.concat([df0,df1], axis=1, join='outer')
#df = df0.append(df1, sort=False)
df = df0.merge(df1, right_index=True, left_index=True, how='outer')
#df = df0.join(df1,how='outer')
#df_meteo2 += '_meteo2'

#df = df0.append(df1,ignore_index=True)
#df = pd.concat([df1,df0], axis=1)

column_1, column_2, column_0 = st.beta_columns([2,6,6])

i=0

view_mode = column_1.radio("SELECT VIEW MODE", ('Live', 'Resume', 'Data Table'))

main_bg = "logo_IES.jpg"
main_bg_ext = "jpg"

st.markdown(
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

if view_mode == 'Live':
       
    temp_humi_live = column_0.multiselect("", df.columns.tolist())
    
    sidebar_live = st.sidebar
    
    sidebar_live.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>VARIABLES SET", unsafe_allow_html=True,)
    
    for col in temp_humi_live:
        sidebar_live.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,)

    column_2.markdown("""<p style='display: block; height:100px; line-height:100px; text-align: center; align: center; font-size: 25px; font-family: calibri; font-weight: bold'>SELECT SET OF VARIABLES TO PLOT LIVE</p>""", unsafe_allow_html=True,)

    # with column_2:
    #     st.image("logo_upm.png",width=300) #añadirlo a la memoria 

    data_tail = deque()
    time_tail = deque()
    
    i=0

    status_text=st.empty()
    
    while True:
        
        j=0
        
        if(i<(len(df)-1)):
            i=i+1
            
        data_tail.append(df[temp_humi_live].values[i]) ##
        time_tail.append(df.index[i])
        
        chart_data = pd.DataFrame(
             data_tail,
             index = time_tail,
             columns = temp_humi_live
             )
        
        df1 = pd.DataFrame(
            [df[temp_humi_live].values[i]],
            index = ["At: " + df.index[i].strftime('%d/%m/%y - %H:%M:%S')],
            columns = temp_humi_live
            )
        
        if(temp_humi_live is None or len(temp_humi_live)==0):
            time.sleep(1) #necesario para que la aplicación arranque sin dar error de 'empty chart'
            chart = st.line_chart({})
        else:
            chart = st.line_chart(chart_data)
            status_text.table(df1.style.set_properties(**{'font-size': '15px','text-align': 'right'}).set_precision(2))
            
            for j in range(1):
                time.sleep(1)
                st.empty()
                
            chart.empty()
            chart.empty()            

elif view_mode == 'Resume':
    
    column1, column2, column0 = st.beta_columns([2,6,6])
    
    sidebar_col1, sidebar_col2 = st.sidebar.beta_columns([1,1])
    
    sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>VARIABLES SET 1", unsafe_allow_html=True,)

    sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>VARIABLES SET 2", unsafe_allow_html=True,)

    with column2:
    
        temp_humi_00 = column_2.multiselect("SELECT FIRST SET OF VARIABLES", df.columns.tolist())
        
        with column2.beta_expander("Pick a plot option:"):
            
            options_list_0 = st.selectbox('', ['FIRST SET ALREADY SELECTED','FIRST TEMPERATURE SET','FIRST HUMIDITY SET'])
            
            variables_set_0 = list
            
            if  options_list_0 == "FIRST SET ALREADY SELECTED":
                variables_set_0=temp_humi_00
            elif options_list_0 == "FIRST TEMPERATURE SET":
                variables_set_0=options_list_0
            elif options_list_0 == "FIRST HUMIDITY SET":
                variables_set_0=options_list_0
                
            if variables_set_0 == temp_humi_00:
            
                df_filt0 = df[[item for item in temp_humi_00 if 'TEMP' in item]]
                for col in df_filt0:
                    sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,)
                df_filt0 = df[[item for item in temp_humi_00 if 'RH' in item]]
                for col in df_filt0:
                    sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,)
                        
            elif variables_set_0 == options_list_0:
            
                if variables_set_0 == "FIRST TEMPERATURE SET":
                    df_filt0 = df[[item for item in df.columns if 'TEMP' in item]]
                    for col in df_filt0.columns:
                        sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,)
                elif variables_set_0 == "FIRST HUMIDITY SET":
                    df_filt0 = df[[item for item in df.columns if 'RH' in item]]
                    for col in df_filt0.columns:
                        sidebar_col1.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,)
    
    with column0:
    
        temp_humi_01 = column_0.multiselect("SELECT SECOND SET OF VARIABLES", df.columns.tolist())
        
        with st.beta_expander("Pick a plot option:"):
            
            options_list = st.selectbox('', ['SECOND SET ALREADY SELECTED','SECOND TEMPERATURE SET','SECOND HUMIDITY SET'])
            
            variables_set_1 = list
            
            if  options_list == "SECOND SET ALREADY SELECTED":
                variables_set_1=temp_humi_01
            elif options_list == "SECOND TEMPERATURE SET":
                variables_set_1=options_list
            elif options_list == "SECOND HUMIDITY SET":
                variables_set_1=options_list
                
            if variables_set_1 == temp_humi_01:
            
                df_filt1 = df[[item for item in temp_humi_01 if 'TEMP' in item]] #
                for col in df_filt1:
                    sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,)
                df_filt1 = df[[item for item in temp_humi_01 if 'RH' in item]] #
                for col in df_filt1:
                    sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,)
                        
            elif variables_set_1 == options_list:
            
                if variables_set_1 == "SECOND TEMPERATURE SET":
                    df_filt1 = df[[item for item in df.columns if 'TEMP' in item]] #
                    for col in df_filt1.columns:
                        sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,)
                elif variables_set_1 == "SECOND HUMIDITY SET":
                    df_filt1 = df[[item for item in df.columns if 'RH' in item]] #
                    for col in df_filt1.columns:                  
                        sidebar_col2.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri'>"+col, unsafe_allow_html=True,)
                    
    column_34, column_3, column_4 = st.beta_columns([1,2,2])
    
    column_34.markdown("<p style='display: block; height: 0px; line-height:115px; text-align: justify; font-size: 25px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</p>", unsafe_allow_html=True,)
    
    column_5, column_6, column_7 = st.beta_columns((2,6,6))
    
    date_1_resume = column_3.date_input('Start date:', df.index.min(), df.index.min(), df.index.max())
    
    date_2_resume = column_4.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today())

    def df_filter_date(message, df):#Función para filtrar el Dataframe por fechas
    
        filtered_df_date = df.loc[date_1_resume:date_2_resume]#Se filtra el Dataframe df, pasado como argumento entre los valores date_1 y date_2

        return filtered_df_date#Se devuelve el Dataframe filtrado
    
    filtered_df_date = df_filter_date('Select dates range to filter dataframe',df) ##2 TIPOS DATOS
                                                                                   ##CAMBIAR
    df_filter1=df_filt1.loc[date_1_resume:date_2_resume]
    
    df_filter0=df_filt0.loc[date_1_resume:date_2_resume]
    
    Data_chart0_title = column_6.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>SET 1 RESUME</p>", unsafe_allow_html=True,)
    
    Data_chart0 = column_6.empty()
    
    if variables_set_0==temp_humi_00:
        
        Data_chart01 = Data_chart0.line_chart(filtered_df_date[temp_humi_00])
        
    elif variables_set_0==options_list_0:
        
        Data_chart02 = Data_chart0.line_chart(df_filter0)
 
    Data_chart1_title = column_7.markdown("<p style='display: block; text-align: center; font-size: 20px; font-family: calibri; font-weight: bold'>SET 2 RESUME</p>", unsafe_allow_html=True,)
    
    Data_chart1 = column_7.empty()
    
    if variables_set_1==temp_humi_01:
        
        Data_chart11 = Data_chart1.line_chart(filtered_df_date[temp_humi_01])
        
    elif variables_set_1==options_list:
        
        Data_chart12 = Data_chart1.line_chart(df_filter1)
            
elif view_mode == 'Data Table':
    
    temp_humi_00 = column_0.multiselect(" ", df.columns.tolist())
    
    column_2.markdown("""<a style='display: block; height:100px; line-height:100px; text-align: center; font-size: 25px; font-family: calibri; font-weight: bold'>SELECT SET OF VARIABLES TO SHOW ON TABLE</a>""", unsafe_allow_html=True,)

    column_34, column_3, column_4 = st.beta_columns([1,2,2])   
    
    column_34.markdown("""<a style='display: block; height:115px; line-height:115px; text-align: center; font-size: 25px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</a>""", unsafe_allow_html=True,)
    
    date_1_table = column_3.date_input('Start date:', df.index.min(), df.index.min(), df.index.max())
    
    date_2_table = column_4.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today())

    def df_filter_date(message, df):#Función para filtrar el Dataframe por fechas
    
        filtered_df_date = df.loc[date_1_table:date_2_table]#Se filtra el Dataframe df, pasado como argumento entre los valores date_1 y date_2

        return filtered_df_date#Se devuelve el Dataframe filtrado
    
    filtered_df_date = df_filter_date('Select dates range to filter dataframe',df)
    
    filtered_df_date.index=filtered_df_date.index.strftime("%d/%m/%y\n%H:%M:%S")
    
    df_1=df.loc[date_1_table:date_2_table]
    
    if len(temp_humi_00)>0:
        data_table = st.table(filtered_df_date[temp_humi_00].style.set_precision(2))