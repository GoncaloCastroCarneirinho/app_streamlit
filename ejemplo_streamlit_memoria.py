# -*- coding: utf-8 -*-
"""
Created on Sat Aug 28 21:27:36 2021

@author: scpgo
"""

import streamlit as st
from pygraphtec import  lee_fichero_sesion
from datetime import timedelta, date
import time
import datetime
from collections import deque
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")

#df = lee_fichero_sesion("201112-165432.csv", path_sesiones='dataLogger')
df = lee_fichero_sesion("201112-180010.csv", path_sesiones='dataLogger')

st.title('Datetime Filter')
    
column_1,column_2 = st.beta_columns((1,2))

i=0

with column_1:
    #temp_humi = st.multiselect("Select variable: ", df.columns.tolist())
    view_mode = st.radio("View mode:", ('Live', 'Resume')) ###
    
column_3, column_4 = st.beta_columns([1,1])

column_5, column_6 = st.beta_columns(2)     

if view_mode == 'Resume':
    
    date_1 = column_3.date_input('Start date:', df.index.min(), df.index.min(), datetime.date.today())

    date_2 = column_4.date_input('End date:', df.index.max(), df.index.min()+timedelta(days=1), datetime.date.today())
        
    def df_filter_date(message, df):
 
        filtered_df_date = df.loc[date_1:date_2]

        return filtered_df_date
 
    filtered_df_date = df_filter_date('Select dates range to filter dataframe',df)
    
    temp_humi = column_2.multiselect("Select variable: ", df.columns.tolist())

    column_5.title('Data Table')
    column_5.write(filtered_df_date[temp_humi])

    column_6.title('Data Chart')
    column_6.line_chart(filtered_df_date[temp_humi])
        
elif view_mode == 'Live':
    
    st.title('Data Chart')
    
    temp_humi = column_2.multiselect("Select variable: ", df.columns.tolist())
    
    len_=len(temp_humi)
    real_tail = deque() ###
    real_tail2 = deque()
    
    if(len(temp_humi)>0):
        i=1
        st.title('+1')
    
    column_3.empty()
    column_3.empty()
    column_4.empty()
    column_4.empty()
    column_5.empty()
    column_5.empty()
    column_6.empty() 
    column_6.empty()
    
    while True:
        # Get some data.
        data2 = np.array({})
        data3 = np.array((np.random.randint(0,20)),int)
        real_tail.append(data3) ##
        real_tail2.append(data3)
        chart_data = pd.DataFrame(
             real_tail,
             columns = temp_humi
        )
        chart = st.line_chart(chart_data)
        if(temp_humi is None or len(temp_humi)==0):
            chart = st.line_chart({})
        else:
            time.sleep(5)
            chart.empty()
            chart.empty()