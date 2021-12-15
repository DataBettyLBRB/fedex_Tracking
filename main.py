import argparse

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from pywebio.platform.flask import webio_view
from pywebio.output import *
from pywebio import start_server
from flask import Flask

import argparse

from tracking_numbers import get_tracking

import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

app = Flask(__name__)


def fedex_search(number):
    GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.binary_location = GOOGLE_CHROME_PATH

    driver = webdriver.Chrome(execution_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    driver.get(
        'https://www.google.com/search?q=fedex+tracking&rlz=1C1CHBF_enUS980US980&oq=fed&aqs=chrome.0.69i59j46i199i291i433i512j69i57j0i433i512j69i60l4.1096j0j7&sourceid=chrome&ie=UTF-8')

    search_bar = driver.find_element(By.CLASS_NAME, "Ym9xpb")
    search_bar.click()
    search_bar.send_keys(number)

    try:
        submit_btn = driver.find_element(By.CLASS_NAME, "fSXkBc")
        submit_btn.click()

        time.sleep(5)
        tracking = driver.find_element(By.XPATH,
                                       "/html/body/app-root/div/div[2]/div/div/ng-component/trk-shared-stylesheet-wrapper"
                                       "/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-"
                                       "detail-page-default/div/div/section[1]/div[5]/trk-shared-to-from/div/div[2]/trk-"
                                       "shared-address/div/div[2]").text

    except:
        tracking = 'ERROR'

    driver.close()

    return tracking


def main():
    df = get_tracking()

    df['BOL/Tracking #'] = df['BOL/Tracking #'].str.extract(r'(\d+)')
    null_df = df[df.SHIP_ADDRESS.isnull()]
    df = df[df.SHIP_ADDRESS.notnull()]

    put_html('<h3>Fedex Tracking</h3>')

    match, fedex_city = [], []
    for idx, row in df.iterrows():
        put_row([put_text(idx), put_text(row['BOL/Tracking #'])])

        city = fedex_search(row['BOL/Tracking #']).split(',')[0]
        df['Fedex_City'] = city

        address = row['SHIP_ADDRESS']

        if city.lower() in address.lower():
            Match = 'TRUE'
            match.append(Match)

        elif city.lower() not in address.lower():
            if '-' in city:
                city = city.replace('-', ' ')
            elif len(city.split(' ', 1)) > 1:
                city = city.split(' ', 1)[1]
            else:
                city = city

            if city.lower() in address.lower():
                Match = 'TRUE'
                match.append(Match)
            else:
                Match = 'FALSE'
                match.append(Match)

        fedex_city.append(city)

        put_row([put_text(address), None, put_text(city), None, put_text(Match)], size='60% 10px 25% 10px 15%')
        put_row([None, put_text('_____________________________________________________________________________')],
                size='270px 100%')

    df['Match'] = match
    df['Fedex_City'] = fedex_city

    put_text('WRITING DATA TO FILE FOR DOWNLOAD')

    with pd.ExcelWriter('Fedex_Address_Validation.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    results = open(writer, 'rb').read()
    put_file('Fedex_Address_Validation.xlsx', results, 'download')

    put_text('PROCESS COMPLETE')

    app.add_url_rule('/', 'webio_view', webio_view(main), methods=['GET', 'POST', 'OPTIONS'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port, auto_open_webbrowser=True)