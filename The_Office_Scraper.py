#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup


# In[2]:


# get the content and return a list
def get_content(url):
    # Most websites refuse GET requests from python, so we change the header to pretend we're a browser.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


page = get_content('https://www.imdb.com/title/tt0386676/episodes?season=1&ref_=ttep_ep_sn_pv')


home='https://transcripts.foreverdreaming.org'
forum = 'https://transcripts.foreverdreaming.org/viewforum.php?f=574'
r = np.arange(25,176,25)
lim = '&start='

exceptions=['Updated: Editors Needed', 'Online Store']

url=[]
ep=[]

page = get_content('https://transcripts.foreverdreaming.org/viewforum.php?f=574')
print('Collecting URLs')
for item in page.find_all('a'):
    #print(str(item.get('class'))+';')
    if(str(item.get('class'))== "['topictitle']"):
        if item.get_text() not in exceptions:
            url.append(home+str(item.get('href'))[1:])
            ep.append(item.get_text())

for i in r:
    page_sulfix = lim+str(i)
    forum_list = forum + page_sulfix
    
    page = get_content(forum_list)
    
    for item in page.find_all('a'):
        if(str(item.get('class'))== "['topictitle']"):
            if item.get_text() not in exceptions:
                url.append(home+str(item.get('href'))[1:])
                ep.append(item.get_text())


df = pd.DataFrame(ep)
df.columns = ['ep']
df['url'] = url
print('URLs Collected')

char=[]
text=[]
ep=[]
print('Collecting Transcripts')
for i, row in df.iterrows():
    page = get_content(row.url)
    print(row.ep)
    for item in page.find_all('p'):
        if':' in item.get_text():
            temp = item.get_text().split(':',1)
            char.append(re.sub("[\[].*?[\]]", "", temp[0]))
            text.append(re.sub("[\[].*?[\]]", "", temp[1]))
            ep.append(row.ep)


df_lines = pd.DataFrame(char)
df_lines.columns = ['char']
df_lines['text'] = text
df_lines['ep'] = ep

df_lines = df_lines.drop(df_lines[df_lines['text']==' '].index).copy()
df_lines = df_lines.drop(df_lines[df_lines['text']==''].index).copy()

df_lines = df_lines[:-1]

print('Saving file')
df_lines.to_csv('the_office.csv', sep=';', encoding='utf-16')

