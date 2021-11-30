import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from pywebio.output import put_file
from flask import Flask
from tracking_numbers import get_tracking

import time
import re

app = Flask(__name__)


def fedex_search(number):
    driver = webdriver.Chrome()
    driver.get(
        'https://www.google.com/search?q=fedex+tracking&rlz=1C1CHBF_enUS980US980&oq=fed&aqs=chrome.0.69i59j46i199i291i433i512j69i57j0i433i512j69i60l4.1096j0j7&sourceid=chrome&ie=UTF-8')

    search_bar = driver.find_element(By.CLASS_NAME, "Ym9xpb")
    search_bar.click()
    search_bar.send_keys(number)

    submit_btn = driver.find_element(By.CLASS_NAME, "fSXkBc")
    submit_btn.click()

    time.sleep(5)

    tracking = {'BOL/Tracking #': number, 'Shipped Location': driver.find_element(By.XPATH,
                                                                     "/html/body/app-root/div/div[2]/div/div/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/div[5]/trk-shared-to-from/div/div[2]/trk-shared-address/div/div[2]").text}
    driver.close()

    return tracking


if __name__ == "__main__":
    tracking_locations = []

    track, ncrt, ec_coco = get_tracking()

    for num in track[0:5]:
        print(num)
        try:
            tracking_locations.append(fedex_search(num))
        except:
            pass

    tracking_nums = pd.DataFrame(tracking_locations)
    new1 = tracking_nums['Shipped Location'].str.split(",", expand=True)
    new2 = tracking_nums['Shipped Location'].str.split(" ", expand=True)

    tracking_nums['SHIPPING_CITY'] = new1[0]
    tracking_nums['SHIPPING_STATE'] = new2[1]

    tracking_final = pd.merge(tracking_nums, ec_coco, on='BOL/Tracking #')
    results = pd.merge(tracking_final, ncrt, left_on='Request ID Number', right_on='REQUEST_ITEM_ID')
    results['MATCH'] = ""

    for rows in results:
        city = results['SHIPPING_CITY'][0]
        addy = results['SHIP_ADDRESS'][0]

    if re.search(city, addy, re.IGNORECASE):
        results['MATCH'] = 'TRUE'
    else:
        results['MATCH'] = 'FALSE'

    with pd.ExcelWriter('FedEx Address Validation.xlsx') as writer:
        results.to_excel(writer, index=False)

    results.to_excel('Fedex_Address_Validation.xlsx', index=False)

    data = open(writer, 'rb').read()
    put_file('FedEx Address Validation.xlsx', data, 'download')
