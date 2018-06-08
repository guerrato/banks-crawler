import bs4
import json
import time
import requests

baseUrl = 'https://banksifsccode.com/swift-codes/'
countries = []

def listCountries(url):
    countries = []
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    countryLinks = soup.body.find(class_='wrap').find(class_='content').find(class_='mid-col').find_all(class_='altCl')

    for c in countryLinks:
        if (c.a != None):
            countries.append({'name': c.a.get_text(), 'url': c.a.get('href'), 'crawled': False})
    
    return countries

def listBanks(countryLink):
    banks = []
    response = requests.get(countryLink)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    bankLinks = soup.body.find(class_='wrap').find(class_='content').find(class_='mid-col').find(class_='clearfix').find_all(class_='select-list-inner')[1].find('form').find('label').find('select').find_all('option')

    for b in bankLinks:
        if (b.get('value') != ''):
            banks.append({'name': b.get_text(), 'url': b.get('value'), 'crawled': False})

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

def listBranchData(branchLink):
    data = dict()
    response = requests.get(branchLink)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    table = soup.body.find(class_='wrap').find(class_='content').find(class_='mid-col').find('div', class_='clearfix').find(class_='data-disp').find('table')

    lines = table.find_all('tr')

    for l in lines:
        key = l.find('p', class_='ifTit').get_text().replace(':', '').strip().lower()
        data[key] = l.find('p', class_='ifDta').get_text()

    return data

def generateStatusFile(data, name, append = False, beautify = True):
    mode = 'w'
    indent = 4

    if append == True:
        mode = 'a'
    
    if beautify == False:
        indent = None

    with open((name + '.json'), mode=mode, encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=indent)

choice = input("Would you like crawl everything again? (y/N) ")

if choice == 'y':
    countries = listCountries(baseUrl)
    generateStatusFile(countries, 'countries')

    for country in countries:
        print('Started: ' + country['name'])
        banks = listBanks(country['url'])
        generateStatusFile(banks, 'banks', append = True, beautify = False)

        # for bank in banks:

            
        #     for keyCity, valueCity in listBankCities(valueBank).items():
        #         for keyBranches, valueBranches in listBankBranches(valueCity).items():
        #             branchData.append(listBranchData(valueBranches))
        # print(country['name'] + ' was crawled!')
        
# exit()
    # banks = listBanks(countries['Brazil'])
# generateStatusFile(countries, 'countries')

# cities = listBankCities(banks['BANCO ITAUBANK S A'])

# branches = listBankBranches(cities['SAO PAULO'])

# branchData = []

# for key, value in branches.items():
#     branchData.append(listBranchData(value))


# with open('banks.json', mode='w', encoding='utf-8') as outfile:
#     json.dump(branchData, outfile, sort_keys=True, indent=4)

print('Done! Check the result in banks.json file!')
