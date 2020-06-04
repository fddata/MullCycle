"""
Created on Wed Aug 07 22:25:54 2019

@author: Fraser D
"""

import pandas as pd
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt


csv_loc = 'C:\\Users\\Samsung\\Desktop\\Programs\\Python\\mull_cycle\\1_GettingData\\df_master.csv'

df = pd.read_csv(csv_loc, index_col=0, parse_dates=['time'])

df.time = (pd.to_datetime(df.time) - pd.to_datetime('today')) / np.timedelta64(1, 'h')

plt.close()

#count  DNF's 
dnf_count =  len(df.query('time == 0').index)
print( 'dnf_count: %s' % dnf_count)

#remove dnfs from the df
df = df.query('time != 0')

#how many NaN in the age col are there?
unknown_age_count =  sum(pd.isnull(df['age']))
print( 'unknown_age_count is: %s' % unknown_age_count)

#640 nan is a lot... is there a way we can back/forward fill missing ages if we know the age for one year?

#who has run the race more than once? we are assumes nobody shares a name.
multi = df.groupby('name').filter(lambda x: len(x) > 1 ).sort('name')

#we only want where people have at least one NaN and at least one non-nan number
#let's write a helper function for the filtering.   .sinull returns the nan, count returns non-nulls
def get_multiples(df):
    return ((df['age'].isnull().sum() > 0 ) & (df['age'].count() > 0 ))

multi = multi.groupby('name').filter(lambda x: get_multiples(x)).sort(['name', 'age'])
    
def get_age(x, known_age, known_year):
    return known_age - (known_year - x)    

def fill_blanks(df):
    known_year =  df.at[df.first_valid_index(), 'year']
    known_age = df.at[df.first_valid_index(), 'age']    
    unknown_rows = df.loc[df['age'].isnull()]
    unknown_rows.loc[:,['age']] = unknown_rows['year'].apply(lambda x : get_age(x, known_age, known_year))
    df.update(unknown_rows)
    return df

multi_filled = multi.groupby('name').apply(lambda x: fill_blanks(x))

df_mf = df.copy()
df_mf.update(multi_filled)

unknown_age_count2 =  sum(pd.isnull(df_mf['age']))
print( 'after age extrapolation, unknown_age_count is: %s' % unknown_age_count2)
print('age extrapolation added an extra %s data points' % (unknown_age_count - unknown_age_count2))

#new col for age grouping
def get_age_range(i):
    try:
        low_bound = (int(i)/10)*10  #note python 2.x floor division
        return str(low_bound) + ' - ' + str(low_bound + 9)
    except:
        return np.nan

df_mf['age_range'] = df_mf['age'].map(lambda x:  get_age_range(x), 1)

df_mf['year'].astype(int) #need to sort this out

#write output here for model
#df_mf.to_csv('C:\\Users\\Samsung\\Desktop\\Programs\\Python\\mull_cycle\\3_Model\\df_mf.csv', encoding='utf-8')   


#==============================================================================
# GRAPHS FROM HERE DOWN - uncomment to plot
#==============================================================================

#sns.boxplot(x='year', y= 'time', hue='course', palette='husl', data=df_mf).set(xlabel='Year', ylabel='Time (hrs)')


#shows averagehistogram of age range bins
#sns.countplot('age_range', data=df_mf, order=df_mf.age_range.value_counts().sort_index().keys().tolist())
#sns.countplot('age_range', data=df_mf, hue='gender', order=df_mf.age_range.value_counts().sort_index().keys().tolist())

# as above, but shows by course,
#sns.countplot('age_range', data=df_mf, hue='course', order=df_mf.age_range.value_counts().sort_index().keys().tolist())

#shows count by year, 1st one includes gender split.
#sns.countplot('year', data=df_mf, hue='gender')
#sns.countplot('year', data=df_mf, hue='course')
#sns.countplot('year', data=df_mf)

   
    
#scatter with age (decade) on x and time on y
sns.lmplot(x="age", y="time", data=df_mf, hue='gender', hue_order=["F", "M"], palette='husl', col='course').set(xlabel='Age', ylabel='Time (hrs)')


#scatter with x-age and y-time for course
##really good example for some simple clustering, 2nd is faceted on gender
#sns.lmplot(x='age', y='time', data=df_mf, hue='course').set(xlabel='Age (years)', ylabel='Time (hrs)')
#sns.lmplot(x='age', y='time', data=df_mf, hue='course').set(xlabel='Age (years)', ylabel='Time (hrs)')
sns.lmplot(x='age', y='time', data=df_mf, hue='course', fit_reg=False, col='gender').set(xlabel='Age (years)', ylabel='Time (hrs)')


#sns.lmplot(x='age', y='time', data=df_mf, hue='course', fit_reg=False).set(xlabel='Age (years)', ylabel='Time (hrs)')
   
   
#plt.scatter(df_mf.age, df_mf.time, label=df_mf.age_range, alpha=0.5)
#plt.title('Scatter plot pythonspot.com')
#plt.xlabel('x')
#plt.ylabel('y')
#plt.show()
