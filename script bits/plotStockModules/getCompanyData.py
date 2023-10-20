import yfinance as yf
import plotStockModules.numDays_ctk as numDays
import plotStockModules.getTicker_ctk as getTicker

def get_data():
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
