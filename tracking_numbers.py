import pandas as pd
from pywebio.input import file_upload


def get_tracking():

    ncrt = file_upload(label="Upload NCRT File Here", accept='.xls*')
    ec_coco = file_upload(label="Upload EC_COCO File Here", accept='.xls*')

    read_ncrt = pd.read_excel(ncrt['content'], skiprows=[0])
    read_ec_coco = pd.read_excel(ec_coco['content'], usecols=['Request ID Number', 'BOL/Tracking #', 'Carrier',
                                                   'Local Stock Number (LSN)'])

    #
    df_ncrt = read_ncrt[["REQUEST_ITEM_ID", "SHIP_ADDRESS", "DLA_NUM"]]
    df_coco = read_ec_coco[(read_ec_coco.Carrier == "FEDEX")]

    tracking = [rows for rows in df_coco['BOL/Tracking #']]
    return tracking, df_ncrt, df_coco
