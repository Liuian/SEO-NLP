import requests
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BertForTokenClassification
import torch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 爬取文章內容
def scrape_article_content(url):
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # 根據具體的網頁結構，提取出文章的內容，可能需要進一步的解析
    article_content = soup.find('div', class_='container-component').get_text()  # 假設文章內容在 <div class="article-content"> 中
    return article_content
'''
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 使用無頭模式，不需要打開瀏覽器
    driver = webdriver.Chrome(options=chrome_options)  # 使用 Chrome 瀏覽器
    driver.get(url)  # 前往指定的 URL
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')  # 使用 BeautifulSoup 解析網頁
    article_content = page_soup.find('div', class_='article-content').get_text()  # 提取文章內容
    driver.quit()  # 關閉瀏覽器
    return article_content

# 文本預處理
def preprocess_text(text):
    # 進行文本清理操作，例如去除 HTML 標記、特殊字符等

    return cleaned_text

# 使用 BERT 模型進行 NER
def perform_ner(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    model = BertForTokenClassification.from_pretrained('bert-base-chinese', num_labels=5)  # 假設有5種命名實體類別
    input_ids = tokenizer.encode(text, add_special_tokens=True)
    with torch.no_grad():
        outputs = model(torch.tensor([input_ids]))
    predictions = torch.argmax(outputs[0], axis=-1).squeeze().tolist()
    return predictions

# 獲取並顯示實體
def extract_entities(text, predictions):
    entities = []
    current_entity = ''
    for i, token in enumerate(text.split()):
        if predictions[i] != 0:  # 假設命名實體類別0表示普通詞
            current_entity += ' ' + token
        else:
            if current_entity:
                entities.append(current_entity.strip())
                current_entity = ''
    return entities

# 主程序
def main():
    url = 'https://www.mbishop.com.tw/Article/Detail/79781'  #文章的網址
    article_content = scrape_article_content(url)
    cleaned_text = preprocess_text(article_content)
    predictions = perform_ner(cleaned_text)
    entities = extract_entities(cleaned_text, predictions)
    print("Entities found in the article:")
    for entity in entities:
        print(entity)

if __name__ == "__main__":
    main()
