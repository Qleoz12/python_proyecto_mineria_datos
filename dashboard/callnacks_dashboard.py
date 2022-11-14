import pandas as pd
from dash import Output, Input

from dashboard.Utils import generate_table, data_imports
from loaddatatod_db import getdata_mysql, getdata_mongo


def register_callbacks(app):
    @app.callback(
    Output("table-imports", "children"),[Input("localidad-filter", "value")])
    def update_charts(ano):
        df_mysql = getdata_mysql(ano,"")
        df_mysql_pbk = df_mysql.groupby(['DEPIM','DEPTODES'], as_index=False).sum()
        df_mysql_pbk['DEPIM'] = df_mysql_pbk['DEPIM'].astype(str).str.zfill(2)
        df_mysql_pbk = data_imports(df_mysql_pbk)
        return generate_table(df_mysql_pbk, "rete")

    @app.callback(
    Output("table-productions", "children"),[Input("localidad-filter", "value")])
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
        df=df.sort_values(by=['RENDIMIENTO'],ascending=False)
        return generate_table(df, "rete")
