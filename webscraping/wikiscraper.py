import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re


# Scraps wiki data about gdp
def scrap():
    r = requests.get('https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita')

    gdptable = r.text
    soup = BeautifulSoup(gdptable, 'lxml')
    table = soup.find('table', attrs = {"class" :"wikitable sortable"})

    theads=[]
    for tx in table.findAll('th'):
        theads.append(tx.text)

    data =[]
    for rows in table.findAll('tr'):
            row={}
            i=0
            for cell in rows.findAll('td'):
                row[theads[i]]=re.sub('\xa0', '',cell.text)
                i+=1
            if len(row)!=0:
                data.append(row)
    print(data)
    gdp = pd.DataFrame(data)
    print(gdp.head())
    gdp = gdp.rename(columns={'US$': 'gdp_per_capita'})
    gdp['gdp_per_capita'] = gdp['gdp_per_capita'].apply(lambda x: re.sub(',', '', x))
    gdp['gdp_per_capita'] = gdp['gdp_per_capita'].apply(pd.to_numeric)
    print(gdp.head())
    gdp50000 = gdp[gdp['gdp_per_capita'] > 50000]
    gdp50000.hist()
if __name__ == '__main__':
    scrap()