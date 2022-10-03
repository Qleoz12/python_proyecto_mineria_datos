import csv
import glob
from difflib import get_close_matches
from typing import final

import numpy as np
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, types
import os, sys

engine = create_engine(
        'mysql://root:root@127.0.0.1:3306/projecto_datos_abierto')  # enter your password and database names here

def load_data():
    # Use a breakpoint in the code line below to debug your script.

    path = "E:\\U\\mineria de datos\\Impo_2016\\Impo_2016\\*.csv"
    dirs = glob.glob(path)

    for file in dirs:
        # if file == '*.csv':
        #     print(file)
        df = pd.read_csv(file,
                         sep=',',
                         encoding='ISO-8859-1',
                         on_bad_lines='warn'
                         )  # Replace Excel_file_name with your excel sheet name
        df.to_sql(os.path.basename(file)[:-4], con=engine, index=False, if_exists='append')  # Rep


def read_data_mysql(mes):
    engine = create_engine(
        'mysql://root:root@127.0.0.1:3306/projecto_datos_abierto')  # enter your password and database names here
    return pd.read_sql('SELECT * FROM {}'.format(mes), con=engine)

def red_data_sqlserver():
    server = 'localhost\SERVIDORSQL'
    database = 'Import2016'
    username = 'sa'
    password = 'Carvajal2022'
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    # select 26 rows from SQL table to insert in dataframe.
    query = "SELECT TOP (1000) *  FROM [Import2016].[dbo].[Abril$];"
    df = pd.read_sql(query, cnxn)
    return df


def red_data_mongo(database, colletion,query):
    try:
        conn=conn_mongo()
        db = conn[database]
        cs=db[colletion].find(query)
        return cs

    except Exception as  e:
        print(e)
        conn.close()




def load_data_mongo(_dict, collection):
    try:
        conn=conn_mongo()
        db = conn.database
        # Insert Data
        rec_id1 = db[collection].insert_one(_dict)


    except Exception as  e:
        print(e)
        conn.close()

def conn_mongo():
    import pymongo

    MONGODB_HOST = 'localhost'
    MONGODB_PORT = '27017'
    MONGODB_TIMEOUT = 1000

    URI_CONNECTION = "mongodb://" + MONGODB_HOST + ":" + MONGODB_PORT + "/"

    try:
        client = pymongo.MongoClient(URI_CONNECTION)
        client.server_info()
        print('OK -- Connected to MongoDB at server %s' % (MONGODB_HOST))
        # client.close()
        return client
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print('Error with MongoDB connection: %s' % error)
    except pymongo.errors.ConnectionFailure as error:
        print('Could not connect to MongoDB: %s' % error)






if __name__ == '__main__':
    # load_data()
    emp_rec2 = {
        "name": "Mr.Shaurya",
        "eid": 14,
        "location": "delhi"
    }
    load_data_mongo(emp_rec2,"my_gfg_collection")

    load_data_mongo(emp_rec2, "test")

    data=red_data_mongo("database","scrap",{'DEPARTAMENTO':'Antioquia'})

    for x in data:
        print(x)