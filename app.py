# -*- coding: utf-8 -*-
"""
Created on Mon May 10 15:17:03 2021

@author: scpgo
"""

import streamlit as st

from pygraphtec import  lee_fichero_sesion

import pandas as pd

from collections import deque

from datetime import timedelta, date

import time

import datetime

from threading import Event

st.set_page_config(layout="wide")

#df = lee_fichero_sesion("201112-165432.csv", path_sesiones='dataLogger')#Se ejecuta la función
df = lee_fichero_sesion("201112-180010.csv", path_sesiones='dataLogger')

column_1, column_2, column_0 = st.beta_columns((1,4,4))

i=0

view_mode = column_1.radio("SELECT VIEW MODE", ('Live', 'Resume', 'Data Table'))

if view_mode == 'Resume':
    
    temp_humi_00 = column_2.multiselect("SELECT FIRST SET OF VARIABLES TO PLOT", df.columns.tolist())
    
    column_2.markdown("<p style='display: block; text-align: center; font-size: 18px; font-family: calibri; font-weight: bold'>VARIABLES SET 1 SELECTED: "+str(len(temp_humi_00)), unsafe_allow_html=True,)
    
    temp_humi_01 = column_0.multiselect("SELECT SECOND SET OF VARIABLES TO PLOT", df.columns.tolist())
    
    column_0.markdown("<p style='display: block; text-align: center; font-size: 18px; font-family: calibri; font-weight: bold'>VARIABLES SET 2 SELECTED: "+str(len(temp_humi_01)), unsafe_allow_html=True,)
    
    column_34, column_3, column_4 = st.beta_columns([1,2,2])
    
    column_34.markdown("""<a style='display: block; height:115px; line-height:115px; text-align: center; font-size: 33px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</a>""", unsafe_allow_html=True,)
    
    column_5, column_6, column_7 = st.beta_columns((1,4,4))
    
    date_1_resume = column_3.date_input('Start date:', df.index.min(), df.index.min(), df.index.max())
    
    date_2_resume = column_4.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today())

    def df_filter_date(message, df):#Función para filtrar el Dataframe por fechas
    
        filtered_df_date = df.loc[date_1_resume:date_2_resume]#Se filtra el Dataframe df, pasado como 
                                                #argumento entre los valores date_1 y date_2

        return filtered_df_date#Se devuelve el Dataframe filtrado
    
    filtered_df_date = df_filter_date('Select dates range to filter dataframe',df)
    
    df_1=df.loc[date_1_resume:date_2_resume]
    df_1.index=df_1.index.strftime("%d/%m-%H:%M")
    
    Data_chart_title = column_6.markdown("<p style='display: block; text-align: center; font-size: 28px; font-family: calibri; font-weight: bold'>SET 1 ON RESUME GRAPH</p>", unsafe_allow_html=True,)

    Data_chart = column_6.line_chart(filtered_df_date[temp_humi_00])
 
    Data_chart1_title = column_7.markdown("<p style='display: block; text-align: center; font-size: 28px; font-family: calibri; font-weight: bold'>SET 2 ON RESUME GRAPH</p>", unsafe_allow_html=True,)
    
    Data_chart1 = column_7.line_chart(filtered_df_date[temp_humi_01])

if view_mode == 'Live':

    temp_humi_10 = column_0.multiselect("", df.columns.tolist())
    
    column_2.markdown("<p style='display: block; height:100px; line-height:100px; text-align: center; align: center; font-size: 28.5px; font-family: calibri; font-weight: bold'>SELECT SET OF VARIABLES TO PLOT LIVE</p>", unsafe_allow_html=True,)

    len_=len(temp_humi_10)
    data_tail = deque()
    time_tail = deque()
    
    i=0

    status_text=st.empty()
    
    while True:
        
        j=0
        
        if(i<(len(df)-1)):
            i=i+1
            
        data_tail.append(df[temp_humi_10].values[i]) ##
        time_tail.append(df.index[i])
        
        chart_data = pd.DataFrame(
             data_tail,
             index = time_tail,
             columns = temp_humi_10
        )
        
        df1 = pd.DataFrame(
            [df[temp_humi_10].values[i]],
            index = ["At: " + df.index[i].strftime('%d/%m/%y - %H:%M:%S')],
            columns = temp_humi_10)
        
        if(temp_humi_10 is None or len(temp_humi_10)==0):
            time.sleep(1) #necesario para que la aplicación arranque sin dar error de 
                          #'empty chart'
            chart = st.line_chart({})
        else:
            chart = st.line_chart(chart_data)
            status_text.table(df1.style.set_properties(**{'font-size': '15px','text-align': 'right'}).set_precision(2))
            
            for j in range(1):
                time.sleep(1)
                st.empty()
                
            chart.empty()
            chart.empty()
            #data_table.empty()
            
if view_mode == 'Data Table':
    
    #column_0.markdown("""<a style='display: block; text-align: center; font-size: 60px; font-family: calibri; font-weight: bold'>ALL SET OF VARIABLES</a>""", unsafe_allow_html=True,)
    
    temp_humi_00 = column_0.multiselect("", df.columns.tolist())
    
    column_2.markdown("""<a style='display: block; height:100px; line-height:100px; text-align: center; font-size: 28.5px; font-family: calibri; font-weight: bold'>SELECT SET OF VARIABLES TO SHOW ON TABLE</a>""", unsafe_allow_html=True,)

    column_34, column_3, column_4 = st.beta_columns([1,2,2])   
    
    column_34.markdown("""<a style='display: block; height:115px; line-height:115px; text-align: center; font-size: 33px; font-family: calibri; font-weight: bold'>PICK DATE RANGE</a>""", unsafe_allow_html=True,)
    
    date_1_table = column_3.date_input('Start date:', df.index.min(), df.index.min(), df.index.max())
    
    date_2_table = column_4.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today())

    def df_filter_date(message, df):#Función para filtrar el Dataframe por fechas
    
        filtered_df_date = df.loc[date_1_table:date_2_table]#Se filtra el Dataframe df, pasado como 
                                                            #argumento entre los valores date_1 y date_2

        return filtered_df_date#Se devuelve el Dataframe filtrado
    
    filtered_df_date = df_filter_date('Select dates range to filter dataframe',df)
    
    filtered_df_date.index=filtered_df_date.index.strftime("%d/%m/%y\n%H:%M:%S")
    
    df_1=df.loc[date_1_table:date_2_table]
    #df.index=df.index.strftime("%m/%d/%y\n%H:%M:%S")
    #data_table = st.table(df.style.set_precision(2))
    if len(temp_humi_00)>0:
        data_table = st.table(filtered_df_date[temp_humi_00].style.set_precision(2))