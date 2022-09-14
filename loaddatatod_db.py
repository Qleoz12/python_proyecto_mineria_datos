import csv
import pyodbc as pyodbc
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10,10)

#from sqlalchemy import create_engine, types

#engine = create_engine(
#        'mysql://root:root@127.0.0.1:3306/projecto_datos_abierto')  # enter your password and database names here

#def load_data():
    # Use a breakpoint in the code line below to debug your script.





#    df = pd.read_csv("E:\\U\\mineria de datos\\Impo_2016\\Impo_2016\\Diciembre\\Diciembre.csv",
#                    sep=',',
#                     encoding='ISO-8859-1',
#                     on_bad_lines='warn'
#                     )  # Replace Excel_file_name with your excel sheet name
#    df.to_sql('diciembre', con=engine, index=False, if_exists='append')  # Rep



#def read_data_mysql():
#    engine = create_engine(
#        'mysql://root:root@127.0.0.1:3306/projecto_datos_abierto')  # enter your password and database names here
#    return pd.read_sql('SELECT * FROM diciembre', con=engine)


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
    # load_data()
#    df=read_data_mysql()
    # print(df.values)
#    print(df.size)
#    print(df.describe())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

server = 'localhost\SERVIDORSQL'
database = 'Import2016'
username = 'sa'
password = 'Carvajal2022'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# select 26 rows from SQL table to insert in dataframe.
query = "SELECT TOP (1000) *  FROM [Import2016].[dbo].[Abril$];"
df = pd.read_sql(query, cnxn)
print(df.head(26))
#print(df.tail(26))

df.info()
df.index

df.shape
print(df.head(26))

#Validacion de crecimiento de demanda por medio de los valores duplicados

df['Crecimiento_Demanda'] = df.FECH.astype(str).str.cat([df.PAISGEN.astype(str), df.NABAN.apply(str)], sep='-')
print(df)
print(df.Crecimiento_Demanda.value_counts())
print(df.Crecimiento_Demanda.value_counts(normalize=True).plot.barh());

#Validacion de valores inexistentes

n_records = len(df)
def valores_inexistentes_col(df):
    for columna in df:
        print("{} | {} | {}".format(
            df[columna].name, len(df[df[columna].isnull()]) / (1.0*n_records), df[columna].dtype
        ))

valores_inexistentes_col(df)


#Validacion de Outliers

from scipy import stats
import numpy as np

def outliers_col(df):
    for columna in df:
        if df[columna].dtype != object:
            n_outliers = len(df[np.abs(stats.zscore(df[columna])) > 3])
            print("{} | {} | {}".format(
                df[columna].name,
                n_outliers,
                df[columna].dtype
        ))

outliers_col(df)


df.boxplot(column='TIPOIM');
