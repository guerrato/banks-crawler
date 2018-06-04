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

def listBankBranches(citiesLink):
    branches = dict()
    response = requests.get(citiesLink)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    citiesLink = soup.body.find(class_='wrap').find(class_='content').find(class_='mid-col').find(class_='clearfix').find_all(class_='select-list-inner')[3].find('form').find('label').find('select').find_all('option')

    for c in citiesLink:
        if (c.get('value') != ''):
            branches[c.get_text()] = c.get('value')

    return branches

def branchData(branchLink):
    data = dict()
    response = requests.get(branchLink)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    table = soup.body.find(class_='wrap').find(class_='content').find(class_='mid-col').find('div', class_='clearfix').find(class_='data-disp').find('table')

    lines = table.find_all('tr')

    data['bank'] = lines[0].find('p', class_='ifDta').get_text()
    data['country'] = lines[1].find('p', class_='ifDta').get_text()
    data['city'] = lines[2].find('p', class_='ifDta').get_text()
    data['swift'] = lines[3].find('p', class_='ifDta').get_text()
    data['address'] = lines[4].find('p', class_='ifDta').get_text()

    return data

countries = listCountries(baseUrl)

banks = listBanks(countries['Brazil'])

cities = listBankCities(banks['BANCO ITAUBANK S A'])

branches = listBankBranches(cities['SAO PAULO'])

branchData = branchData(branches['Sao Paulo Branch'])

print(branchData)
