
import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# مدل پیش‌بینی
class FinalOptimizationExpansionPredictiveSystem:
    def __init__(self):
        self.rf_model = RandomForestClassifier(n_estimators=250)
        self.lr_model = LogisticRegression(max_iter=3500)
        self.svm_model = SVC(kernel='rbf', probability=True)
        self.gb_model = GradientBoostingClassifier(n_estimators=100)
        self.market_data = []
        self.labels = []
        self.multi_stage_predictions = []
        self.model_accuracy = 0

    def process_market_data(self, market_data):
        features = [market_data['sentiment'], market_data['volatility'], market_data['price_change']]
        self.market_data.append(features)
        self.labels.append(market_data['buy_sell_signal'])
        return features

    def train_models(self):
        if len(self.market_data) > 0:
            X = np.array(self.market_data)
            y = np.array(self.labels)
            self.rf_model.fit(X, y)
            self.lr_model.fit(X, y)
            self.svm_model.fit(X, y)
            self.gb_model.fit(X, y)

    def make_predictions(self, market_data):
        features = [market_data['sentiment'], market_data['volatility'], market_data['price_change']]
        rf_prediction = self.rf_model.predict([features])[0]
        lr_prediction = self.lr_model.predict([features])[0]
        svm_prediction = self.svm_model.predict([features])[0]
        gb_prediction = self.gb_model.predict([features])[0]

        combined_prediction = "hold"
        if rf_prediction == 1 and lr_prediction == 1 and svm_prediction == 1 and gb_prediction == 1:
            combined_prediction = "buy"
        elif rf_prediction == 0 and lr_prediction == 0 and svm_prediction == 0 and gb_prediction == 0:
            combined_prediction = "sell"
        return combined_prediction

# اتصال به متاتریدر
if not mt5.initialize():
    print("خطا در اتصال به متاتریدر")
    quit()

symbol = "XAUUSD"
rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 100)
df = pd.DataFrame(rates)
df['time'] = pd.to_datetime(df['time'], unit='s')

# محاسبه ویژگی‌ها برای پیش‌بینی
last_price = df['close'].iloc[-1]
price_change = (df['close'].iloc[-1] - df['close'].iloc[-2]) / df['close'].iloc[-2]
volatility = df['close'].rolling(5).std().iloc[-1]
sentiment = np.tanh(price_change * 20)  # تقریب از احساسات بازار

# آماده‌سازی داده برای مدل
market_data = {
    "sentiment": sentiment,
    "volatility": volatility,
    "price_change": price_change
}

# اجرای مدل و دریافت سیگنال
model = FinalOptimizationExpansionPredictiveSystem()
# آموزش اولیه با داده ساختگی
training_data = [
    {'sentiment': 0.6, 'volatility': 0.01, 'price_change': 0.04, 'buy_sell_signal': 1},
    {'sentiment': -0.5, 'volatility': 0.02, 'price_change': -0.03, 'buy_sell_signal': 0},
    {'sentiment': 0.4, 'volatility': 0.015, 'price_change': 0.02, 'buy_sell_signal': 1},
    {'sentiment': -0.7, 'volatility': 0.03, 'price_change': -0.05, 'buy_sell_signal': 0}
]
for d in training_data:
    model.process_market_data(d)
model.train_models()

signal = model.make_predictions(market_data)
print(f"سیگنال سیستم: {signal}")

# ارسال سفارش
if signal == "buy":
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.1,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(symbol).ask,
        "deviation": 10,
        "magic": 123456,
        "comment": "AI_Buy_Signal",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    mt5.order_send(request)

elif signal == "sell":
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": 0.1,
        "type": mt5.ORDER_TYPE_SELL,
        "price": mt5.symbol_info_tick(symbol).bid,
        "deviation": 10,
        "magic": 123456,
        "comment": "AI_Sell_Signal",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    mt5.order_send(request)

mt5.shutdown()
