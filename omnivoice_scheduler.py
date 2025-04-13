
import time
import subprocess

# مسیر فایل‌هایی که باید به صورت خودکار اجرا بشن
VOICE_GENERATOR_PATH = "omnivoice_farsi_tts.py"
TELEGRAM_SENDER_PATH = "omnivoice_telegram_sender.py"

# زمان بین اجراها (مثلاً 1 ساعت = 3600 ثانیه)
INTERVAL_SECONDS = 3600  # یا 1800 برای نیم ساعت

print("OmniVoice Self-Scheduler فعال شد.")

while True:
    print("در حال اجرای سیستم تحلیل و تولید صدا...")
    subprocess.run(["python", VOICE_GENERATOR_PATH])
    
    print("در حال ارسال پیام به تلگرام...")
    subprocess.run(["python", TELEGRAM_SENDER_PATH])
    
    print(f"در حال انتظار برای {INTERVAL_SECONDS // 60} دقیقه بعدی...")
    time.sleep(INTERVAL_SECONDS)
