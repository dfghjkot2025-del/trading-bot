import os
import time
import requests
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# 1. 🌐 سيرفر ويب مدمج لإرضاء منصة Render ومنع علامة الـ X الحمراء
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Trading Bot is Active and Live!")

def run_render_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_render_server, daemon=True).start()

# 2. ⚙️ جلب متغيرات البيئة من لوحة تحكم Render
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("تنبيه: التوكن أو الآيدي غير متوفرين في الإعدادات!")
        return
    
    # صياغة الرابط البرمجي الصحيح 100% لمنع الالتصاق والخطأ
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram response: {response.status_code}")
    except Exception as e:
        print(f"Error sending message: {e}")

# 3. 📊 رادار الفحص اللحظي فائق الحساسية للأسعار
def trading_strategy_loop():
    # رسالة انطلاق ترحيبية فورية تصل لهاتفك بمجرد تشغيل السيرفر
    send_telegram_message("🔔 **تم تشغيل رادار الفحص اللحظي بنجاح!**\nبدأ البوت بمراقبة الأسعار الحية وضخ الصفقات فوراً...")
    
    previous_price = None
    
    while True:
        try:
            # جلب السعر الحي للبيتكوين من منصة Binance العالمية
            api_url = "https://binance.com"
            response = requests.get(api_url).json()
            current_price = float(response['price'])
            print(f"Checking Price: {current_price}")
            
            if previous_price is not None and current_price != previous_price:
                # إشارة صعود لحظية
                if current_price > previous_price:
                    msg = f"📈 **إشارة شراء لحظية**\n• الزوج: BTC/USDT\n• السعر الحركي: ${current_price:,}"
                    send_telegram_message(msg)
                # إشارة هبوط لحظية
                elif current_price < previous_price:
                    msg = f"📉 **إشارة بيع لحظية**\n• الزوج: BTC/USDT\n• السعر الحركي: ${current_price:,}"
                    send_telegram_message(msg)
            
            previous_price = current_price
                    
        except Exception as e:
            print(f"Error in trading loop: {e}")
            
        time.sleep(10) # فحص وتحليل كل 10 ثوانٍ

# إطلاق عقل البوت
trading_strategy_loop()
