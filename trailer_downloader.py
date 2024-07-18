import os
import re
import requests
from bs4 import BeautifulSoup

# 設定目標網址
base_url = 'https://javtrailers.com'
home_url = f'{base_url}/'

# 設定 HTTP 標頭模擬瀏覽器請求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 發送 GET 請求到首頁
response = requests.get(home_url, headers=headers)
response.raise_for_status()  # 確保請求成功

# 使用 BeautifulSoup 解析首頁內容
soup = BeautifulSoup(response.content, 'html.parser')

# 找到所有包含 "video" 的連結
video_links = [a['href'] for a in soup.find_all('a', href=True) if 'video' in a['href']]

# 設定 M3U8 播放列表的查找和提取函數
def get_m3u8_and_title(video_page_url):
    response = requests.get(video_page_url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', string=lambda text: 'playlist.m3u8' in text if text else False)
    
    m3u8_url = None
    if script_tag:
        m3u8_url_start = script_tag.text.find('https://cc3001.dmm.co.jp/hlsvideo/freepv/')
        m3u8_url_end = script_tag.text.find('"', m3u8_url_start)
        m3u8_url = script_tag.text[m3u8_url_start:m3u8_url_end]
    
    title_tag = soup.find('h1', class_='lead')
    title = title_tag.get_text(strip=True) if title_tag else "unknown_title"
    title = re.sub(r'[\\/*?:"<>|]', "", title)  # 去除不合法的文件名字符

    return m3u8_url, title

# 創建 output 文件夾（如果不存在）
os.makedirs('output', exist_ok=True)

# 打開文件以便寫入
with open('m3u8_urls.txt', 'w') as file:
    # 迭代所有 video 連結，提取 M3U8 播放列表 URL 和標題
    for link in video_links:
        video_page_url = f'{base_url}{link}'
        m3u8_url, title = get_m3u8_and_title(video_page_url)
        if m3u8_url:
            print(f"影片頁面 URL: {video_page_url}")
            print(f"找到 M3U8 播放列表 URL: {m3u8_url}")
            print(f"影片標題: {title}")
            # 將找到的 M3U8 URL 和標題寫入文件
            file.write(f"{video_page_url}\n{m3u8_url}\n{title}\n\n")
            
            # 使用 ffmpeg 下載影片
            video_filename = os.path.join('output', f"{title}.mp4")
            ffmpeg_command = f'ffmpeg -i "{m3u8_url}" -c copy "{video_filename}"'
            os.system(ffmpeg_command)
            print(f"影片已下載並儲存為 {video_filename}")
        else:
            print(f"未找到 M3U8 播放列表 URL: {video_page_url}")

print("所有 M3U8 URL 和標題已存儲到 'm3u8_urls.txt' 文件中。")