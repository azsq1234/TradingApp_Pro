import yfinance as yf

def get_live_data(symbol="BTC-USD", period="1mo", interval="1d"):
    """
    الرموز المقترحة:
    - البيتكوين: BTC-USD
    - الذهب: GC=F
    - الفضة: SI=F
    - أسهم أبل: AAPL
    - عملات (يورو/دولار): EURUSD=X
    """
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        if not df.empty:
            return df['Close'] # يعيد سلسلة أسعار الإغلاق
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None