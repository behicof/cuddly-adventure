
import requests

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

# اجرای ارسال‌ها
send_text_message(TEXT_MESSAGE)
send_voice_message(AUDIO_FILE_PATH)
