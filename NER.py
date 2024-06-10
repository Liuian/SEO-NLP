import requests
from bs4 import BeautifulSoup
from transformers import BertTokenizer, BertForTokenClassification
import torch
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_text_in_div(soup):
    # 初始化文本内容为空字符串
    text_content = ""

    # 遍历所有子标签
    for child in soup.children:
        # 如果子标签是字符串类型，则将其文本内容添加到总文本内容中
        if isinstance(child, str):
            text_content += child.strip() + " "  # 去除多余的空白字符
        # 如果子标签是标签类型，则递归调用函数继续遍历其子标签
        elif child.name == 'p':
            text_content += child.text.strip() + " "  # 去除多余的空白字符
        elif child.name == 'span':
            text_content += child.text.strip() + " "  # 去除多余的空白字符
        else:
            text_content += find_text_in_div(child)

    return text_content

# 爬取文章内容
def scrape_article_content(url):
    # 使用 Chrome 驅動
    driver = webdriver.Chrome()
    # 打開網頁
    driver.get(url)
    # 等待直到目標元素可見
    wait = WebDriverWait(driver, 10)
    root_element = wait.until(EC.visibility_of_element_located((By.ID, "root")))
    # 使用 BeautifulSoup 解析頁面
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 關閉瀏覽器
    driver.quit()
    # 提取需要的內容
    content = soup.find('div', id='root')
    # 如果找到了 root_div
    if content:
        # 找到 root_div 中的所有文字内容
        text_content = find_text_in_div(content)
        #print(text_content)
        return text_content
    else:
        print("未找到 id 为 root 的 div 标签")
        return ''

# 文本预处理
def preprocess_text(text):
    # 进行文本清理操作，例如去除 HTML 标记、特殊字符等
    cleaned_text = text.replace('\n', ' ').replace('\r', '').strip()
    return cleaned_text

# 使用 BERT 模型进行 NER
def perform_ner(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
    model = BertForTokenClassification.from_pretrained('bert-base-chinese', num_labels=10)  # 假设有5种命名实体类别
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2).squeeze().tolist()
    tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'].squeeze().tolist())
    return tokens, predictions

# 获取并显示实体
def extract_entities(tokens, predictions):
    entities = []
    current_entity = ''
    for token, pred in zip(tokens, predictions):
        if pred != 0:  # 假设命名实体类别0表示普通词
            if current_entity:
                current_entity += token.replace('##', '')
            else:
                current_entity = token.replace('##', '')
        else:
            if current_entity:
                entities.append(current_entity.strip())
                current_entity = ''
    if current_entity:
        entities.append(current_entity.strip())
    return entities

def write_entities_to_txt(entities):
    with open('entities_output.txt', 'w', encoding='utf-8') as file:
        file.write("Entities found in the article:\n")
        for entity in entities:
            file.write(f"{entity}\n")

def main():
    url = 'https://www.mbishop.com.tw/Article/Detail/79781'  # 文章的网址
    article_content = scrape_article_content(url)
    cleaned_text = preprocess_text(article_content)
    tokens, predictions = perform_ner(cleaned_text)
    entities = extract_entities(tokens, predictions)
    write_entities_to_txt(entities)

if __name__ == "__main__":
    main()
