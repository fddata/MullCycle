# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import pandas as pd

def get_data(year, driver):
    print 'getting %s data' % year
    cols_201X= ['name', 'gender' ,'age','time' ] # also 18,19
    df_201X = pd.DataFrame(columns=cols_201X)
    
    base_url = 'http://www.mullsportive.co.uk/results-'
    
    #driver = driver #webdriver.Chrome(executable_path=r'C:\Users\Samsung\Desktop\Programs\Python\Chromium\chromedriver.exe')
    driver.get(base_url + str(year))
    
    
    #click the bottom link first, so that it doesn't affect position of top link
    short_load = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="divRRPublish"]/div[4]/table/tbody[7]/tr/td/a[2]')));
    short_load.click()
    time.sleep(2.5)
    
    
#    long_load = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tb_1LoadAll"]/tr/td/a')));
    long_load = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="divRRPublish"]/div[4]/table/tbody[3]/tr/td/a[2]')));
    long_load.click()
    time.sleep(2.5)

    
    ###############
    ##NOW GET DFS##
    ###############
    try:
        loaded_page = driver.page_source
        soup = BeautifulSoup(loaded_page, 'html.parser')
        
        rows_long = soup.select("tbody[id=tb_1Data] > tr")
        tds_long = [row.findAll('td') for row in rows_long]
        
        rows_short = soup.select("tbody[id=tb_2Data] > tr")
        tds_short = [row.findAll('td') for row in rows_short]
        
        
        for td in tds_long:
            for index in sorted([0,1,2,5,7,9], reverse=True):
                del td[index]
        
        my_dict_long = [{cols_201X[i]: td[i].string for i in range(len(cols_201X))} for td in tds_long]
        
        
        for td in tds_short:
            for index in sorted([0,1,2,5,7,9], reverse=True):
                del td[index]
        
        my_dict_short = [{cols_201X[i]: td[i].string for i in range(len(cols_201X))} for td in tds_short]
        
        
        df_201X = df_201X.append(my_dict_long)
        df_201X['course'] = 'long'
        df_201X = df_201X.append(my_dict_short)
        df_201X['course'].fillna('short', inplace=True)
        df_201X['gender'] = df_201X['gender'].str.upper()
        df_201X.loc[df_201X['time'] == u'\xa0', 'time'] = '00:00:00,0' # replace &nbsp in time columns
        df_201X['time'] = pd.to_datetime(df_201X['time'], format= '%H:%M:%S,%f').dt.time
        df_201X['age'] = df_201X['age'].str.split().str[1].str[:2]
        df_201X['year'] = str(year)
    
    
    
    finally:
        pass
    return df_201X
