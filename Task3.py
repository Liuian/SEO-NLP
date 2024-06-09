# pip install plotly
import pygsheets
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# 授權訪問Google Sheets
gc = pygsheets.authorize(service_file='deep-cascade-425708-t5-bfff383647bd.json')  # 替換為你的服務帳戶凭证

# 讀取Google Sheets中的數據
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1HEKz3_iiSTeA6xd6mAbeJD0WrXYT8AYl5b0K38c-BYk/edit?gid=0#gid=0')
wks = sh[0]  # 選擇工作表
df = wks.get_as_df()  # 將數據讀取為DataFrame

# 分詞長度統計
df['word_count_title'] = df['segmented_title'].apply(lambda x: len(x.split()))
df['word_count_meta'] = df['segmented_meta'].apply(lambda x: len(x.split()))
df['word_count_content'] = df['segmented_content'].apply(lambda x: len(x.split()))

# 創建儀表板
fig = go.Figure()

# 添加直方圖軌跡
fig.add_trace(go.Histogram(x=df['word_count_title'], name='Title', nbinsx=20))
fig.add_trace(go.Histogram(x=df['word_count_meta'], name='Meta', nbinsx=20))
fig.add_trace(go.Histogram(x=df['word_count_content'], name='Content', nbinsx=20))

# 更新佈局
fig.update_layout(title='分詞長度分佈',
                  xaxis_title='詞數',
                  yaxis_title='數量')

# 顯示儀表板
fig.show()