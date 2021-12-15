import numpy as np
from numpy import nan
import pandas as pd
import datetime
from pywebio.input import file_upload

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def get_tracking():
    today = datetime.datetime.now()
    month = today.strftime("%b").upper()
    year = today.strftime("%Y")
    date = str(month + year)

    ncrt = file_upload(label="Upload NCRT File Here", accept='.xls*')
    ec_coco = file_upload(label="Upload EC_COCO File Here", accept='.xls*')

    read_ncrt = pd.read_excel(ncrt['content'], skiprows=[0])
    read_ec_coco = pd.read_excel(ec_coco['content'], usecols=['Request ID Number', 'BOL/Tracking #',
                                                              'Carrier'], sheet_name=date).dropna()

    df_ncrt = read_ncrt[["REQUEST_ITEM_ID", "SHIP_ADDRESS", "DLA_NUM"]]

    # EXTRACTED THE FEDEX NAMES
    df_coco = read_ec_coco[read_ec_coco['Carrier'].str.contains('FED')]
    df_coco = df_coco.rename(columns={'Request ID Number': 'REQUEST_ITEM_ID'})

    return pd.merge(df_coco, df_ncrt, how='left', on=['REQUEST_ITEM_ID'])
