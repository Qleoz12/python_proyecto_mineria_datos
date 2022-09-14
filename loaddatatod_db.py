import csv
from difflib import get_close_matches

import pandas as pd
from sqlalchemy import create_engine, types

engine = create_engine(
        'mysql://root:root@127.0.0.1:3306/projecto_datos_abierto')  # enter your password and database names here

def load_data():
    # Use a breakpoint in the code line below to debug your script.





    df = pd.read_csv("E:\\U\\mineria de datos\\Impo_2016\\Impo_2016\\Diciembre\\Diciembre.csv",
                     sep=',',
                     encoding='ISO-8859-1',
                     on_bad_lines='warn'
                     )  # Replace Excel_file_name with your excel sheet name
    df.to_sql('diciembre', con=engine, index=False, if_exists='append')  # Rep



def read_data_mysql():
    engine = create_engine(
        'mysql://root:root@127.0.0.1:3306/projecto_datos_abierto')  # enter your password and database names here
    return pd.read_sql('SELECT * FROM diciembre', con=engine)


def inexistentes(df):

    n_records = len(df)
    for columna in df:
        print("{} | {} | {}".format(
            df[columna].name, len(df[df[columna].isnull()]) / (1.0 * n_records), df[columna].dtype
        ))




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # load_data()
    df=read_data_mysql()
    # print(df.values)
    # print(df.size)
    # print(df.describe())

    # print(list(df))
    # df.rename(columns={
    #     "DEPIM": "Departamento_del_importador",
    #     "NABAM": "Posición_arancelaria",
    #     "CANU": "Cantidad_de_unidades",
    #     "CODA": "Codigo_de_unidad",
    #     "PNK": "Peso_neto_en_kilos",
    #     "FECH": "Fecha_de_proceso",
    #     "VADUA": "Valor_Aduana",
    #     "TOTALIVAYO": "Total_IVA_y_otros_gastos",
    #     "PAISCOM": "Pais_de_compra",
    #     "PAISPRO": "Pais_productor",
    #     "PAISGEN": "Pais_origen",
    #     "VACIP": "Valor_en_pesos",
    #     "VAFODO": "Valor_en_dolares",
    #     "RZIMPO": "Valor_en_Razon_social_del_importador",
    #     "CLASE": "Clase_de_importador",
    # })

    # ADUA      Código de la aduana
    # PAISGEN   País origen
    # PAISPRO   País de procedencia
    # PAISCOM   País de compra
    # DEPTODES  Departamento destino
    # VIATRANS  Código vía de transporte
    # BANDERA
    # REGIMEN
    # ACUERDO
    # PBK       Peso bruto en kilos
    # PNK
    # CANU      Cantidad de unidades
    # CODA      Código de unidad
    # NABAN     Posición arancelaria
    # VAFODO    Valor FOB dólares de la mercancía
    # FLETE     Fletes
    # VACID     Valor CIF dólares de la mercancía
    # VACIP     Valor CIF pesos de la mercancía
    # IMP1      Impuesto a las ventas
    # OTDER     Otros Derechos
    # CLASE     Clase de importador
    # CUIDAIMP  Ciudad del importador
    # CUIDAEXP  Ciudad del exportador
    # ACTECON   Actividad económica
    # CODADAD   Código administración de aduana
    # VADUA     Valor aduana
    # VRAJUS    Valor ajuste
    # BASEIVA
    # OTROSP     Porcentaje otros
    # OTROSBASE
    # TOTALIVAYO  Total IVA y otros gastos
    # SEGUROS    Seguros
    # OTROSG     Otros gastos
    # LUIN       Lugar de ingreso
    # CODLUIN    Código lugar de ingreso
    # DEPIM      Departamento del importador
    # COPAEX     Código país del exportador
    # TIPOIM     Tipo de importación
    # PORARA     Porcentaje de arancel
    # NIT
    # DIGV       Digito de Verificación
    # RZIMPO
    # DEREL      Derechos Arancelarios
    # print(df.duplicated('RZIMPO'))


    df1 = df.groupby(['RZIMPO'])
    print(df1)
    # df1['duplicate']=df1.RZIMPO.map(lambda x: get_close_matches(x, df1.RZIMPO, n=2,cutoff=0.8))\
    #           .apply(pd.Series)
    # print (df1['duplicate'])
    print(df.dtypes)

    # print(df1.modelo_unico.value_counts()
    print(df.shape)
    # print(inexistentes(df1))
    #fecha
    print(df['PAISCOM'])

    df['pedidos_unicos'] = df.FECH.astype(str).str.cat([df.PAISGEN.astype(str), df.PAISPRO.apply(str)], sep='-')
    print(df)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/



