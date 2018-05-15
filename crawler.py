# import urllib
import time

import bs4
import requests

baseUrl = 'https://banksifsccode.com/swift-codes/'
countries = []

def listCountries(url):
    countries = dict()
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    countryLinks = soup.body.find(class_='wrap').find(class_='content').find(class_='mid-col').find_all(class_='altCl')

    for c in countryLinks:
        if (c.a != None):
            countries[c.a.get_text()] = c.a.get('href')
    
    return countries

def listBanks(country):
    pass

countries = listCountries(baseUrl)

# for c in countries.keys():
#     print(countries[c])