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

def listBankCities(banksLink):
    cities = dict()
    response = requests.get(banksLink)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    bankLinks = soup.body.find(class_='wrap').find(class_='content').find(class_='mid-col').find(class_='clearfix').find_all(class_='select-list-inner')[2].find('form').find('label').find('select').find_all('option')

    for c in bankLinks:
        if (c.get('value') != ''):
            cities[c.get_text()] = c.get('value')

    return cities

countries = listCountries(baseUrl)

banks = listBanks(countries['Afghanistan'])

cities = listBankCities(banks['AFGHAN UNITED BANK'])

print(cities)
