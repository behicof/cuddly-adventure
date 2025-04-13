
from binance.client import Client
from binance.enums import *
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import time

# اطلاعات API (جایگزین کن)
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_SECRET_KEY"

# اتصال به Binance
client = Client(API_KEY, API_SECRET)

symbol = "BTCUSDT"

# دریافت داده کندل (آخرین 100 کندل 15 دقیقه‌ای)
klines = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE, limit=100)
df = pd.DataFrame(klines, columns=["timestamp", "o", "h", "l", "c", "v", "_", "_", "_", "_", "_", "_"])
df["Close"] = df["c"].astype(float)
df["price_change"] = df["Close"].pct_change().fillna(0)
df["volatility"] = df["Close"].rolling(5).std().fillna(0)
df["sentiment"] = np.tanh(df["price_change"] * 20)
df["future_price"] = df["Close"].shift(-2)
df["buy_sell_signal"] = (df["future_price"] > df["Close"]).astype(int).fillna(0)

# مدل هوشمند
class FinalOptimizationExpansionPredictiveSystem:
    def __init__(self):
        self.rf = RandomForestClassifier(n_estimators=200)
        self.lr = LogisticRegression(max_iter=3000)
        self.svm = SVC(kernel="rbf", probability=True)
        self.gb = GradientBoostingClassifier(n_estimators=100)
        self.X = []
        self.y = []

    def process(self, row):
        self.X.append([row["sentiment"], row["volatility"], row["price_change"]])
        self.y.append(row["buy_sell_signal"])

    def train(self):
        X = np.array(self.X)
        y = np.array(self.y)
        self.rf.fit(X, y)
        self.lr.fit(X, y)
        self.svm.fit(X, y)
        self.gb.fit(X, y)

    def predict(self, row):
        features = [row["sentiment"], row["volatility"], row["price_change"]]
        if all(model.predict([features])[0] == 1 for model in [self.rf, self.lr, self.svm, self.gb]):
            return "buy"
        elif all(model.predict([features])[0] == 0 for model in [self.rf, self.lr, self.svm, self.gb]):
            return "sell"
        else:
            return "hold"

# اجرای مدل و تصمیم‌گیری
model = FinalOptimizationExpansionPredictiveSystem()
for i, row in df.iterrows():
    model.process(row)
model.train()

latest = df.iloc[-1]
signal = model.predict(latest)
print(f"سیگنال نهایی: {signal}")

# اجرای سفارش آزمایشی (تغییر به real در صورت نیاز)
if signal in ["buy", "sell"]:
    side = SIDE_BUY if signal == "buy" else SIDE_SELL
    order = client.create_test_order(
        symbol=symbol,
        side=side,
        type=ORDER_TYPE_MARKET,
        quantity=0.001  # مقدار بیت‌کوین فرضی برای تست
    )
    print("سفارش تست ارسال شد:", order)
else:
    print("هیچ سفارشی ارسال نشد.")
