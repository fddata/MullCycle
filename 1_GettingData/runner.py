"""
Author = Fraser D
"""
import pandas as pd
from selenium import webdriver
import timeit

from scripts import mull_2011
from scripts import mull_2012
from scripts import mull_2013
from scripts import mull_2014
from scripts import mull_2015
from scripts import mull_2016
from scripts import mull_2017
from scripts import mull_2018
from scripts import mull_2019

start_time = timeit.default_timer()
driver = webdriver.Chrome(executable_path=r'C:\Users\Samsung\Desktop\Programs\Python\Chromium\chromedriver.exe')

df_master = pd.DataFrame()

df_master = df_master.append(mull_2011.get_data(), ignore_index=True)
df_master = df_master.append(mull_2012.get_data(), ignore_index=True)
df_master = df_master.append(mull_2013.get_data(), ignore_index=True)
df_master = df_master.append(mull_2014.get_data(), ignore_index=True)
df_master = df_master.append(mull_2015.get_data(), ignore_index=True)
df_master = df_master.append(mull_2016.get_data(), ignore_index=True)
df_master = df_master.append(mull_2017.get_data(driver), ignore_index=True)
df_master = df_master.append(mull_2018.get_data(driver), ignore_index=True)
df_master = df_master.append(mull_2019.get_data(driver), ignore_index=True)

driver.close()
   
df_master.to_csv('C:\\Users\\Samsung\\Desktop\\Programs\\Python\\mull_cycle\\1_GettingData\\df_master.csv', encoding='utf-8')   

print ('runner.py completed in %f seconds' %  (timeit.default_timer() - start_time))