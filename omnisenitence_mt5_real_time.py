
import MetaTrader5 as mt5
from OmniSentience_v1_2 import OmniSentienceV1_2

# اطلاعات حساب MetaTrader 5
MT5_ACCOUNT = 12345678
MT5_PASSWORD = "your_password"
MT5_SERVER = "your_broker_server"
symbol = "BTCUSD"  # نماد معاملاتی (یا نماد دیگر مانند XAUUSD)

# اتصال به MetaTrader 5
mt5.initialize(login=MT5_ACCOUNT, password=MT5_PASSWORD, server=MT5_SERVER)

# بررسی اتصال
if not mt5.initialize():
    print("خطا در اتصال به MetaTrader 5")
    quit()

# دریافت داده از MetaTrader 5
def get_mt5_data(symbol="BTCUSD", timeframe=mt5.TIMEFRAME_M1, bars=100):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, bars)
    return rates

# دریافت داده از MetaTrader 5
data = get_mt5_data(symbol=symbol, timeframe=mt5.TIMEFRAME_M1, bars=100)

# تبدیل داده‌ها به DataFrame
import pandas as pd
df = pd.DataFrame(data)
df['time'] = pd.to_datetime(df['time'], unit='s')

# دریافت پیش‌بینی سیگنال از OmniSentience
agent = OmniSentienceV1_2(balance=10000)
signal_response = agent.process_market(df, expected_profit=25)

# ارسال سفارش بر اساس سیگنال
def send_order(signal):
    if signal['signal'] == 'buy':
        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 0.01,  # حجم خرید (بر اساس موجودی)
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(symbol).ask,
            "deviation": 10,
            "magic": 123456,
            "comment": "OmniSentience Buy Order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(order)
        print(f"سفارش خرید ارسال شد: {result}")
    elif signal['signal'] == 'sell':
        order = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": 0.01,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(symbol).bid,
            "deviation": 10,
            "magic": 123456,
            "comment": "OmniSentience Sell Order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(order)
        print(f"سفارش فروش ارسال شد: {result}")

# ارسال سفارش با توجه به سیگنال
send_order(signal_response)
