5. 如何分析SEO的排名要素？請從量化與質化數據個別探討
* 請爬取google第一到第三頁關於心理諮商的標題/meta/內容
* 用CKIP進行斷詞斷句並輸出到google sheet(串接pygsheet套件)：https://docs.google.com/spreadsheets/d/1HEKz3_iiSTeA6xd6mAbeJD0WrXYT8AYl5b0K38c-BYk/edit?gid=0#gid=0
* 用Python plotly做出簡易儀錶板(加分題)
* 運用圖表做出簡易分析  

6. 請用不同NER技術標註此篇文章的實體（請不要以單個字進行拆解，需要是一個詞） 
* 如何拆解解決問題的流程
  * 讀取並理解文章的內容
  * NER 技術選擇
  * 文本預處理：對文章進行文本清理，包括刪除特殊字符、標點符號等，以確保文本的整潔性。
  * 實體標註：使用所選擇的NER技術對文章進行實體標註，識別出文中的人名、地名、組織名等命名實體。
  * 實體分類： 將識別出的實體進行分類，區分出不同類型的實體，例如人物、地點、機構等。
  * 檢查實體標註的結果，確保實體標註的準確性和完整性。
* 使用哪一個演算法進行NER拆解(提示BERT）
  * BERT（Bidirectional Encoder Representations from Transformers）是一種基於Transformer架構的自然語言處理（NLP）模型。
  * 雙向性：同時從左右兩個方向考慮上下文
  * Transformer架構：能夠捕捉句子中各個詞之間的長距依賴關係。
  * BERT可以進行微調（fine-tuning）來適應具體的NLP任務。微調過程中，BERT會在有標註數據的小規模數據集上進行短時間的訓練，以適應特定任務的需求。
* 實際執行並將實體用google sheet輸出
  * 自學有關爬蟲的兩個技術花比較多時間1. 因為頁面是javascript動態加載，因此要等待一段時間讓頁面完全加載。2. 片栗HTML的所有子標籤並獲取文字。


連結：https://docs.google.com/document/d/1BUG8PDLBFFBfQfu_7RJvpq7nUL30_tPWdkFHqh5FO6s/edit
