import csv
from difflib import get_close_matches

import numpy as np
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

if __name__ == '__main__':
    pass