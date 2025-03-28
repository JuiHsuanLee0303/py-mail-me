"""
錯誤處理範例：展示如何在任務失敗時發送錯誤通知
"""

import logging
import sys
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.py_mail_me import EmailNotifier

# 設定 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_data(data):
    """模擬資料處理過程"""
    if not isinstance(data, list):
        raise TypeError("輸入必須是列表類型")
    
    logger.info("開始處理資料...")
    
    # 模擬一些可能出錯的操作
    for i, item in enumerate(data):
        if not isinstance(item, (int, float)):
            raise ValueError(f"資料項目 {i} 不是數字類型")
        logger.info(f"處理項目 {i}: {item}")
    
    return [x * 2 for x in data]

def main():
    # 正確的輸入
    valid_data = [1, 2, 3, 4, 5]
    
    # 錯誤的輸入（包含非數字）
    invalid_data = [1, 2, "3", 4, 5]
    
    # 使用 context manager 處理錯誤情況
    with EmailNotifier(
        email="admin@example.com",
        subject="資料處理狀態通知",
        attach_logs=True
    ):
        logger.info("開始執行資料處理任務...")
        
        try:
            # 嘗試處理無效資料
            result = process_data(invalid_data)
        except Exception as e:
            logger.error(f"處理失敗: {str(e)}")
            raise  # 重新拋出異常，EmailNotifier 會捕獲並發送錯誤通知
        
        logger.info("資料處理完成")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"任務失敗: {e}")  # 程式會結束，但錯誤通知已發送 