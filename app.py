# -*- coding: utf-8 -*-
"""
Created on Mon May 10 15:17:03 2021

@author: scpgo
"""

import streamlit as st

from pygraphtec import  lee_fichero_sesion

from datetime import timedelta, date, time

import datetime

df = lee_fichero_sesion("201112-165432.csv", path_sesiones='dataLogger')#Se ejecuta la función

def df_filter_date(message, df):#Función para filtrar el Dataframe por fechas
    
    filtered_df_date = df.loc[date_1:date_2]#Se filtra el Dataframe df, pasado como argumento,
                                            #entre los valores date_1 y date_2

    return filtered_df_date#Se devuelve el Dataframe filtrado
    
def df_filter_time(message, df):#Función para filtrar el Dataframe por horas
     
     filtered_df_time = df.loc[time_1:time_2]#Se filtra el Dataframe df, pasado como argumento,
                                             #entre los valores time_1 y time_2

     return filtered_df_time#Se devuelve el Dataframe filtrado
    
if __name__ == '__main__':
    
    column_1, column_2, column_3 = st.beta_columns(3)#Se estructura la visualización de la 
                                                     #aplicación mediante columnas del mismo
                                                     #tamaño
    with column_1:
        #Se crea el filtro para seleccionar la primera fecha (de primer dia del df hasta hoy)
        date_1 = st.date_input('start date', df.index.min(), df.index.min(), datetime.date.today())
        #Se crea el filtro para seleccionar el primer valor de horario
        time_1 = st.time_input('start time', time(00,00,00))

    with column_2:
        #Se crea el filtro para seleccionar la segunda fecha (del sgundo día del df hasta hoy)
        date_2 = st.date_input('end date', date_1+datetime.timedelta(days=1), date_1+datetime.timedelta(days=1), datetime.date.today())            
        #Se crea el filtro para seleccionar el segundo valor de horario
        time_2 = st.time_input('end time', time(23,30,00))
        
    with column_3:
        #Se crea el filtro para seleccionar las variables a graficar
        temp_humi = st.multiselect("Select variable to plot: ", df.columns.tolist())
    
    #Información de las fechas y horarios seleccionados
    st.info('Start: **%s** at **%s** End: **%s** at **%s**' % (date_1, time_1, date_2, time_2))   
 
    #Filtramos nuestro Dataframe 'df' en fecha y tiempo llamando a las funciones creadas
    filtered_df_date = df_filter_date('Select dates range to filter dataframe',df)
    filtered_df_time = df_filter_time('Select times range to filter dataframe',df)

    column_1, column_2 = st.beta_columns(2)#Se estructura la visualización de la aplicación 
                                           #mediante columnas del mismo tamaño

    with column_1:
        #Se dibuja la tabla de valores del Dataframe 'df' existente
        st.title('Data Frame')
        st.write(filtered_df_date[temp_humi])

    with column_2:
        #Se grafican las variables previamente seleccionadas
        st.title('Chart')
        st.line_chart(filtered_df_date[temp_humi])        