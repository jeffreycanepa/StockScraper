'''Script for trying out new things'''
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from datetime import datetime, timedelta

# Date must be in the fromat ("%Y-%m-%d") That is, year-month-day
now = datetime.now()
start_date = (now - timedelta(days=356)).strftime('%Y-%m-%d')
end_date = now.strftime('%Y-%m-%d')

# Get Stock Data
aapl = yf.download(tickers = "AAPL",
                  start = start_date,
                  end = end_date)
aapl.name = 'Apple Computer'
adbe = yf.download(tickers = "ADBE",
                  start = start_date,
                  end = end_date)
adbe.name = 'Adobe Systems'
csco = yf.download(tickers = "CSCO",
                  start = start_date,
                  end = end_date)
csco.name = 'Cisco'
ntap = yf.download(tickers = "NTAP",
                  start = start_date,
                  end = end_date)
ntap.name = 'NetApp'
amzn = yf.download(tickers = "AMZN",
                  start = start_date,
                  end = end_date)
amzn.name = 'Amazon'
msft = yf.download(tickers = "MSFT",
                  start = start_date,
                  end = end_date)
msft.name = 'Microsoft'
tsla = yf.download(tickers = "TSLA",
                  start = start_date,
                  end = end_date)
tsla.name = 'Tesla'
vmw = yf.download(tickers = "VMW",
                  start = start_date,
                  end = end_date)
vmw.name = 'VMWare'
docu = yf.download(tickers = "DOCU",
                  start = start_date,
                  end = end_date)
docu.name = 'DocuSign'
splk = yf.download(tickers = "SPLK",
                  start = start_date,
                  end = end_date)
splk.name = 'Splunk'
ge = yf.download(tickers = "GE",
                  start = start_date,
                  end = end_date)
ge.name = 'General Electric'
xlu = yf.download(tickers = "XLU",
                  start = start_date,
                  end = end_date)
xlu.name = 'Utilities Select Sector'


# Plot everything by leveraging the very powerful matplotlib package
# hist['Close'].plot(figsize=(16, 9))
plt.figure(figsize=(16, 9))
sns.set_style('ticks')
company = [aapl, adbe, csco, ntap, amzn, msft, vmw, tsla, docu, splk, ge, xlu]
colorr = ['blue', 'red', 'black', 'yellow', 'orange', 'green', 'navy', 'hotpink', 'lightsteelblue', 'mediumspringgreen', 'grey', 'sandybrown']
for cmp, clr in zip(company,colorr):
    sns.lineplot(data=cmp,x="Date",y="Close",color=clr,linewidth=2.5, label=cmp.name)
# sns.lineplot(data=aapl, x='Date', y='Close', color='blue')
sns.despine()
plt.title('Closing Prices (1 year)', size='x-large', color='black')
plt.ylabel('Stock Price $')
plt.show()