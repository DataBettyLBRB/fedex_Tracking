def fedex_search():
    driver = webdriver.Chrome()
    driver.get(
        'https://www.google.com/search?q=fedex+tracking&rlz=1C1CHBF_enUS980US980&oq=fed&aqs=chrome.0.69i59j46i199i291i433i512j69i57j0i433i512j69i60l4.1096j0j7&sourceid=chrome&ie=UTF-8')

    search_bar = driver.find_element(By.CLASS_NAME, "Ym9xpb")
    search_bar.click()
    search_bar.send_keys('1001891721360007011200285895109990')

    submit_btn = driver.find_element(By.CLASS_NAME, "fSXkBc")
    submit_btn.click()

    return driver.find_element(By.CLASS_NAME, "to-from--to")


driver.get(
        'https://www.fedex.com/fedextrack/?trknbr=1001891721360007011200285895109990&trkqual=2459528000~285895109990~FX')

    search_bar = driver.find_element(By.XPATH,
                                     "/html/body/app-root/div/div[2]/div/div/ng-component/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page/trk-shared-stylesheet-wrapper/div/div/trk-shared-detail-page-default/div/div/section[1]/div[5]/trk-shared-to-from/div/div[2]/trk-shared-address/div/div[2]").text
    print(search_bar)