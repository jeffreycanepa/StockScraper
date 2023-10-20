import yfinance as yf
import plotStockModules.numDays_ctk as numDays_ctk
import plotStockModules.getTicker_ctk as getTicker_ctk

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
