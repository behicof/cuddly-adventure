
import requests
from OmniSentience_v1_2 import OmniSentienceV1_2

# تنظیمات ربات تلگرام
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
TEXT_MESSAGE = "سیگنال امروز: خرید! بازار داره بالا می‌ره."
AUDIO_FILE_PATH = "signal_voice.mp3"  # فایل صوتی تولیدشده توسط gTTS

# ارسال پیام متنی
def send_text_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text
    }
    response = requests.post(url, data=data)
    print("پیام متنی ارسال شد:", response.status_code)

# ارسال فایل صوتی
def send_voice_message(file_path):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendAudio"
    with open(file_path, 'rb') as audio:
        files = {'audio': audio}
        data = {"chat_id": CHAT_ID}
        response = requests.post(url, files=files, data=data)
        print("فایل صوتی ارسال شد:", response.status_code)

# دریافت سیگنال از OmniSentience
agent = OmniSentienceV1_2(balance=10000)
live_data = agent.get_live_data(symbol="BTC-USD", interval="15m", period="2d")
signal_response = agent.process_market(live_data, expected_profit=30)

# ارسال سیگنال و فایل صوتی به تلگرام
send_text_message(f"سیگنال پیش‌بینی‌شده: {signal_response['signal']}")
send_voice_message(AUDIO_FILE_PATH)
