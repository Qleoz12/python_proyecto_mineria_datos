import csv
import glob
import json
from difflib import get_close_matches
from typing import final

import numpy as np
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, types
import os, sys

engine = create_engine(
    'mysql://root:root@127.0.0.1:3306/projecto_datos_abierto?charset=utf8mb4')  # enter your password and database names here

def find_delimiter(filename):
    sniffer = csv.Sniffer()
    with open(filename) as fp:
        delimiter = sniffer.sniff(fp.read(5000)).delimiter
    return delimiter

def load_data():
    path = "D:/U/mineria/Impo/*/"
    dirs = glob.glob(path)

    for folder in dirs:
        files = glob.glob(folder + "/*.csv")
        for file in files:
            print(file)
            res=find_delimiter(file)
            print(res)
            # print(folder[-5:-1])
            df = pd.read_csv(file,
                             sep=res,
                             encoding='ISO-8859-1',
                             on_bad_lines='warn'
                             )  # Replace Excel_file_name with your excel sheet name
            df.rename(columns=lambda c: c.replace("ï»¿","") if c.find('ï»¿') else c)
            if 'NABAN' in df.columns:
                df_target = df.query('NABAN == 1005901100')
                print(df_target.size)
                df_target.to_sql(folder[-5:-1], con=engine, index=True, if_exists='replace',chunksize=500)  # Rep
            else:
                print("no encontrado en {}".format(file))


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


def read_data_mongo(database, colletion, query):
    try:
        conn = conn_mongo()
        db = conn[database]
        cs = db[colletion].find(query)
        return cs

    except Exception as  e:
        print(e)
        conn.close()


def load_data_mongo(_dict, collection):
    try:
        conn = conn_mongo()
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
        # print('OK -- Connected to MongoDB at server %s' % (MONGODB_HOST))
        # client.close()
        return client
    except pymongo.errors.ServerSelectionTimeoutError as error:
        print('Error with MongoDB connection: %s' % error)
    except pymongo.errors.ConnectionFailure as error:
        print('Could not connect to MongoDB: %s' % error)

def read_geojson():
    try:
        # Opening JSON file
        f = open('../departments.json', encoding='UTF-8')
        # returns JSON object as
        # a dictionary
        data = json.load(f)

        return data
    except:
        print("error loading geojson")

def getdata_mongo(v, column,year):
    filter = "{}"
    YEAR="{}"
    query= {'DEPARTAMENTO': {"$regex" : '{}'.format(filter.format(v))}, 'AÑO': '{}'.format(YEAR.format(year))}
    # print(query)
    cs = read_data_mongo("database", "scrap",query)
    # cs = red_data_mongo("database","scrap",{'DEPARTAMENTO':'Antioquia'}).limit(1)
    # print(filter.format(v.capitalize()))
    # print(list(cs))
    result = list(cs)
    if result:
        return float(result[0][column].replace(",", "."))
    else:
        return 0

def getdata_mysql(ano, filter):

    query = "projecto_datos_abierto." + str(ano) + "" + " " + filter + ";"
    return read_data_mysql(query)


if __name__ == '__main__':
    # load_data()
    # emp_rec2 = {
    #     "name": "Mr.Shaurya",
    #     "eid": 14,
    #     "location": "delhi"
    # }
    # load_data_mongo(emp_rec2,"my_gfg_collection")
    #
    # load_data_mongo(emp_rec2, "test")
    #
    # data=red_data_mongo("database","scrap",{'DEPARTAMENTO':'Antioquia'})
    #
    # for x in data:
    #     print(x)
    load_data()
