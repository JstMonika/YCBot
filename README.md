# 🎫 YCBot - 自動搶票機器人

## 📝 專案簡介

YCBot 是一個支援三大票務平台（拓元、KKTIX、遠大）的自動搶票機器人，使用 undetected_chromedriver 技術避免被反爬蟲系統偵測，並整合 OCR 驗證碼識別功能。

## ✨ 主要功能

- 🎯 **多平台支援**：支援拓元票務、KKTIX、遠大票務
- 🤖 **智慧搶票**：自動登入、搜尋、選位、下單
- 📅 **彈性日期選擇**：支援多個偏好日期自動選擇
- 💺 **智慧選位**：根據偏好自動選擇座位區域
- 🔢 **數量控制**：靈活設定購票張數
- 👁️ **OCR驗證碼**：自動識別並輸入驗證碼
- 🕵️ **反偵測技術**：使用 undetected_chromedriver 避免被封鎖
- 📊 **詳細日誌**：完整記錄搶票過程和結果

## 🛠️ 技術架構

### 核心技術
- **undetected-chromedriver**：避免反爬蟲偵測
- **selenium**：網頁自動化操作
- **pytesseract/easyocr**：OCR驗證碼識別
- **loguru**：高級日誌系統

### 專案結構
```
YCBot/
├── main.py                    # 程式入口點
├── requirements.txt           # 依賴套件
├── config/                    # 設定檔案
│   ├── settings.py           # 主設定管理
│   └── platforms.py          # 平台設定
├── core/                      # 核心模組
│   ├── base_bot.py           # 基礎機器人類別
│   └── ocr_handler.py        # OCR處理器
├── platforms/                 # 平台處理模組
│   ├── tixcraft.py           # 拓元票務
│   ├── kktix.py              # KKTIX票務
│   └── famiticket.py         # 遠大票務
└── utils/                     # 工具模組
    ├── logger.py             # 日誌系統
    ├── webdriver_manager.py  # WebDriver管理
    └── helpers.py            # 輔助工具
```

## 🚀 快速開始

### 環境需求
- Python 3.8+
- Chrome 瀏覽器
- Tesseract OCR (可選)

### 安裝步驟

1. **克隆專案**
```bash
git clone https://github.com/your-username/YCBot.git
cd YCBot
```

2. **安裝依賴**
```bash
pip install -r requirements.txt
```

3. **設定 Tesseract OCR**
- Windows: 下載並安裝 Tesseract OCR
- Linux: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`

4. **執行程式**
```bash
python main.py
```

## ⚙️ 設定說明

### 基本設定
程式首次執行會自動建立 `config.ini` 設定檔，可根據需求調整：

```ini
[webdriver]
headless = false
window_size = 1920,1080
user_agent = auto

[ocr]
engine = tesseract
language = eng+chi_tra

[general]
max_retries = 3
default_wait_time = 10
```

### 平台帳號設定
在程式中設定各平台的登入帳號密碼。

## 🎮 使用方式

1. **選擇平台**：從主選單選擇要使用的票務平台
2. **登入帳號**：輸入該平台的帳號密碼
3. **搜尋活動**：輸入活動關鍵字進行搜尋
4. **設定偏好**：
   - 偏好日期清單
   - 座位區域偏好
   - 購票張數
5. **開始搶票**：確認設定後開始自動搶票流程

## 📊 功能特色

### 智慧選位策略
- 支援多個偏好座位區域
- 價位範圍自動篩選
- 座位品質評估

### 驗證碼處理
- 多引擎OCR支援（Tesseract + EasyOCR）
- 圖片預處理優化識別率
- 失敗自動重試機制

### 反偵測措施
- 隨機化操作時間間隔
- 模擬人類瀏覽行為
- 動態User-Agent切換

## 📝 日誌系統

程式會自動記錄：
- 搶票流程的每個步驟
- 錯誤和異常情況
- 效能統計資訊
- 最終搶票結果

日誌檔案儲存在 `logs/` 目錄下。

## ⚠️ 注意事項

1. **合法使用**：請遵守各平台的使用條款
2. **頻率控制**：避免過於頻繁的請求
3. **帳號安全**：妥善保管帳號密碼
4. **測試建議**：建議先在測試環境試用

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

## 📄 授權條款

本專案採用 MIT 授權條款。

## 🙋 常見問題

### Q: Chrome 被偵測怎麼辦？
A: 程式已使用 undetected_chromedriver，如仍被偵測可嘗試更新版本。

### Q: OCR 識別率不高？
A: 可嘗試切換 OCR 引擎或調整圖片預處理參數。

### Q: 搶票失敗率高？
A: 檢查網路連線、調整重試次數、確認選位策略。

---

**⚡ 祝您搶票成功！** 