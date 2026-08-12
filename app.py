import os
import time
import threading
import requests
import pandas as pd
import yfinance as yf
from flask import Flask

# إنشاء خادم ويب وهمي لإرضاء منصة Render المجانية
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل الآن بنجاح ومستيقظ!"

def run_web_server():
    # تشغيل الخادم على المنفذ المخصص من Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# إعدادات البوت والقناة من متغيرات البيئة السرية في Render
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

ASSETS = {
    "GC=F": "الذهب (Gold)",
    "EURUSD=X": "اليورو مقابل الدولار (EUR/USD)",
    "GBPUSD=X": "الباوند مقابل الدولار (GBP/USD)",
    "USDJPY=X": "الدولار مقابل الين (USD/JPY)"
}

def send_telegram_message(message):
    url = f"https://telegram.org{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try: requests.post(url, json=payload)
    except Exception as e: print(f"خطأ إرسال: {e}")

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def check_signals_loop():
    print("بدء مراقبة الأسواق في الخلفية...")
    while True:
        for ticker, name in ASSETS.items():
            try:
                df = yf.download(tickers=ticker, period="5d", interval="1h", progress=False)
                if df.empty: continue
                df['RSI'] = calculate_rsi(df)
                
                current_price = round(df['Close'].iloc[-1], 2)
                current_rsi = round(df['RSI'].iloc[-1], 2)
                
                recommendation = None
                if current_rsi < 30:
                    recommendation = "🟢 **توصية شـراء (BUY)** 🟢"
                elif current_rsi > 70:
                    recommendation = "🔴 **توصية بـيـع (SELL)** 🔴"
                    
                if recommendation:
                    msg = f"{recommendation}\n\n📊 **الأصل**: {name}\n💵 **السعر**: {current_price}\n📈 RSI = {current_rsi}"
                    send_telegram_message(msg)
            except Exception as e:
                print(f"خطأ في {name}: {e}")
        time.sleep(900) # فحص كل 15 دقيقة

if __name__ == "__main__":
    # تشغيل فحص التوصيات في الخلفية واصل دون انقطاع
    t = threading.Thread(target=check_signals_loop)
    t.daemon = True
    t.start()
    
    # تشغيل خادم الويب الرئيسي لـ Render
    run_web_server()
