# py-mail-me

**py-mail-me** 是一個簡單易用的 Python 套件，讓你在任務（如資料處理、模型訓練、爬蟲等）完成後，自動寄送 Email 通知，並附上 log 或執行輸出。適合長時間執行的程式、定期任務、CI/CD 流程、自動化腳本等。

---

## 特點 Features

- **任務完成後自動發送通知信件**
- **支援附加 log 檔或輸出檔案**
- **可使用裝飾器或 context manager 快速整合**
- **自訂 Email 收件人、主旨與內容**
- **支援 logging 模組整合**

---

## 安裝 Installation

```bash
pip install py-mail-me
```

或從 GitHub 安裝最新版本：

```bash
pip install git+https://github.com/juihsuanlee0303/py-mail-me.git
```

---

## 快速開始 Quick Start

### 使用裝飾器（Decorator）

```python
from py_mail_me import py_mail_me

@py_mail_me(
    email="you@example.com",
    subject="任務完成通知",
    attach_logs=True,
    password="your password"
)
def long_running_task():
    print("執行中...")
    # 任務邏輯
```

### 使用 context manager

```python
from py_mail_me import EmailNotifier

with EmailNotifier(
    email="you@example.com",
    subject="資料處理完成",
    attach_logs=True,
    password="your password"
):
    # 執行主要工作
    print("處理中...")
```

---

## 設定 Configuration

你可以透過環境變數或 `.env` 檔設定 email 寄信帳號：

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-password-or-app-password
```

或程式中直接傳入設定參數。

---

## 使用範例 Examples

在 `examples` 目錄中提供了多個實際應用範例：

### 1. 機器學習訓練通知 (decorator_example.py)

使用裝飾器方式在模型訓練完成後發送通知：

```python
@py_mail_me(
    email="your-email@gmail.com",
    subject="模型訓練完成通知",
    attach_logs=True,
    password="your password"
)
def train_model():
    logger.info("開始訓練模型...")
    # 訓練過程...
    logger.info("模型訓練完成！")
```

### 2. 網頁爬蟲任務 (context_manager_example.py)

使用 context manager 在爬蟲任務完成後發送通知給多個收件人：

```python
with EmailNotifier(
    email=["admin@example.com", "team@example.com"],
    subject="網站爬蟲完成通知",
    attach_logs=True,
    password="your password"
):
    logger.info("開始執行爬蟲任務...")
    # 爬蟲過程...
    logger.info("爬蟲完成")
```

### 3. 錯誤處理 (error_handling_example.py)

展示如何在任務失敗時自動發送錯誤通知：

```python
with EmailNotifier(
    email="admin@example.com",
    subject="資料處理狀態通知",
    attach_logs=True,
    password="your password"
):
    try:
        result = process_data(invalid_data)
    except Exception as e:
        logger.error(f"處理失敗: {str(e)}")
        raise  # EmailNotifier 會捕獲錯誤並發送通知
```

完整的範例程式碼可以在 `examples` 目錄中找到。

---

## 適用場景 Use Cases

- 資料處理流程（ETL、資料清洗）
- 機器學習訓練任務
- 爬蟲與報表生成
- 每日/每週定時排程任務
- 自動化測試或部署完成後通知
- 需要遠端通知的 CLI 工具

---

## 發展規劃 Roadmap

- [x] 基本 email 通知功能
- [x] 附加 log 檔案或任務輸出
- [ ] 支援錯誤捕捉並寄出錯誤通知
- [ ] 支援多通訊方式（如 Telegram, Slack, LINE Notify）
- [ ] 建立 Web UI 管理通知歷史紀錄
- [ ] 整合 Python logging 模組自動紀錄

---

## 貢獻方式 Contributing

歡迎發送 PR、開 issue 討論新功能或改善設計。

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/my-feature`)
3. 提交更改 (`git commit -am 'Add new feature'`)
4. Push 到分支 (`git push origin feature/my-feature`)
5. 發送 Pull Request

---

## 授權 License

MIT License

---

## 聯絡 Contact

有問題或建議歡迎聯絡作者：

- GitHub: [your-username](https://github.com/your-username)
- Email: `your-email@example.com`
