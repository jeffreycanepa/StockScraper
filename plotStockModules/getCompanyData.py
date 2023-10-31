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
    try:
        # company_name = cmp.info['longName']

        # yfinance info seems to be flakey, so get company name by other means
        company_name = get_company_name(item)
    except:
        company_name = item

def get_company_name(ticker):
    import requests, re

    url = 'https://finance.yahoo.com/quote/WMT/'
    url = url.replace("WMT",ticker)

    req = requests.get(url)
    html = req.text

    name = re.search(r'\<title>([^\s]+)\ ([^\s]+)', html)
    result = str(name.group(0))
    result = result.replace("<title>", "")
    return result