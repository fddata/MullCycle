import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

def get_data(driver):
    print 'Getting 2019 data...'
    try:
        cols_2019 = ['name', 'age' ,'gender','time' ] # also 18,19
        df_2019 = pd.DataFrame(columns=cols_2019)
        
        base_url = 'http://www.mullsportive.co.uk/results-'
        
        driver.get(base_url + '2019')
        
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

        loaded_page = driver.page_source
        soup = BeautifulSoup(loaded_page, 'html.parser')
        
        rows_long = soup.select("tbody[id=tb_2Data] > tr")
        tds_long = [row.findAll('td') for row in rows_long]
        
        rows_short = soup.select("tbody[id=tb_1Data] > tr")
        tds_short = [row.findAll('td') for row in rows_short]
        
        
        for td in tds_long:
            for index in sorted([0,1,2,6,8], reverse=True):
                del td[index]
        
        my_dict_long = [{cols_2019[i]: td[i].string for i in range(len(cols_2019))} for td in tds_long]
        
        
        for td in tds_short:
            for index in sorted([0,1,2,6,8], reverse=True):
                del td[index]
        
        my_dict_short = [{cols_2019[i]: td[i].string for i in range(len(cols_2019))} for td in tds_short]
        
        
        df_2019 = df_2019.append(my_dict_long)
        df_2019['course'] = 'long'
        df_2019 = df_2019.append(my_dict_short)
        df_2019['course'].fillna('short', inplace=True)
        df_2019['gender'] = df_2019['gender'].str.upper()
        df_2019.loc[df_2019['time'] == u'\xa0', 'time'] = '00:00:00' # replace &nbsp in time columns
        df_2019['time'] = pd.to_datetime(df_2019['time'], format= '%H:%M:%S').dt.time
        df_2019['age'] = (2019 - df_2019['age'].astype(int))
        df_2019['year'] = '2019'
       # df_2019.to_csv('C:\\Users\\Samsung\\Desktop\\Programs\\Python\\mull_cycle\\2019!!!.csv', encoding='utf-8')    
        
        print 'Getting 2019 data... OK'
        return df_2019
        
    except Exception as e:
        print 'Get 2019 data failed with detail: ', e.message
