import os
import re
import csv
import requests
from bs4 import BeautifulSoup

# 設定目標網址
base_url = 'https://javtrailers.com'
studio_url_template = f'{base_url}/ja/studios/s1-no-1-style'  # 第一頁不帶 ?page=

# 設定 HTTP 標頭模擬瀏覽器請求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 創建 S1/videos 和 S1/cover 資料夾（如果不存在）
video_dir = 'S1/videos'
cover_dir = 'S1/cover'
os.makedirs(video_dir, exist_ok=True)
os.makedirs(cover_dir, exist_ok=True)

# 提取 M3U8 播放列表和影片標題的函數
def get_m3u8_and_title(video_page_url):
    response = requests.get(video_page_url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    # 查找 M3U8 播放列表 URL
    script_tag = soup.find('script', string=lambda text: 'playlist.m3u8' in text if text else False)
    m3u8_url = None
    if script_tag:
        m3u8_url_start = script_tag.text.find('https://cc3001.dmm.co.jp/hlsvideo/freepv/')
        m3u8_url_end = script_tag.text.find('"', m3u8_url_start)
        m3u8_url = script_tag.text[m3u8_url_start:m3u8_url_end]

    # 提取影片標題
    title_tag = soup.find('h1', class_='lead')
    title = title_tag.get_text(strip=True) if title_tag else "unknown_title"
    title = re.sub(r'[\\/*?:"<>|]', "", title)  # 去除不合法的檔案名字符

    return m3u8_url, title

# 生成封面 URL
def generate_cover_url(part_number):
    return f"https://pics.dmm.co.jp/digital/video/{part_number.lower()}/{part_number.lower()}pl.jpg"

# 調整番號格式
def adjust_part_number(title):
    # 移除特殊符號
    part_number = re.sub(r'[^A-Za-z0-9]', "", title[:8])
    # 在番號中間插入 "00"
    adjusted_number = f"{part_number[:4]}00{part_number[4:]}"
    return adjusted_number

# 寫入 CSV 檔案
csv_filename = 'S1/video_info.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['影片番號', '影片標題', '封面圖片 URL']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 從第1頁到第10頁抓取
    for page in range(1, 11):
        # 設定每頁的 URL
        if page == 1:
            page_url = studio_url_template  # 第一頁不帶 '?page='
        else:
            page_url = f'{studio_url_template}?page={page}'

        print(f"正在抓取頁面：{page_url}")

        # 發送 GET 請求到每頁
        response = requests.get(page_url, headers=headers)
        response.raise_for_status()  # 確保請求成功

        # 使用 BeautifulSoup 解析頁面內容
        soup = BeautifulSoup(response.content, 'html.parser')

        # 找到所有包含 "video" 的連結
        video_links = [a['href'] for a in soup.find_all('a', href=True) if 'video' in a['href']]

        # 迭代所有 video 連結，提取 M3U8 播放列表 URL 和影片標題
        for link in video_links:
            video_page_url = f'{base_url}{link}'
            m3u8_url, title = get_m3u8_and_title(video_page_url)

            if m3u8_url:
                print(f"影片頁面 URL: {video_page_url}")
                print(f"找到 M3U8 播放列表 URL: {m3u8_url}")
                print(f"影片標題: {title}")

                # 調整番號格式
                part_number = adjust_part_number(title)

                # 生成封面圖片 URL
                cover_url = generate_cover_url(part_number)

                # 將影片番號、標題和封面圖片 URL 寫入 CSV 檔案
                writer.writerow({
                    '影片番號': part_number,
                    '影片標題': title,
                    '封面圖片 URL': cover_url
                })

                # 使用 ffmpeg 下載影片
                video_filename = os.path.join(video_dir, f"{title}.mp4")
                ffmpeg_command = f'ffmpeg -i "{m3u8_url}" -c copy "{video_filename}" -loglevel error -y'
                print(f"執行命令: {ffmpeg_command}")
                os.system(ffmpeg_command)
                print(f"影片已下載並保存為 {video_filename}")

                # 下載封面圖片
                try:
                    img_response = requests.get(cover_url, headers=headers)
                    img_response.raise_for_status()
                    cover_filename = os.path.join(cover_dir, f"{part_number}_cover.jpg")
                    with open(cover_filename, 'wb') as img_file:
                        img_file.write(img_response.content)
                    print(f"封面圖片已下載並保存為 {cover_filename}")
                except requests.exceptions.RequestException as e:
                    print(f"下載圖片失敗 {cover_url}: {e}")

print(f"所有影片資訊已儲存到 '{csv_filename}' 檔案中。")
