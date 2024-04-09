import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = uc.ChromeOptions()
prefs = {"credentials_enable_service": False,
         "profile.password_manager_enabled": False}
options.add_experimental_option("prefs", prefs)

options.add_argument('--disable-save-password-bubble')
# options.add_argument('--blink-settings=imagesEnabled=false')
driver = uc.Chrome(options=options)
base_url = "https://web.datatree.com/#/home"
driver.get(base_url)
driver.maximize_window()


def read_credentials(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        username = lines[0].split(': ')[1].strip()
        password = lines[1].split(': ')[1].strip()
    return username, password


credentials_file = "credentials.txt"
username, password = read_credentials(credentials_file)

driver.find_element(By.CSS_SELECTOR, "#UserName").send_keys(username)
driver.find_element(By.CSS_SELECTOR, "#NextStep").click()
counter_element = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#password")))
time.sleep(2)

passs = driver.find_element(By.CSS_SELECTOR, "#password").send_keys(password)
driver.find_element(By.CSS_SELECTOR, "#next").click()

inp = input("Complete the filteration process and input here anything: ")
input_df=pd.read_excel("input.xlsx")


results = []
for s in range(len(input_df)):
    county = input_df.County[s]
    city=input_df.City[s]
    # if s > 0:
    dropdown = driver.find_element(By.CSS_SELECTOR,
                            "#advanced-filter-container > div > div > div:nth-child(2) > div.bundle-container > div.filter-component-container.filter-multi-dropdown.ng-isolate-scope.filter-CountyFips.fields.filter-full-length-with-op-and-select > div.chosen-container.chosen-container-multi.filter-main-values.fmd-values > ul > li > input")
    dropdown.send_keys(' ')

    print(county)
    try:
        
        dropdown.send_keys(county)
        time.sleep(1)
        dropdown.send_keys(Keys.ENTER)
        time.sleep(1)
        city_inp=driver.find_element(By.CSS_SELECTOR,'#advanced-filter-container > div > div > div:nth-child(3) > div.filter-component-container.filter-form-input.ng-isolate-scope.filter-6-Cities.fields > div.ffi-field-container.filter-main-values > input.ffi-input-field.ffi-single-input')
        city_inp.clear()
        time.sleep(1)
        city_inp.send_keys(city)
        time.sleep(1)
        city_inp.send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR,
                            "#searchFilter > div > div > div.modal-body > advanced-filters > applied-filters > div > div.view-result-section > div:nth-child(3) > a").click()
        time.sleep(3)
        number_string = driver.find_element(By.CSS_SELECTOR, "#counter").text
        number_string_without_comma = number_string.replace(",", "")
        count = int(number_string_without_comma)
        
        driver.find_element(By.CLASS_NAME, "search-choice-close").click()
        time.sleep(1)
        x=driver.find_element(By.CSS_SELECTOR,"#searchFilter > div > div > div.modal-body > advanced-filters > applied-filters > div > div.applied-filters > div:nth-child(2)").text
        if "city" in x.lower():
            driver.find_element(By.CSS_SELECTOR,"#searchFilter > div > div > div.modal-body > advanced-filters > applied-filters > div > div.applied-filters > div:nth-child(2) > div > div.applied-filter-container.ng-scope > table > tbody > tr > td.applied-display-right > div > div.tag.ng-scope > i").click()
            time.sleep(1)
            results.append([county,city, int(count)])
        else:
            results.append([county,city, 'Error1'])
    except:
        time.sleep(2)
        driver.find_element(By.PARTIAL_LINK_TEXT,'Deselect all').click()
        time.sleep(1)
        x=driver.find_element(By.CSS_SELECTOR,"#searchFilter > div > div > div.modal-body > advanced-filters > applied-filters > div > div.applied-filters > div:nth-child(2)").text
        if "city" in x.lower():
            driver.find_element(By.CSS_SELECTOR,"#searchFilter > div > div > div.modal-body > advanced-filters > applied-filters > div > div.applied-filters > div:nth-child(2) > div > div.applied-filter-container.ng-scope > table > tbody > tr > td.applied-display-right > div > div.tag.ng-scope > i").click()
        results.append([county,city, 'Error2'])
    if s%10==0:
        df = pd.DataFrame(results, columns=['County','City', 'Data Number'])
        df.to_excel('output.xlsx', index=False)
df = pd.DataFrame(results, columns=['County','City', 'Data Number'])
State = input("Enter your state name that you have selected:")

Low_limit = input("Enter Lower limit of Lot Acreahe you have selected: ")
Upp_limit = input("Enter Upper limit of Lot Acreahe you have selected: ")
filename = f"{State}_{Low_limit}_{Upp_limit}.xlsx"
df.to_excel(filename, index=False)
driver.quit()