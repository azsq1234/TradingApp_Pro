from data.fetcher import get_live_data
from engine.indicators import calculate_rsi, calculate_ema

def run_system():
    # 1. جلب البيانات
    prices = get_live_data()
    
    # 2. حساب المؤشرات
    rsi = calculate_rsi(prices).iloc[-1]
    ema = calculate_ema(prices).iloc[-1]
    current_price = prices.iloc[-1]
    
    print(f"Price: {current_price} | RSI: {rsi:.2f} | EMA200: {ema:.2f}")
    
    # 3. اتخاذ القرار (هنا نضع استراتيجيتك)
    if rsi < 30 and current_price > ema:
        print("SIGNAL: BUY OPPORTUNITY")
    else:
        print("SIGNAL: WAIT")

if __name__ == "__main__":
    run_system()