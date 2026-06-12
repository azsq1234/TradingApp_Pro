import requests
import pandas as pd

def get_live_data(symbol="BTCUSDT", interval="5m", limit=300):
    """جلب بيانات الأسعار الحية وتحويلها إلى DataFrame"""
    url = f"https://api.binance.com/api/v3/klines"
    params = {'symbol': symbol, 'interval': interval, 'limit': limit}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # تحويل البيانات إلى جدول
    df = pd.DataFrame(data, columns=['t', 'o', 'h', 'l', 'close', 'v', 'ct', 'qv', 'nt', 'tb', 'tq', 'ignore'])
    df['close'] = df['close'].astype(float)
    return df['close']