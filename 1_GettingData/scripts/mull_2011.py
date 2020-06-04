import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def get_data():
    print 'Getting 2011 data...'
    try:
        base_url = 'http://www.mullsportive.co.uk/results-'
        cols_2011 = ['name','course', 'time', 'gender']
        df_2011 = pd.DataFrame(columns=cols_2011)
        
        page = requests.get(base_url+'2011')
        soup = BeautifulSoup(page.content, 'html.parser')
        
        rows = soup.select("table[id=tablepress-10] > tbody > tr")
        tds = [row.findAll('td', class_=['column-1','column-2', 'column-4','column-5' ]) for row in rows]
        my_dict = [{cols_2011[i]: td[i].string for i in range(len(cols_2011))} for td in tds]
        df_2011 = df_2011.append(my_dict)
        df_2011['age'] = np.nan
        df_2011.loc[df_2011['time'] == 'DNF', 'time'] = 0.00
        df_2011['time'] = pd.to_datetime(df_2011['time'], format='%H.%M').dt.time
        df_2011['year'] = '2011'
        df_2011['course'] = df_2011['course'].str.split(n=1).str[0].str.lower() 
        print 'Getting 2011 data... OK'
        return df_2011
    
    except Exception as e:
        print 'Get 2011 data failed with detail: ', e.message
        