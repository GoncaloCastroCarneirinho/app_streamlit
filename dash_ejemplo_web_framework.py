# -*- coding: utf-8 -*-
"""
Created on Tue May 18 14:20:14 2021

@author: scpgo
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from datetime import timedelta
from pygraphtec import  lee_fichero_sesion

df = lee_fichero_sesion("201112-180010.csv", path_sesiones='/Users/scpgo/.spyder-py3/dataLogger') #LECTURA Y CREACIÓN DE DATAFRAME DE DATOS

app = dash.Dash() #CREACIÓN DE VARIABLE PARA SIMPLIFICAR LLAMADAS A FUNCIONES DE DASH

fig_names = df.columns #ASIGNACIÓN DE fig_names A LAS COLUMNAS DEL DATAFRAME

cols_dropdown = html.Div([ #DIV DE LOS FILTROS
    dcc.Dropdown(
        id='cols_dropdown', #IDENTIFICADOR DE FILTRO DE VARIABLES A SELECCIONAR
        options=[{'label': x, 'value': x} for x in fig_names], #CREACIÓN DEL FILTRO DE VARIABLES A SELECCIONAR
        value=None, #NINGUNA OPCIÓN INICIAL PRESELECCIONADA    
        multi=True #PERMITE LA SELECCIÓN DE VARIAS OPCIONES
    ),
    dcc.DatePickerRange(
        id='my-date-picker-range', #IDENTIFICADOR DE FILTRO DE RANGO DE FECHAS
        min_date_allowed=df.index.min()-timedelta(days=1), #FECHA MÍNIMA PERMITIDA
        max_date_allowed=df.index.max(), #FECHA MÁXIMA PERMITIDA
        initial_visible_month=df.index.min(), #AYUDA VISUAL DE FECHAS SELECCIONADAS
        start_date=df.index.min(), #FECHA INICIAL POR DEFECTO
        end_date=df.index.max())]) #FECHA FINAL POR DEFECTO

fig_plot = html.Div(id='fig_plot') #DIV DE LA GRÁFICA
app.layout = html.Div([cols_dropdown, fig_plot]) #CREACIÓN DE PANEL INTERACTIVO

@app.callback( #PERMITE DEVOLVER LA GRÁFICA COMO Dash Core Component dcc.Graph
dash.dependencies.Output('fig_plot', 'children'), #OUTPUT: REPRESENTACIÓN GRÁFICA
[dash.dependencies.Input('cols_dropdown', 'value'), #INPUT: FILTRO DE VARIABLES
 dash.dependencies.Input('my-date-picker-range', 'start_date'), #INPUT: FILTRO DE FECHA INICIAL
 dash.dependencies.Input('my-date-picker-range', 'end_date')]) #INPUT: FILTRO DE FECHA FINAL

def name_to_figure(value,start_date,end_date): #FUNCIÓN PARA CREACIÓN DE REPRESENTACIÓN GRÁFICA FILTRADA
    if value is None or len(value)==0 or start_date not in df.index:
        figure = {} #CREACIÓN DE REPRESENTACIÓN INICIAL VACÍA
    else:
        df_date_filter = df.loc[start_date:end_date] #DATAFRAME FILTRADO POR RANGO DE FECHAS
        figure=px.line(df_date_filter[value]) #CREACIÓN DE REPRESENTACIÓN GRÁFICA DE VARIABLES SELECCIONADAS
    return dcc.Graph(figure=figure)

app.run_server(debug=True, use_reloader=False) #ARRANQUE DE LA APLICACIÓN - DASH