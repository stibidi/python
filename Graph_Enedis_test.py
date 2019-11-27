#!/usr/bin/env python
# coding: utf-8

import pickle
import pandas as pd
import datetime
import plotly
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

# =============================================================

with open('C:/BMT/csv_python/IP3/source/datasites_test2.pickle', 'rb') as datafile :
    datas = pickle.load(datafile)
print('loaded')
#data = pickle.load('C:/BMT/csv_python/IP3/source/datasites_test1.pickle')

# =============================================================

PRMs = []
PRMs = list(datas.keys())
prm = PRMs[0]

for PRM in PRMs :
	print(PRM)
	df = pd.DataFrame()
	df = datas[PRM]['cdc']
	df = df.rename(columns={"Date de la mesure":"jr","Heure de la mesure":"hr","Valeur":"PA"})
	datas[PRM]['cdc'] = df
	df2 = datas[PRM]['cdc']['jr']+' '+datas[PRM]['cdc']['hr']
	df3 = pd.to_datetime(df2, format='%d-%m-%Y %H:%M')
	datas[PRM]['cdc']['dtime'] = df3
	inf_s = []
	inf_s = datas[PRM]['infos_sites']['Site'].index
	infs = inf_s[0]
	PS = datas[PRM]['admin_sites']['PS'][infs][:-3]
	
# =============================================================

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'grisclair': '#858175', 
	'grisfonce': '#4d4d4d',
    'orange': '#f26f2e',
	'blanc': '#ffffff'
    }

# =============================================================

app.layout = html.Div(
				style={'backgroundColor': colors['blanc']},
				children=[
			    html.H1(
			    	children='Courbe de Charge', 
			    	style={'textAlign': 'center', 'color':colors['orange']}
			    	),
			    html.H2(
			    	children='Relevés de Puissance toutes les 10mn (kW)', 
			    	style={'textAlign': 'center', 'color': colors['grisfonce']}
			    	),

				html.Div([
    				html.Label('Sélectionner un PRM'),
    				dcc.Dropdown(
        				id='PRMselect',
        				options=[
        					{'label': i, 'value': str(i)} for i in PRMs],
        				value= prm
    					),

					html.Hr(),

    				# html.Label('Informations sur le PRM sélectionné:'),
				    # dash_table.DataTable(
				    # 	id='datatable_infos',
				    # 	columns = (
				    # 		[{'id': 'Site', 'nom_site': 'NomSite'}]+
				    # 		[{'id': p, 'name': p} for p in params]
    				# 	),
    				# 	data = [
    				# 		]

    				# ),	
			    	
					html.Div([
						dcc.Graph(
					        id='graph_cdc',
					        #figure={} parti dans le return du callback
					        )
				    	]),
				],
			    	style={'textAlign': 'center', 'color':colors['orange']}
			    	),
			])

#========================== Callbacks pour update les éléments du contenu ===================================================

@app.callback(
	Output(component_id='graph_cdc', component_property='figure'),
	[Input(component_id='PRMselect', component_property='value')])

def update_graph(PRMselect):
	prm = '{}'.format(PRMselect)
	prm = str(prm)
	df_graph = pd.DataFrame()
	df_graph = datas[prm]
	dfg2 = pd.DataFrame()
	dfg2 = df_graph['cdc']
	dfg2 = dfg2[(dfg2['PA'] > 0)]
	valSP = dfg2['PA'] /1000
	jours = dfg2['dtime']
	inf_s = []
	inf_s = datas[prm]['infos_sites']['Site'].index
	infs = inf_s[0]
	site = datas[prm]['infos_sites']['Site'][infs]
	PSs = datas[prm]['admin_sites']['PS'][infs]
	PS = datas[prm]['admin_sites']['PS'][infs][:-3]
	titre = 'Valeurs 10mn - '+prm+' - '+site+' - '+PSs
	print(PS,' , ',infs,' , ',min(jours),' , ',max(jours))

	data = [
			go.Scatter(x = jours, y = valSP, name = 'prm', 
				mode = 'lines', connectgaps=True, line = dict(color='orange', width = 0.5)),
			
			]
	lyt = go.Layout(
	xaxis=dict(range=[min(jours),max(jours)]),
	yaxis=dict(range=[min(valSP),max(valSP)]),
	xaxis_rangeslider_visible=True,title_text = titre,
	shapes = [{'type' : 'line', 'xref' : 'x', 'x0' : min(jours), 'y0' : int(PS), 
				'yref' : 'y', 'x1' : max(jours), 'y1' : int(PS), 'name' : 'P.S.', 
				'line' : {'color' : 'red', 'width' : 1.5}
				}],
			)

	return {
		'data': data, 'layout': lyt
		}

if __name__ == '__main__':
    app.run_server(debug=True)
