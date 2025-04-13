
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import random
from gtts import gTTS
import os

# مدل پیش‌بینی
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
            return "buy"
        elif rf == lr == svm == gb == 0:
            return "sell"
        else:
            return "hold"

# گرفتن داده واقعی
df = yf.download(tickers="BTC-USD", period="2d", interval="1h")
df["price_change"] = df["Close"].pct_change().fillna(0)
df["volatility"] = df["Close"].rolling(window=5).std().fillna(0)
df["sentiment"] = np.tanh(df["price_change"] * 20)
df["future_price"] = df["Close"].shift(-2)
df["buy_sell_signal"] = (df["future_price"] > df["Close"]).astype(int).fillna(0)

# آموزش مدل و پیش‌بینی
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

# پاسخ احساسی فارسی
def emotional_response(signal):
    if signal == "buy":
        return random.choice([
            "بازار نشون می‌ده وقت خرید رسیده!",
            "سیستم پیشنهاد می‌کنه که وارد پوزیشن خرید بشیم.",
            "فرصت مناسبی برای خرید در حال شکل‌گیریه."
        ])
    elif signal == "sell":
        return random.choice([
            "الان وقت فروشه. بازار در حال نزوله.",
            "سیستم هشدار می‌ده که بهتره بفروشیم.",
            "علائم نشون می‌دن روند نزولی داره شکل می‌گیره."
        ])
    else:
        return random.choice([
            "بازار فعلاً بی‌تصمیمه. بهتره منتظر بمونیم.",
            "سیستم پیشنهاد می‌کنه دست نگه داریم.",
            "فعلاً سیگنال مشخصی وجود نداره."
        ])

message = emotional_response(signal)
print(f"سیگنال: {signal.upper()}\n{message}")

# تولید فایل صوتی با gTTS
tts = gTTS(text=message, lang='fa')
tts.save("signal_voice.mp3")
print("فایل صوتی سیگنال ساخته شد: signal_voice.mp3")
