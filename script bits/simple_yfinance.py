import yfinance as yf
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
today_data = yf.download('ADBE', today )

print(today_data)