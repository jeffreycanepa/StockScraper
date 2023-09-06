import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import yfinance
from datetime import datetime, date, timedelta

start = date(2022,8,5)
end = date(2023,8,4)

stockTickers = ['AAPL', 'ADBE','CSCO', 'NTAP']
cn = ["Apple", "Adobe", "Cisco", "NetApp"]
stockData = []

for company in stockTickers:
    cmp = yfinance.download(company, start=start, end=end)
    newcmp = cmp.reset_index()
    stockData.append(newcmp)

now = datetime.now()
then = now + timedelta(days=len(stockData[0]))
days = mdates.drange(now,then,timedelta(days=1))

mylines = []
fig, ax = plt.subplots(figsize=(12,7))
ax.set_title('My Stocks for past year')

x = 0
while x <= len(stockData)-1:
    line, = ax.plot(days, stockData[x]['Adj Close'], label=cn[x])
    mylines.append(line,)
    x += 1

ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%y'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=20))
ax.tick_params(axis='x', labelrotation=45)

leg = ax.legend(fancybox=True, shadow=True)
lines = [mylines[0], mylines[1], mylines[2], mylines[3]]
print(lines[0])

lined = {}  # Will map legend lines to original lines.
for legline, origline in zip(leg.get_lines(), mylines):
    legline.set_picker(True)  # Enable picking on the legend line.
    legline.set_picker(5)
    lined[legline] = origline


def on_pick(event):
    # On the pick event, find the original line corresponding to the legend
    # proxy line, and toggle its visibility.
    legline = event.artist
    origline = lined[legline]
    visible = not origline.get_visible()
    origline.set_visible(visible)
    # Change the alpha on the line in the legend, so we can see what lines
    # have been toggled.
    legline.set_alpha(1.0 if visible else 0.2)
    fig.canvas.draw()

fig.canvas.mpl_connect('pick_event', on_pick)
plt.show()