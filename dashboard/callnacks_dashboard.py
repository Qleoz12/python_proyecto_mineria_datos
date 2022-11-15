import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
from dash import Output, Input

from dashboard.Utils import generate_table, data_imports
from loaddatatod_db import getdata_mysql, getdata_mongo


def register_callbacks(app):
    @app.callback(
        [Output("table-imports", "children"),
         Output("row-statics-b", "children")],
        [Input("localidad-filter", "value")])
    def update_charts(ano):
        df_mysql = getdata_mysql(ano, "")

        df_mysql_pbk = data_imports(df_mysql)

        details = dict()
        details["DEPARTAMENTO DESTINO"] = df_mysql_pbk.iloc[0]["DEPARTAMENTO DESTINO"]
        details["total"] = df_mysql_pbk.iloc[0]["PESO TONELADAS"]
        details["empresa"] = \
        df_mysql[df_mysql['DEPTODES'] == int(df_mysql_pbk.iloc[0]["DEPTODES"])].sort_values(by=['PNK'],
                                                                                            ascending=False).iloc[0][
            "RZIMPO"]

        return generate_table(df_mysql_pbk, "rete"), build_card(False, "mayor importador", details, "", [])

    @app.callback(
        [Output("table-productions", "children"),
         Output("row-statics-a", "children")],
        [Input("localidad-filter", "value")])
    def update_charts2(ano):
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

        df['PRODUCCION'] = df['Name'].apply(lambda x: getdata_mongo(x, 'PRODUCCIÓN (t)', ano))
        df['AREA'] = df['Name'].apply(lambda x: getdata_mongo(x, 'ÁREA (ha)', ano))
        df['RENDIMIENTO'] = df['Name'].apply(lambda x: getdata_mongo(x, 'RENDIMIENTO (t/ha)', ano))
        df = df.sort_values(by=['RENDIMIENTO'], ascending=False)

        details = dict()
        details["departamento"] = df.iloc[0]["Name"]
        details["produción"] = df.iloc[0]["PRODUCCION"]
        details["área"] = df.iloc[0]["AREA"]
        details["rendimiento"] = df.iloc[0]["RENDIMIENTO"]

        return generate_table(df, "rete"), build_card(False, "mayor productor", details, "", [])

    def build_card(imgTop, titles, details, img, links):
        cardbody = []

        cardbody.append(html.H1(titles.capitalize(), className="card-title"))
        cardbody.append(html.H3(str(list(details.values())[0]).capitalize(), className="card-title"))

        listgroup = dbc.ListGroup([dbc.ListGroupItem([f"{k}: {v} "]) for k, v in details.items()],
                                  flush=True, style={"width": "18rem"}, )
        cardbody.append(listgroup)

        if imgTop:
            card_content = \
                [
                    dbc.CardImg(src=img, top=False),
                    dbc.CardBody(
                        cardbody,
                        className="home-card-body"
                    ),
                ]

        else:
            card_content = \
                [
                    dbc.CardBody(
                        cardbody,
                        className="home-card-body"
                    ),
                    dbc.CardImg(src=img, top=True),
                ]

        card = dbc.Card(
            card_content,
            className="home-card h-100"
        )

        return dbc.Col(
            [card],
            style={"margin": "0.5rem"},
        )
