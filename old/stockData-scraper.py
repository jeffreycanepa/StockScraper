'''This is a simple stock price scraper as described at 
https://www.scraperapi.com/blog/how-to-scrape-stock-market-data-with-python/
This is just meant as a means for me to learn how to use pyhon and at the 
same time track some stocks of interest (to me).  Original code by Zoltan Bettenbuk.
'''
# /opt/homebrew/bin/python3

import requests
from requests.exceptions import HTTPError, Timeout
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlencode
import datetime

# My Scraperapi.com API key
myApiKey = 'd244474ba73a08e90252a036c5c0fc5f'

# My Stocks
urls = ['https://www.investing.com/equities/apple-computer-inc',
        'https://www.investing.com/equities/adobe-sys-inc',
        'https://www.investing.com/equities/network-appliance-inc',
        'https://www.investing.com/equities/cisco-sys-inc',
        'https://www.investing.com/equities/microsoft-corp',
        'https://www.investing.com/equities/amazon-com-inc',
        'https://www.investing.com/equities/tesla-motors',
        'https://www.investing.com/equities/vm-ware-inc',
        'https://www.investing.com/equities/docusign-inc',
        'https://www.investing.com/equities/splunk-inc',
        'https://www.investing.com/equities/general-electric',
        'https://www.investing.com/etfs/spdr-select-sector---utilities']

# Get current date
today = datetime.datetime.now().strftime('%Y-%m-%d')

# Create/open csv file for storing data
file = open('stockprices.csv', 'w')
writer = csv.writer(file)
writer.writerow(['Date', 'Company', 'Price', 'Change', '% Change'])
writer.writerow([today, '', '', '', ''])

# Loop through supplied stocks and get data
for url in urls:
    # Use Scraperapi.com to funnel our url requests through
    params = {'api_key': myApiKey, 'url' : url}
    try:
        page = requests.get('http://api.scraperapi.com/', params=urlencode(params))
    except HTTPError as err:
        print("Error: {0}".format(err))
    except Timeout as err:
        print("Request timed out: {0}".format(err))

    # Extract the data we want
    soup = BeautifulSoup(page.text, 'html.parser')
    company = soup.find('h1', {'class': 'text-xl text-left font-bold leading-7 md:text-3xl md:leading-8 mb-2.5 md:mb-2 text-[#232526] rtl:soft-ltr'}).text
    price = soup.find('div', {'class': 'text-5xl font-bold leading-9 md:text-[42px] md:leading-[60px] text-[#232526]'}).text
    change = soup.find('div', {'class': 'text-base font-bold leading-6 md:text-xl md:leading-7 rtl:force-ltr'}).text
    pctChange = soup.find('div', {'class': 'text-base font-bold leading-6 md:text-xl md:leading-7 rtl:force-ltr'}).text

    
    # Print the data to screen.  This is serving as a makeshift status widget
    print('Loading:', url)
    print('\t',company, price, change, pctChange)

    # Write the data to a csv file
    writer.writerow(['', company, price, 
                 change, pctChange])

file.close()