import csv
import glob
from difflib import get_close_matches

import numpy as np
import pandas as pd
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

if __name__ == '__main__':
    load_data()

