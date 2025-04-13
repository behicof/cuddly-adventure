
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# تعریف مدل
class FinalOptimizationExpansionPredictiveSystem:
    def __init__(self):
        self.rf_model = RandomForestClassifier(n_estimators=250)
        self.lr_model = LogisticRegression(max_iter=3500)
        self.svm_model = SVC(kernel='rbf', probability=True)
        self.gb_model = GradientBoostingClassifier(n_estimators=100)
        self.market_data = []
        self.labels = []

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

        if rf_prediction == 1 and lr_prediction == 1 and svm_prediction == 1 and gb_prediction == 1:
            return "buy"
        elif rf_prediction == 0 and lr_prediction == 0 and svm_prediction == 0 and gb_prediction == 0:
            return "sell"
        else:
            return "hold"

# دریافت داده از Yahoo Finance (نماد طلا یا بیت‌کوین)
symbol = "BTC-USD"  # یا "XAUUSD=X" برای طلا
df = yf.download(tickers=symbol, period="2d", interval="1h")

# محاسبه ویژگی‌ها
df["price_change"] = df["Close"].pct_change().fillna(0)
df["volatility"] = df["Close"].rolling(window=5).std().fillna(0)
df["sentiment"] = np.tanh(df["price_change"] * 20)
df["future_price"] = df["Close"].shift(-2)
df["buy_sell_signal"] = (df["future_price"] > df["Close"]).astype(int).fillna(0)

# آموزش مدل و پیش‌بینی برای آخرین نقطه
model = FinalOptimizationExpansionPredictiveSystem()
for i, row in df.iterrows():
    model.process_market_data({
        "sentiment": row["sentiment"],
        "volatility": row["volatility"],
        "price_change": row["price_change"],
        "buy_sell_signal": row["buy_sell_signal"]
    })
model.train_models()

latest = df.iloc[-1]
signal = model.make_predictions({
    "sentiment": latest["sentiment"],
    "volatility": latest["volatility"],
    "price_change": latest["price_change"]
})

print(f"سیگنال پیش‌بینی‌شده برای {symbol}: {signal}")
