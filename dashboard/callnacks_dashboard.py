import traceback


import pandas as pd
from dash import Output, Input

from dashboard.Utils import generate_table, data_imports, build_card
from loaddatatod_db import getdata_mysql, getdata_mongo, read_geojson
import plotly.express as px

def register_callbacks(app):
    @app.callback(
        [Output("table-imports", "children"),
         Output("row-statics-b", "children"),
         Output("figure-imports", "figure")],
        [Input("localidad-filter", "value")])
    def update_datatable_imports(ano):
        try:
            df_mysql = getdata_mysql(ano, "")

            df_mysql_pbk = data_imports(df_mysql)

            details = dict()
            details["DEPARTAMENTO DESTINO"] = df_mysql_pbk.iloc[0]["DEPARTAMENTO DESTINO"]
            details["total"] = df_mysql_pbk.iloc[0]["PESO TONELADAS"]
            details["empresa"] = \
            df_mysql[df_mysql['DEPTODES'] == int(df_mysql_pbk.iloc[0]["DEPTODES"])].sort_values(by=['PNK'],
                                                                                                ascending=False).iloc[0]["RZIMPO"]
            geojson = read_geojson()
            df_mysql_pbk["PNK"] = df_mysql_pbk["PNK"].astype(str).str.replace(",", ".").astype(float)  # adjustment for 2017 and 2018
            df_mysql_pbk["PBK"] = df_mysql_pbk["PBK"].astype(str).str.replace(",", ".").astype(float)  # adjustment for 2017 and 2018

            df_mysql_pbk_fig = df_mysql_pbk.groupby(['DEPTODES','DEPARTAMENTO DESTINO'], as_index=False).sum()
            fig_imports = px.choropleth(
                df_mysql_pbk_fig,
                locations="DEPTODES",
                geojson=geojson,
                color="PESO TONELADAS",
                featureidkey="properties.DPTO",
                hover_name="DEPARTAMENTO DESTINO",
                center=dict(lat=4.570868, lon=-74.2973328),
                basemap_visible=True,
                # size="PBK"
                # projection='eckert4'
                # lat="Latitude",
                # lon="Longitude",
            )

            fig_imports.update_layout(
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

            return generate_table(df_mysql_pbk, "rete"), build_card(False, "mayor importador", details, "", []),fig_imports
        except Exception as e:
            print(e)
            traceback.print_exc()

    @app.callback(
        [Output("table-productions", "children"),
         Output("row-statics-a", "children"),
         Output("figure-productions", "figure")],
        [Input("localidad-filter", "value")])
    def update_datatable_productions(ano):
        try:
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

            geojson = read_geojson()

            fig = px.choropleth(
                df,
                locations="id",
                geojson=geojson,
                color="RENDIMIENTO",
                featureidkey="properties.DPTO",
                hover_name="Name",
                center=dict(lat=4.570868, lon=-74.2973328),
                basemap_visible=True,
                # size="PRODUCCION"
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


            return generate_table(df, "rete"), build_card(False, "mayor productor", details, "", []),fig

        except Exception as e:
            print(e)
            traceback.print_exc()

