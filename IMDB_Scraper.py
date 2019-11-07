#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


# get the content and return a list
def get_content(url):
    # Most websites refuse GET requests from python, so we change the header to pretend we're a browser.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


page = get_content('https://www.imdb.com/title/tt0386676/episodes?season=8')


ratings, ep_name, ep_num, season = [],[],[],[]

for s in np.arange(1,10):
    temp_ratings, temp_ep_name, temp_ep_num, temp_season = [],[],[],[]

    counter = 1
    for i in page.find_all('span'):
        class_name = dict(i.attrs).get('class')
        if class_name == ['ipl-rating-star__rating']:
            # print(dict(i.attrs).get('class'))
            temp_ratings.append(i.get_text())
    temp_ratings = temp_ratings[::23]

    for i in page.find_all('a'):
        class_name = dict(i.attrs).get('itemprop')
        # print(class_name)
        if class_name == 'name':
            temp_ep_name.append(i.get_text())
            temp_ep_num.append(counter)
            temp_season.append(s)
            counter += 1
            print('Season ' + str(s) + ', episode ' + str(counter) + ' collected')
            
    ratings.extend(temp_ratings)
    ep_name.extend(temp_ep_name)
    ep_num.extend(temp_ep_num)
    season.extend(temp_season)
        
df = pd.DataFrame(ep_name)
df.columns = ['ep_name']
df['ep_num'] = ep_num
df['season'] = season
df['ratings'] = ratings


df.to_csv('ratings.csv', sep=';', encoding='utf-16')

