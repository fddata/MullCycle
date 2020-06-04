import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_data():
    print 'Getting 2014 data...'
    try:
        base_url = 'http://www.mullsportive.co.uk/results-'
        
        cols_2014 = ['name','course',  'time', 'age','gender']
        
        df_2014 = pd.DataFrame(columns=cols_2014)
        
        
        page = requests.get(base_url+'2014')
        soup = BeautifulSoup(page.content, 'html.parser')
        
        rows = soup.select("table[id=tablepress-6] > tbody > tr")
        tds = [row.findAll('td', class_=['column-1','column-2', 'column-4','column-5','column-6' ]) for row in rows]
        my_dict = [{cols_2014[i]: td[i].string for i in range(len(cols_2014))} for td in tds]
        df_2014 = df_2014.append(my_dict)
        df_2014.loc[df_2014['time'] == 'DNF', 'time'] = '00:00:00'
        df_2014['time'] = pd.to_datetime(df_2014['time'], format= '%H:%M:%S').dt.time
        df_2014['gender'] = df_2014["gender"].str[:1]
        df_2014['year'] = '2014'
        df_2014['course'] = df_2014['course'].str.split(n=1).str[0].str.lower()
        print 'Getting 2014 data... OK'
        return df_2014

    except Exception as e:
        print 'Get 2014 data failed with detail: ', e.message