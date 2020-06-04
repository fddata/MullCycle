import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def get_data():
    print 'Getting 2016 data...'
    try:   
        base_url = 'http://www.mullsportive.co.uk/results-'
        
        cols_2016 = ['name','course',  'time', 'gender']
        df_2016 = pd.DataFrame(columns=cols_2016)
        page = requests.get(base_url+'2016')
        soup = BeautifulSoup(page.content, 'html.parser')
        
        rows = soup.select("table[id=tablepress-4] > tbody > tr")
        tds = [row.findAll('td', class_=['column-1','column-2', 'column-4','column-5' ]) for row in rows]
        my_dict = [{cols_2016[i]: td[i].string for i in range(len(cols_2016))} for td in tds]
        df_2016 = df_2016.append(my_dict)
        df_2016.loc[df_2016['time'] == 'DNF', 'time'] = '00:00:00'
        df_2016['time'] = pd.to_datetime(df_2016['time'], format= '%H:%M:%S').dt.time
        df_2016['age'] = np.nan
        df_2016['gender'] = df_2016["gender"].str[:1]
        df_2016['year'] = '2016'
        df_2016['course'] = df_2016['course'].str.split(n=1).str[0].str.lower() 
        print 'Getting 2016 data... OK'
        return df_2016
        
    except Exception as e:
        print 'Get 2016 data failed with detail: ', e.message


