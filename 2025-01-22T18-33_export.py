
import MetaTrader5 as mt5
import pandas as pd
import time

# اتصال به متاتریدر 5
def connect_to_mt5():
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialization failed: {mt5.last_error()}")
    print("Connected to MetaTrader 5")

# دریافت داده زنده بازار (مثال: XAUUSD - طلا)
def get_latest_market_data(symbol="XAUUSD", timeframe=mt5.TIMEFRAME_M1, num_candles=1):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, num_candles)
    if rates is None or len(rates) == 0:
        raise ValueError("No data retrieved from MT5")
    df = pd.DataFrame(rates)
    return df

# جدا کردن ویژگی‌های مورد نیاز برای مدل
def extract_features_from_candle(candle):
    price_change = (candle['close'] - candle['open']) / candle['open']
    volatility = (candle['high'] - candle['low']) / candle['open']
    sentiment = 1 if candle['close'] > candle['open'] else -1
    return {
        "sentiment": sentiment,
        "volatility": volatility,
        "price_change": price_change
    }

# بستن اتصال
def shutdown_mt5():
    mt5.shutdown()
