import requests
import time
import datetime

# Thông tin cần thiết
API_KEY = 'AIzaSyDA5motGcbnGYnBoW_ScExssgCN0bcS1qk'  # Google API Key
CSE_ID = '3624de2b048744afc'  # CSE ID
CHAT_ID = '7338638985'  # Telegram chat ID
BOT_TOKEN = '8189876001:AAETReEzNrBvuOhCVan8oQW-BuGIcUrk91I'  # Telegram Bot Token


# Hàm gửi tin nhắn qua Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
    response = requests.post(url, data=payload)
    print("Status code:", response.status_code)  # In ra mã trạng thái HTTP
    print("Response text:",
          response.text)  # In ra nội dung phản hồi từ Telegram


# Hàm tìm kiếm Google Custom Search
def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"
    response = requests.get(url)
    print("Google Search Response:",
          response.json())  # In ra kết quả trả về từ Google
    return response.json()


# Hàm lọc kết quả tìm kiếm mới trong vòng 15 phút qua
def filter_new_results(results):
    recent_results = []
    current_time = datetime.datetime.now()
    fifteen_minutes_ago = current_time - datetime.timedelta(minutes=15)

    for item in results:
        title = item['title']
        link = item['link']
        snippet = item['snippet']

        print(f"Title: {title}\nSnippet: {snippet}"
              )  # In ra thông tin để kiểm tra

        # Giả sử rằng trong snippet hoặc title có thông tin liên quan đến thời gian, ví dụ:
        # "Vụ cháy xảy ra lúc 10:45 AM" (Đây là một ví dụ, có thể tùy thuộc vào dữ liệu)

        # Tìm kiếm thông tin thời gian trong snippet (Giả sử có format thời gian trong "hh:mm")
        time_found = False
        time_in_snippet = None
        for word in snippet.split():
            if ":" in word and len(word.split(
                    ":")) == 2:  # Kiểm tra nếu từ có định dạng giờ phút
                try:
                    time_in_snippet = datetime.datetime.strptime(word, '%H:%M')
                    time_found = True
                except ValueError:
                    continue

        if time_found and time_in_snippet:
            # Chuyển thời gian trong snippet thành datetime
            time_in_snippet = current_time.replace(
                hour=time_in_snippet.hour,
                minute=time_in_snippet.minute,
                second=0,
                microsecond=0)

            # Kiểm tra nếu thời gian đăng bài trong 15 phút qua
            if time_in_snippet >= fifteen_minutes_ago:
                recent_results.append(
                    f"<b>{title}</b>\n{snippet}\nLink: {link}")

    return recent_results


# Hàm tìm kiếm và gửi tin nhắn nếu có bài mới
def search_and_notify():
    query = "cháy nổ Lào Cai site:facebook.com OR site:tiktok.com"
    search_results = google_search(query)
    items = search_results.get('items', [])

    # Lọc ra kết quả mới nhất trong 15 phút qua
    new_results = filter_new_results(items)

    if new_results:
        message = "\n\n".join(new_results)
        send_telegram_message(message)
        print("✅ Đã gửi tin nhắn với các kết quả tìm thấy.")
    else:
        # Nếu không tìm thấy kết quả nào, gửi tin nhắn báo không có vụ cháy
        send_telegram_message(
            "🚨 Trong 15 phút vừa qua không có vụ cháy nào tại Lào Cai.")
        print("❌ Không tìm thấy kết quả mới.")


# Chạy tìm kiếm và gửi tin nhắn mỗi 15 phút
if __name__ == '__main__':
    while True:
        search_and_notify()
        print("⏱️ Chờ 15 phút trước khi tìm kiếm lại...")
        time.sleep(15 * 60)  # Chờ 15 phút trước khi tìm kiếm lại
