import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash import dash
import dash_bootstrap_components as dbc
from dash import dcc, dash_table

from dashboard.callnacks_dashboard import register_callbacks
from loaddatatod_db import read_geojson, getdata_mongo, getdata_mysql


# TODO grafica de historico cantidades por mes y rankings por año
# el objetivo del movimiento del departamento el que mas importa menos produce
# estrategias de produccion


class dashboard():
    years = range(2012, 2022)
    app = None

    def dash_on(self):
        external_stylesheets = \
            [
                {
                    "href": "https://fonts.googleapis.com/css2?"
                            "family=Lato:wght@400;700&display=swap",
                    "rel": "stylesheet",
                },
            ]

        geojson = read_geojson()
        year_default = "2013"

        list1 = ["05", "08", "11", "13", "15", "17", "18", "19", "20", "23", "25", "27", "41", "44", "47",
                 "50", "52", "54", "63", "66", "68", "70", "73", "76", "81", "85", "86", "91", "94", "95", "97", "99",
                 "88"]
        list3 = ["ANTIOQUIA", "ATLANTICO", "SANTAFE DE BOGOTA D.C", "BOLIVAR", "BOYACA", "CALDAS", "CAQUETA", "CAUCA",
                 "CESAR", "CORDOBA", "CUNDINAMARCA", "CHOCO", "HUILA", "LA GUAJIRA", "MAGDALENA", "META",
                 "NARIÑO", "NORTE DE SANTANDER", "QUINDIO", "RISARALDA", "SANTANDER", "SUCRE", "TOLIMA",
                 "VALLE DEL CAUCA", "ARAUCA", "CASANARE", "PUTUMAYO", "AMAZONAS", "GUAINIA", "GUAVIARE", "VAUPES",
                 "VICHADA",
                 "ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA"]

        df = pd.DataFrame(list(zip(list1, list3)), columns=['id', "Name"])
        df['id'] = df['id'].astype(str)

        df['PRODUCCION'] = df['Name'].apply(lambda x: getdata_mongo(x, 'PRODUCCIÓN (t)', year_default))

        df['RENDIMIENTO'] = df['Name'].apply(lambda x: getdata_mongo(x, 'RENDIMIENTO (t/ha)', year_default))

        df['AREA'] = df['Name'].apply(lambda x: getdata_mongo(x, 'ÁREA (ha)', year_default))

        df_mysql = getdata_mysql("2013", "")

        desired_width = 320
        pd.set_option('display.width', desired_width)
        pd.set_option('display.width', 400)
        pd.set_option('display.max_columns', 22)

        df_mysql_pbk = df_mysql.groupby(['DEPIM'], as_index=False).sum()
        df_mysql_pbk['DEPIM'] = df_mysql_pbk['DEPIM'].astype(str).str.zfill(2)
        # print(df_mysql_pbk)




        app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        register_callbacks(app)

        _table = app.layout = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
        app.layout = html.Div(
            children=[
                html.Div(
                    children=[
                        html.P(children="🌽", className="header-emoji"),
                        html.H1(
                            children="Colombian Corn Analytics", className="header-title"
                        ),
                        html.P(
                            children="Analyze the behavior of Corn prices"
                                     " and the number of corn imports vs own prodcttion"
                                     " between 2016 and 2021",
                            className="header-description",
                        ),
                        html.P(children="🌽", className="header-emoji"),
                    ],
                    className="header",
                ),
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                html.Div(children="Años ", className="menu-title"),
                                dcc.Dropdown(
                                    id="localidad-filter",
                                    options=[
                                        {"label": ano, "value": ano}
                                        for ano in self.years
                                    ],
                                    value="2013",
                                    clearable=False,
                                    className="dropdown",
                                ),
                            ]
                        )
                    ],
                    className="",
                ),
                dbc.Row(id="row-statics", children=[
                    dbc.Col(id="row-statics-a"),
                    dbc.Col(id="row-statics-b"),
                ], style={"display": "flex",
                          "justify-content": "center"}),
                html.Div(style={'textAlign': 'Center'}, children=[
                    html.P(children="production", className="header-title"),
                    dcc.Graph(
                        id="figure-productions",
                        style={"height": "50vh"},
                    )
                ]),

                html.Div(style={'textAlign': 'Center'},
                         id="table-productions",
                         children=[]),
                html.Div(style={'textAlign': 'Center'}, children=[
                    html.P(children="importations", className="header-title"),
                    dcc.Graph(
                        style={"height": "50vh"},
                        id="figure-imports",
                    )
                ]),
                html.Div(
                    style={'textAlign': 'Center'},
                    id="table-imports",
                    children=[]),

            ],
            className="wrapper",
        )

        app.run_server(debug=True)


if __name__ == '__main__':
    dashboard().dash_on()
