import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def get_data():
    print 'Getting 2015 data...'
    try:
        base_url = 'http://www.mullsportive.co.uk/results-'
        
        cols_2015 = ['name','course',  'time', 'gender']
        
        df_2015 = pd.DataFrame(columns=cols_2015)
        page = requests.get(base_url+'2015')
        soup = BeautifulSoup(page.content, 'html.parser')
        
        rows = soup.select("table[id=tablepress-2] > tbody > tr")
        tds = [row.findAll('td', class_=['column-1','column-2', 'column-4','column-5' ]) for row in rows]
        my_dict = [{cols_2015[i]: td[i].string for i in range(len(cols_2015))} for td in tds]
        df_2015 = df_2015.append(my_dict)
        df_2015.loc[df_2015['time'] == 'DNF', 'time'] = '00:00:00'
        df_2015['time'] = pd.to_datetime(df_2015['time'], format= '%H:%M:%S').dt.time
        df_2015['age'] = np.nan
        df_2015['gender'] = df_2015["gender"].str[:1]
        df_2015['year'] = '2015'
        df_2015['course'] = df_2015['course'].str.split(n=1).str[0].str.lower()
        print 'Getting 2015 data... OK'
        return df_2015

    except Exception as e:
        print 'Get 2015 data failed with detail: ', e.message