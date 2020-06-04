import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_data():
    print 'Getting 2012 data...'
    try:
        base_url = 'http://www.mullsportive.co.uk/results-'
        cols_2012 = ['name','course', 'gender', 'time']
        df_2012 = pd.DataFrame(columns=cols_2012)      
        
        page = requests.get(base_url+'2012')
        soup = BeautifulSoup(page.content, 'html.parser')
        
        rows = soup.select("table[id=tablepress-8] > tbody > tr")
        tds = [row.findAll('td', class_=['column-1','column-2', 'column-3','column-4' ]) for row in rows]
        my_dict = [{cols_2012[i]: td[i].string for i in range(len(cols_2012))} for td in tds]
        df_2012 = df_2012.append(my_dict)
        df_2012.loc[df_2012['time'] == 'DNF', 'time'] = '00:00:00'
        df_2012['time'] = pd.to_datetime(df_2012['time'], format= '%H:%M:%S').dt.time
        df_2012['age'] = df_2012["gender"].str[1:]
        df_2012['gender'] = df_2012["gender"].str[:1]
        df_2012['year'] = '2012'
        df_2012['course'] = df_2012['course'].str.split(n=1).str[0].str.lower()  
        print 'Getting 2012 data... OK'
        return df_2012

    except Exception as e:
        print 'Get 2012 data failed with detail: ', e.message
        
        
    