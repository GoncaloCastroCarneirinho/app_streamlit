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

st.set_page_config(layout="wide")

df = lee_fichero_sesion("201112-165432.csv", path_sesiones='dataLogger')#Se ejecuta la función

column_1, column_2 = st.beta_columns((1,2))

i=0

view_mode = column_1.radio("View mode:", ('Live', 'Resume'))

column_3, column_4 = st.beta_columns([1,1])

column_5, column_6 = st.beta_columns(2) 

if view_mode == 'Resume':
    
    date_1 = column_3.date_input('Start date:', df.index.min(), df.index.min(), df.index.max())
    
    date_2 = column_4.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today())

    def df_filter_date(message, df):#Función para filtrar el Dataframe por fechas
    
        filtered_df_date = df.loc[date_1:date_2]#Se filtra el Dataframe df, pasado como argumento,
                                                #entre los valores date_1 y date_2

        return filtered_df_date#Se devuelve el Dataframe filtrado
    
    filtered_df_date = df_filter_date('Select dates range to filter dataframe',df)
    
    temp_humi = column_2.multiselect("Select variable: ", df.columns.tolist())
    
    Data_table_title = column_5.title('Data Table')
    Data_table = column_5.write(filtered_df_date[temp_humi])
    
    Data_chart_title = column_6.title('Data Chart')
    Data_chart = column_6.line_chart(filtered_df_date[temp_humi])
    
    #Información de las fechas y horarios seleccionados
    #st.info('Start: **%s** End: **%s**' % (date_1, date_2))   
 
elif view_mode == 'Live':
    
    st.title('Data Chart')
    
    temp_humi = column_2.multiselect("Select variable: ", df.columns.tolist())
    
    len_=len(temp_humi)
    data_tail = deque() ###
    time_tail = deque()
    
    column_3.empty()
    column_3.empty()
    column_4.empty()
    column_4.empty()
    column_5.empty()
    column_5.empty()
    column_6.empty() 
    column_6.empty()
    
    i=0
    
    while True:
        if(i<(len(df)-1)):
            i=i+1
        
        data_tail.append(df[temp_humi].values[i]) ##
        time_tail.append(df.index[i])
        
        chart_data = pd.DataFrame(
             data_tail,
             index = time_tail,
             columns = temp_humi
        )
        
        column_7, column_8 = st.beta_columns((6,2)) 
        
        if(temp_humi is None or len(temp_humi)==0):
            time.sleep(1) #necesario para que la aplicación arranque sin dar error de 
                          #'empty chart'
            chart = st.line_chart({})
        else:
            chart = column_7.line_chart(chart_data)
            data_table = column_8.dataframe(chart_data)
            time.sleep(20)
            chart.empty()
            chart.empty()
            data_table.empty()