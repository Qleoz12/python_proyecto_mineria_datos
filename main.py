
# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import matplotlib
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

from loaddatatod_db import read_data_mysql, red_data_sqlserver


def inexistentes(df):

    n_records = len(df)
    for columna in df:
        print("{} | {} | {}".format(
            df[columna].name, len(df[df[columna].isnull()]) / (1.0 * n_records), df[columna].dtype
        ))


# Validacion de crecimiento de demanda por medio de los valores duplicados para lo cual tomamos los valores de FECH=Fecha_de_proceso, PAISGEN=Pais_origen
# NABAM=Posición_arancelaria que es con la cual identificamos el tipo de producto y PAISPRO=Pais_productor, de modo que por medio de este vamos a saber
# cual es el tipo que mas veces se importa de la misma procedencia identificando así los lugares de los cuales se empieza a depender mas para evaluar
# el porque de esta procedencia con las de mas consultas
def duplicados(df):

    df['Crecimiento_Demanda'] = df.FECH.astype(str).str.cat([df.PAISGEN.astype(str), df.PAISPRO.astype(str),
                                                             df.PAISCOM.astype(str), df.NABAN.apply(str)], sep='-')
    print(df)

    # Listamos y Revisamos las colmunas que tengan alto numero de duplicados

    print(df.Crecimiento_Demanda.value_counts())

    # Revisamos variables en las que se encuentren gran cantidad de registros con el mismo valor

    n_records = len(df)

    def valores_duplicados_col(df):
        for columna in df:
            n_por_valor = df[columna].value_counts()
            mas_comun = n_por_valor.iloc[0]
            menos_comun = n_por_valor.iloc[-1]
            print("{} | {}-{} | {}".format(
                df[columna].name,
                round(mas_comun / (1.0 * n_records), 3),
                round(menos_comun / (1.0 * n_records), 3),
                df[columna].dtype
            ))

    valores_duplicados_col(df)

    # Graficamos el resltado de nuestra consulta

    print(df.Crecimiento_Demanda.value_counts(normalize=True).plot.barh())

#Creamos nuestra funcion para validar los valores inexistentes
def inexistentes(df):
    n_records = len(df)

    def valores_inexistentes_col(df):
        for columna in df:
            print("{} | {} | {}".format(
                df[columna].name, len(df[df[columna].isnull()]) / (1.0 * n_records), df[columna].dtype
            ))

    valores_inexistentes_col(df)

def outliers_col(df):
        for columna in df:
            if df[columna].dtype != object:
                n_outliers = len(df[np.abs(stats.zscore(df[columna])) > 3])
                print("{} | {} | {}".format(
                    df[columna].name,
                    n_outliers,
                    df[columna].dtype
                ))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    #    df=read_data_mysql()
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


    #df1 = df.groupby(['RZIMPO'])
    #print(df1)
    # df1['duplicate']=df1.RZIMPO.map(lambda x: get_close_matches(x, df1.RZIMPO, n=2,cutoff=0.8))\
    #           .apply(pd.Series)
    # print (df1['duplicate'])
    #print(df.dtypes)

    # print(df1.modelo_unico.value_counts()
    #print(df.shape)
    # print(inexistentes(df1))
    #fecha
    #print(df['PAISCOM'])

    #df['pedidos_unicos'] = df.FECH.astype(str).str.cat([df.PAISGEN.astype(str), df.PAISPRO.apply(str)], sep='-')
    #print(df)

    #outliers_col(df)
    #df.boxplot(column='TIPOIM')
    #matplotlib.use('TkAgg')
    #plt.interactive(False)
    #plt.show()


## Esta es la validacion de los duplicados para calcular el crecimiento de demanda basados en el pais la fecha
##


    df = red_data_sqlserver()
    duplicados(df)
    inexistentes(df)