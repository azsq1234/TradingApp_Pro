import requests
import pandas as pd

def get_live_data(symbol="bitcoin", vs_currency="usd", days=1):
    # ملاحظة: CoinGecko يستخدم أسماء العملات (bitcoin وليس BTCUSDT)
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {'vs_currency': vs_currency, 'days': days, 'interval': 'hourly'}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # استخراج الأسعار من هيكلية استجابة CoinGecko
            prices = [item[1] for item in data['prices']]
            return pd.Series(prices, name='close')
        else:
            return None
    except Exception as e:
        print(f"Error fetching from Coingecko: {e}")
        return None