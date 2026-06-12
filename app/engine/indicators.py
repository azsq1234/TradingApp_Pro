import pandas as pd

def calculate_rsi(data, period=14):
    """حساب مؤشر القوة النسبية - RSI"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_ema(data, period=200):
    """حساب المتوسط المتحرك الأسي - EMA"""
    return data.ewm(span=period, adjust=False).mean()