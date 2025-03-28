"""
使用 context manager 的範例：模擬一個網頁爬蟲任務
"""
import os
import sys
import time
import logging
import random
from dotenv import load_dotenv
from py_mail_me import EmailNotifier

load_dotenv()

# 設定 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def crawl_website(url):
    """模擬爬蟲過程"""
    logger.info(f"開始爬取網站: {url}")
    time.sleep(random.uniform(0.5, 1.5))  # 模擬網頁載入時間
    
    # 模擬資料處理
    data = [f"數據 {i}" for i in range(5)]
    for item in data:
        logger.info(f"處理資料: {item}")
        time.sleep(0.5)
    
    return data

def main():
    websites = [
        "https://example1.com",
        "https://example2.com",
        "https://example3.com"
    ]
    
    with EmailNotifier(
        email=os.getenv("EMAIL_USER"),  # 可發送給多個收件人
        subject="網站爬蟲完成通知",
        attach_logs=True,
        password=os.getenv("EMAIL_PASSWORD")
    ):
        logger.info("開始執行爬蟲任務...")
        
        all_data = []
        for url in websites:
            try:
                data = crawl_website(url)
                all_data.extend(data)
                logger.info(f"成功爬取 {url}，獲得 {len(data)} 筆資料")
            except Exception as e:
                logger.error(f"爬取 {url} 時發生錯誤: {str(e)}")
                raise  # 重新拋出異常，EmailNotifier 會捕獲並發送錯誤通知
            
        logger.info(f"爬蟲完成，共收集 {len(all_data)} 筆資料")
        
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"任務失敗: {e}")  # 程式會結束，但錯誤通知已發送 