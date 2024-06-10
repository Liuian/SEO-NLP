# 你的代码几乎正确了，但在遍历子标签时，你需要排除包含 HTML 标签的特殊子标签，例如 <strong> 等。你可以使用 .string 属性来获取纯文本内容。让我帮你修改一下代码：
# 看起来页面的内容可能是通过 JavaScript 动态加载的，而 Selenium 获取页面源代码时可能无法获取到动态加载的内容。在这种情况下，你可以尝试等待一段时间，让页面完全加载，然后再获取页面的源代码。

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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

url = 'https://www.mbishop.com.tw/Article/Detail/79781'

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
    print(text_content)
else:
    print("未找到 id 为 root 的 div 标签")
