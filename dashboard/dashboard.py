import json

from dash import dcc, Output, Input, dash_table
import dash_html_components as html
import plotly.express as px
from dash import dash
import numpy as np
import pandas as pd

from loaddatatod_db import red_data_mongo


class  dashboard():


    def getdata(self, v,column):
        filter = "{}"
        cs = red_data_mongo("database", "scrap", {'DEPARTAMENTO': '{}'.format(filter.format(v.capitalize())) } )
        # cs = red_data_mongo("database","scrap",{'DEPARTAMENTO':'Antioquia'}).limit(1)
        print(filter.format(v.capitalize()))
        # print(list(cs))
        result=list(cs)

        if result:
            return float(result[0][column].replace(",","."))
        else:
            return 0

    def generate_table(self,dataframe, max_rows=10):
        return html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in dataframe.columns])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
                ]) for i in range(min(len(dataframe), max_rows))
            ])
        ])

    def dash_on(self):
        with open('departments.json', encoding='UTF-8') as f:
            data = json.load(f)

        import plotly.graph_objects as go

        # for tile in data['features']:
        #     print(tile['properties']['NOMBRE_DPT'])
        #     print(tile['properties']['DPTO'])

        # data2 = red_data_mongo("database", "scrap", {})
        #
        # for x in data2:
        #     print(x)

        list1 = ["05", "08", "11", "13", "15", "17", "18", "19", "20", "23", "25", "27", "41", "44", "47",
                 "50", "52", "54", "63", "66", "68", "70", "73", "76", "81", "85", "86", "91", "94", "95", "97", "99",
                 "88"]
        list3 = ["ANTIOQUIA", "ATLANTICO", "SANTAFE DE BOGOTA D.C", "BOLIVAR", "BOYACA", "CALDAS", "CAQUETA", "CAUCA",
                 "CESAR", "CORDOBA", "CUNDINAMARCA", "CHOCO", "HUILA", "LA GUAJIRA", "MAGDALENA", "META",
                 "NARIÑO", "NORTE DE SANTANDER", "QUINDIO", "RISARALDA", "SANTANDER", "SUCRE", "TOLIMA",
                 "VALLE DEL CAUCA", "ARAUCA", "CASANARE", "PUTUMAYO", "AMAZONAS", "GUAINIA", "GUAVIARE", "VAUPES",
                 "VICHADA",
                 "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA"]
        list2 = [(np.random.randn() + 3) * 100 for i in range(33)]
        df = pd.DataFrame(list(zip(list1, list2, list3)),
                          columns=['id', "DPTO", "Name"])

        df['id'] = df['id'].astype(str)



        df['PRODUCCION']=df['Name'].apply(lambda x:self.getdata(x,'PRODUCCIÓN (t)'))

        df['RENDIMIENTO'] = df['Name'].apply(lambda x: self.getdata(x, 'RENDIMIENTO (t/ha)'))

        df['AREA'] = df['Name'].apply(lambda x: self.getdata(x, 'ÁREA (ha)'))

        # print(df.loc[[1]])

        # df['importaciones'] = df['Name'].apply(lambda x: print(filter.format(x)) )

        fig = px.scatter_geo(
            df,
            locations="id",
            geojson=data,
            color="DPTO",
            featureidkey="properties.DPTO",
            hover_name="Name",
            center=dict(lat=4.570868, lon=-74.2973328),
            basemap_visible=True,
            size="PRODUCCION"
            # projection='eckert4'
            # lat="Latitude",
            # lon="Longitude",
        )

        fig.update_layout(
            autosize=True,
            height=600,
            geo=dict(
                center=dict(
                    lat=4.570868,
                    lon=-74.2973328
                ),
                scope='south america',
                projection_scale=6
            )
        )

        app = dash.Dash(__name__)

        _table=app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
        app.layout =html.Div(
            children=[
                html.Div(style={'textAlign': 'Center'}, children=[

                    dcc.Graph(
                        style={"height": "50vh"},
                        figure=fig,
                    )
                ]),
                html.Div(style={'textAlign': 'Center'}, children=[


                   self.generate_table(df),

                ]),

            ],
            className="wrapper",
        )










        app.run_server(debug=True)

if __name__ == '__main__':
    dashboard().dash_on()