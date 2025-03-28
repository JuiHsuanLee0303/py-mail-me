"""
使用裝飾器的範例：模擬一個長時間運行的機器學習訓練任務
"""

import os
import time
import logging
import sys
from dotenv import load_dotenv
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.py_mail_me import py_mail_me

load_dotenv()

# 設定 logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@py_mail_me(
    email=os.getenv("EMAIL_USER"),
    subject="模型訓練完成通知",
    attach_logs=True,
    password=os.getenv("EMAIL_PASSWORD")
)
def train_model():
    logger.info("開始訓練模型...")
    
    # 模擬訓練過程
    for epoch in range(5):
        time.sleep(1)  # 模擬訓練時間
        logger.info(f"Epoch {epoch + 1}/5 完成，準確率: {0.8 + epoch * 0.04:.2f}")
    
    logger.info("模型訓練完成！")
    return "訓練成功"

if __name__ == "__main__":
    train_model() 