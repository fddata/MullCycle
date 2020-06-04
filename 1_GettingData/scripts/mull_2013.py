import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def get_data():
    print 'Getting 2013 data...'
    try:
        base_url = 'http://www.mullsportive.co.uk/results-'
        cols_2013 = ['name','course',  'time', 'gender']
        df_2013 = pd.DataFrame(columns=cols_2013)
    
        page = requests.get(base_url+'2013')
        soup = BeautifulSoup(page.content, 'html.parser')
        
        rows = soup.select("table[id=tablepress-7] > tbody > tr")
        tds = [row.findAll('td', class_=['column-1','column-2', 'column-4','column-5' ]) for row in rows]
        my_dict = [{cols_2013[i]: td[i].string for i in range(len(cols_2013))} for td in tds]
        df_2013 = df_2013.append(my_dict)
        df_2013.loc[df_2013['time'] == 'DNF', 'time'] = '00:00:00'
        df_2013['time'] = pd.to_datetime(df_2013['time'], format= '%H:%M:%S').dt.time
        df_2013['age'] = np.nan
        df_2013['gender'] = df_2013["gender"].str[:1]
        df_2013['year'] = '2013'
        df_2013['course'] = df_2013['course'].str.split(n=1).str[0].str.lower() 
        print 'Getting 2013 data... OK'
        return df_2013

    except Exception as e:
        print 'Get 2013 data failed with detail: ', e.message