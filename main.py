import os
import time
import threading
import requests
from flask import Flask

# Thông tin cần thiết
API_KEY = 'AIzaSyDA5motGcbnGYnBoW_ScExssgCN0bcS1qk'  # Google API Key
CSE_ID = '3624de2b048744afc'  # CSE ID
CHAT_ID = '7338638985'  # Telegram chat ID
BOT_TOKEN = '8189876001:AAETReEzNrBvuOhCVan8oQW-BuGIcUrk91I'  # Telegram Bot Token

# Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# Gửi tin nhắn qua Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    print("Status code:", response.status_code)
    print("Response text:", response.text)

# Gọi Google Custom Search
def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"
    response = requests.get(url)
    print("Google Search Response:", response.json())
    return response.json()

# Lọc kết quả mới nhất
def filter_new_results(results):
    recent_results = []
    for item in results:
        title = item['title']
        link = item['link']
        snippet = item['snippet']
        if 'cháy' in snippet or 'nổ' in snippet or 'Lào Cai' in snippet:
            recent_results.append(f"<b>{title}</b>\n{snippet}\nLink: {link}")
    return recent_results

# Hàm chính để tìm kiếm và gửi tin
def search_and_notify():
    query = "cháy nổ Lào Cai site:facebook.com OR site:tiktok.com"
    search_results = google_search(query)
    items = search_results.get('items', [])
    new_results = filter_new_results(items)
    if new_results:
        message = "\n\n".join(new_results)
        send_telegram_message(message)
        print("✅ Đã gửi tin nhắn với các kết quả tìm thấy.")
    else:
        send_telegram_message("🚨 Trong 15 phút vừa qua không có vụ cháy nào tại Lào Cai.")
        print("❌ Không tìm thấy kết quả mới.")

# Bot chạy lặp lại mỗi 15 phút
def run_bot_loop():
    while True:
        search_and_notify()
        print("⏱️ Chờ 15 phút trước khi tìm kiếm lại...")
        time.sleep(15 * 60)

# Chạy cả bot + Flask khi khởi động
if __name__ == '__main__':
    # Thread riêng để chạy bot
    threading.Thread(target=run_bot_loop).start()

    # Lấy PORT từ biến môi trường của Render (hoặc dùng 10000 mặc định)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
