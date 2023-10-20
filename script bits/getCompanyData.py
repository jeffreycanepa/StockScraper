import yfinance as yf
import numDays
import getTicker

global company_name
global stockData

def get_data():
    global dates
    global company_name
    global stockData
    item = getTicker.ticker
    # Pseudo status
    print('Fetching data for', item, '...')
    stockData = yf.download(tickers = item,
                         start= numDays.dates[2],
                         end= numDays.dates[3])
    cmp = yf.Ticker(item)
    company_name = cmp.info['longName']
