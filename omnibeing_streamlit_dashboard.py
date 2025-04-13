
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

st.set_page_config(layout="wide")
st.title("داشبورد پیش‌بینی بازار | OmniBeing")

symbol = st.sidebar.selectbox("انتخاب نماد", ["BTC-USD", "XAUUSD=X", "ETH-USD"])
interval = st.sidebar.selectbox("تایم‌فریم", ["1h", "30m", "15m", "5m"])
period = st.sidebar.selectbox("بازه زمانی", ["1d", "2d", "5d", "7d"])

# دریافت داده از یاهو فاینانس
df = yf.download(tickers=symbol, interval=interval, period=period)
df["price_change"] = df["Close"].pct_change().fillna(0)
df["volatility"] = df["Close"].rolling(window=5).std().fillna(0)
df["sentiment"] = np.tanh(df["price_change"] * 20)
df["future_price"] = df["Close"].shift(-2)
df["buy_sell_signal"] = (df["future_price"] > df["Close"]).astype(int).fillna(0)

# مدل
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

    def train_models(self):
        X = np.array(self.market_data)
        y = np.array(self.labels)
        self.rf_model.fit(X, y)
        self.lr_model.fit(X, y)
        self.svm_model.fit(X, y)
        self.gb_model.fit(X, y)

    def make_predictions(self, market_data):
        features = [market_data['sentiment'], market_data['volatility'], market_data['price_change']]
        rf = self.rf_model.predict([features])[0]
        lr = self.lr_model.predict([features])[0]
        svm = self.svm_model.predict([features])[0]
        gb = self.gb_model.predict([features])[0]
        if rf == lr == svm == gb == 1:
            return "خرید"
        elif rf == lr == svm == gb == 0:
            return "فروش"
        else:
            return "نگه‌دار"

# آموزش و پیش‌بینی
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

st.subheader(f"سیگنال نهایی مدل برای {symbol}:")
st.success(f"→ {signal}")

st.line_chart(df["Close"], use_container_width=True)
