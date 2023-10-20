import yfinance as yf
import numDays_ctk
import getTicker_ctk

def get_data():
    global company_name
    global stockData
    item = getTicker_ctk.ticker
    # Pseudo status
    print('Fetching data for', item, '...')
    stockData = yf.download(tickers = item,
                         start= numDays_ctk.dates[2],
                         end= numDays_ctk.dates[3])
    cmp = yf.Ticker(item)
    company_name = cmp.info['longName']
