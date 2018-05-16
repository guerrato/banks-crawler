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

def listBanks(countryLink):
    banks = dict()
    response = requests.get(countryLink)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    bankLinks = soup.body.find(class_='wrap').find(class_='content').find(class_='mid-col').find(class_='clearfix').find_all(class_='select-list-inner')[1].find('form').find('label').find('select').find_all('option')

    for b in bankLinks:
        if (b.get('value') != ''):
            banks[b.get_text()] = b.get('value')

    return banks

countries = listCountries(baseUrl)
print(listBanks(countries['Afghanistan']))
