# Task2: 用CKIP進行斷詞斷句並輸出到google sheet(串接pygsheet套件)
# reference: https://ithelp.ithome.com.tw/articles/10234325
import pygsheets
from ckiptagger import WS
import pandas as pd

# 斷詞斷句
def ckip_segmentation(text_list):
    ws = WS("./data")  # 加载 CKIP 模型
    word_sentence_list = ws(text_list)
    return word_sentence_list

# 讀取CSV文件
df = pd.read_csv('google_results.csv')

# 將 NaN 值替換為空字符串
df['title'] = df['title'].fillna('')
df['meta'] = df['meta'].fillna('')
df['content'] = df['content'].fillna('')

# 分別處理title、meta和content進行斷詞
title_list = df['title'].tolist()
meta_list = df['meta'].tolist()
content_list = df['content'].tolist()

segmented_title = ckip_segmentation(title_list)
segmented_meta = ckip_segmentation(meta_list)
segmented_content = ckip_segmentation(content_list)

# 將斷詞結果添加到原DataFrame
df['segmented_title'] = [' '.join(words) for words in segmented_title]
df['segmented_meta'] = [' '.join(words) for words in segmented_meta]
df['segmented_content'] = [' '.join(words) for words in segmented_content]

# 將結果寫入 Google Sheets
def write_to_google_sheet(df):
    gc = pygsheets.authorize(service_file='deep-cascade-425708-t5-bfff383647bd.json')  # 连接到 Google Sheets
    # 替換下面這行的 URL 為你的 Google Sheets 文件的 URL
    sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1HEKz3_iiSTeA6xd6mAbeJD0WrXYT8AYl5b0K38c-BYk/edit?gid=0#gid=0')
    wks = sh[0]  # 选择工作表
    wks.set_dataframe(df, start='A1')  # 將結果寫入工作表

write_to_google_sheet(df)