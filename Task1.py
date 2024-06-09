# Task1: 請爬取google第一到第三頁關於心理諮商的標題/meta/內容


# 遇到chrome is being controlled by automated test software
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import pandas as pd

def save_to_csv(results):
    # 將結果保存到 CSV 文件
    df = pd.DataFrame(results)
    df.to_csv('google_results.csv', index=False, encoding='utf-8-sig')

def get_google_results(query, pages=3):
    # 創建 Chrome Options 對象，禁用提示
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    # 使用 Chrome Options 創建 WebDriver 對象
    driver = webdriver.Chrome(options=chrome_options)

    results = []

    for page in range(pages):
        start = page * 10
        url = f"https://www.google.com/search?q={query}&start={start}"
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 查找所有搜索結果
        for result in soup.find_all('div', class_='g'):
            title_element = result.find('h3')
            meta_element = result.find('span', class_='st')
            link_element = result.find('a')

            if title_element and link_element:
                title = title_element.get_text()
                meta = meta_element.get_text() if meta_element else ''
                link = link_element['href']

                try:
                    # 訪問鏈接，提取頁面內容
                    driver.get(link)
                    time.sleep(2)
                    page_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    content = page_soup.get_text()

                    # 將結果添加到列表
                    results.append({
                        'title': title,
                        'meta': meta,
                        'content': content[:500]  # 只保存前500個字符
                    })

                    driver.back()
                    time.sleep(2)
                except Exception as e:
                    print(f"Failed to access {link}: {e}")
                    driver.back()
                    time.sleep(2)

    driver.quit()
    return results

# 設定查詢關鍵字和頁數
query = '心理諮商'
results = get_google_results(query, pages=3)

# 保存結果到 CSV 文件
save_to_csv(results)
