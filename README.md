# TicketBot - 自動購票機器人

## 專案簡介

TicketBot 是一個採用物件導向設計的多平台自動購票機器人，支援 KKTIX、TixCraft、FamiTicket 等票務平台。使用 undetected_chromedriver 技術避免被反爬蟲系統偵測，並採用抽象基礎類別架構，方便擴展至不同平台。

## 主要功能

- **物件導向設計**：使用抽象基礎類別 (ABC) 架構，確保各平台一致性
- **多平台架構**：可輕鬆擴展支援新的票務平台
- **KKTIX 支援**：完整的 KKTIX 平台搶票邏輯
- **反偵測技術**：使用 undetected_chromedriver 避免被系統封鎖
- **智慧重試**：自動重新整理和重試機制，最大化搶票成功率
- **設定簡單**：JSON 格式設定檔，配置直觀簡單

## 技術架構

### 核心技術
- **Python 抽象基礎類別 (ABC)**：統一的平台介面
- **undetected-chromedriver**：避免反爬蟲偵測
- **selenium**：網頁自動化操作
- **python 3.8+**：現代 Python 語法支援

### 專案結構
```
YCBot/
├── main.py                    # 程式入口點與平台工廠
│   ├── __init__.py           # 套件初始化檔案
│   └── platforms/            # 平台模組目錄
│       ├── base.py           # BaseTicketBot 抽象基礎類別
│       └── kktix.py          # KKTIXBot 類別實作
├── requirements.txt           # 依賴套件清單
├── settings.json              # 搶票設定檔
├── README.md                  # 專案說明文件
├── .gitignore                # Git 忽略檔案設定
├── html_analysis/            # HTML 分析檔案
│   ├── kktix_raw.html       # KKTIX 頁面原始 HTML
│   ├── kktix_raw2.html      # KKTIX 頁面原始 HTML (版本2)
│   ├── analysis_result.txt   # 分析結果
│   ├── css_selector_analysis.txt  # CSS 選擇器分析
│   └── ticket_container_analysis.txt  # 票種容器分析
├── logs/                     # 執行日誌目錄
├── screenshots/              # 截圖存放目錄
└── __pycache__/             # Python 快取檔案
```

## 快速開始

### 環境需求
- Python 3.8 或更高版本
- Chrome 瀏覽器
- Windows/Linux/macOS 系統

### 安裝步驟

1. **下載專案**
```bash
git clone <repository-url>
cd TicketBot/YCBot
```

2. **安裝依賴套件**
```powershell
pip install -r requirements.txt
```

3. **設定配置檔案**
編輯 `settings.json` 檔案，設定目標事件：
```json
{
  "event_url": "https://kktix.com/events/your-event/registrations/new",
  "ticket_type": "預售票",
  "quantity": 1,
  "headless": false
}
```

4. **執行程式**
```powershell
python main.py
```

## 物件導向架構

### BaseTicketBot 抽象基礎類別 (platforms/base.py)

定義所有平台搶票機器人的標準介面：

```python
class BaseTicketBot(ABC):
    @abstractmethod
    def setup_browser_and_navigate(self):
        """步驟1-2: 啟動瀏覽器並導航到目標網頁"""
        pass
    
    @abstractmethod
    def wait_for_manual_login(self):
        """步驟3: 等待使用者手動登入"""
        pass
    
    @abstractmethod
    def ticket_booking_loop(self):
        """步驟4-7: 執行搶票主循環"""
        pass
    
    def start_booking(self):
        """主控流程：協調執行完整搶票流程"""
        # 統一的流程控制邏輯
```

#### 核心功能
- **標準流程**：定義 7 步驟搶票流程架構
- **異常處理**：統一的錯誤處理和使用者中斷處理
- **資源管理**：自動清理瀏覽器等資源
- **設定驗證**：基礎設定檔驗證功能

### KKTIXBot 實作類別 (platforms/kktix.py)

繼承 BaseTicketBot 並實作 KKTIX 平台特定邏輯：

```python
class KKTIXBot(BaseTicketBot):
    def get_platform_name(self):
        return "KKTIX"
    
    def setup_browser_and_navigate(self):
        # KKTIX 特定的瀏覽器啟動和導航邏輯
    
    def wait_for_manual_login(self):
        # KKTIX 的登入等待流程
    
    def ticket_booking_loop(self):
        # KKTIX 的搶票循環邏輯
```

## KKTIX 搶票 7 步驟流程

### 模組化設計

搶票流程被拆分為 3 個核心方法：

#### **setup_browser_and_navigate()** - 步驟 1-2
1. **步驟1：啟動瀏覽器**
   - 使用 undetected_chromedriver 啟動 Chrome
   - 設定基本瀏覽器選項
2. **步驟2：連到目標網頁**
   - 根據 settings.json 中的 event_url 導航

#### **wait_for_manual_login()** - 步驟 3
3. **步驟3：等待手動登入**
   - 程式暫停，等待使用者手動登入 KKTIX 帳號
   - 按 Enter 後繼續執行

#### **ticket_booking_loop()** - 步驟 4-7
4. **步驟4：尋找可選票種**
   - 搜尋 `div.display-table-row` 票種容器
   - 檢查票種是否可選購（非售完狀態）
5. **步驟5：選擇數量**
   - 在目標票種的輸入框中填入數量
6. **步驟6：勾選同意**
   - 自動勾選同意條款 (`#person_agree_terms`)
7. **步驟7：按下一步**
   - 點擊「下一步」按鈕完成搶票

## 使用方式

### 程式流程
```python
# 1. 載入設定
settings = load_settings()

# 2. 自動選擇平台 (工廠模式)
bot = create_bot(settings)  # 根據網址自動建立對應的 Bot

# 3. 驗證設定
bot.validate_settings()

# 4. 開始搶票
bot.start_booking()
```

### 實際使用流程
1. 修改 `settings.json` 設定目標活動和票種
2. 執行 `python main.py`
3. 程式自動識別平台並建立對應的機器人
4. 瀏覽器會自動開啟並導航到活動頁面
5. **重要：手動登入您的帳號**
6. 登入完成後回到終端機按 Enter 鍵
7. 程式開始自動搶票，最多嘗試 300 次
8. 搶票成功後會暫停，請檢查訂單狀態

## 設定說明

### settings.json 設定檔

```json
{
  "event_url": "KKTIX活動報名網址",
  "ticket_type": "目標票種名稱（如：預售票、一般票）",
  "quantity": 1,
  "headless": false
}
```

### 設定項目說明

- **event_url**: 票務平台活動的報名頁面網址 (程式會自動識別平台)
- **ticket_type**: 想要搶購的票種名稱，留空 `""` 表示搶第一個可用票種
- **quantity**: 購票數量
- **headless**: 是否使用無頭模式（false = 顯示瀏覽器視窗）

## 開發指南

### 新增平台支援

1. **建立新的平台類別**
```python
# platforms/tixcraft.py
from .base import BaseTicketBot

class TixCraftBot(BaseTicketBot):
    def get_platform_name(self):
        return "TixCraft"
    
    def setup_browser_and_navigate(self):
        # 實作 TixCraft 的步驟1-2
        pass
    
    def wait_for_manual_login(self):
        # 實作 TixCraft 的步驟3
        pass
    
    def ticket_booking_loop(self):
        # 實作 TixCraft 的步驟4-7
        pass
```

2. **在主程式中註冊**
```python
# main.py
def create_bot(settings):
    event_url = settings.get('event_url', '').lower()
    
    if 'kktix' in event_url:
        return KKTIXBot(settings)
    elif 'tixcraft' in event_url:
        from platforms.tixcraft import TixCraftBot
        return TixCraftBot(settings)
    # ... 其他平台
```

### 設計原則

- **統一介面**：所有平台都使用相同的抽象方法
- **模組化**：每個平台獨立實作，互不影響
- **可擴展**：新增平台只需實作抽象方法
- **向後相容**：保留原有函數接口供舊版本使用

## TODO - 待完成功能

### 高優先級
- [ ] **接管現有瀏覽器功能** - 允許程式連接到已開啟的 Chrome 瀏覽器實例
  - [ ] 在 BaseTicketBot 中實作 `connect_to_existing_browser()` 方法
  - [ ] 增加 `use_existing_browser` 設定選項
  - [ ] 增加遠程調試連接埠設定 (`debug_port`)
- [ ] **TixCraft 平台支援** - 實作 TixCraftBot 類別
- [ ] **FamiTicket 平台支援** - 實作 FamiTicketBot 類別
- [ ] **錯誤處理優化** - 改善各種異常情況的處理
- [ ] **日誌系統** - 完整的操作記錄和錯誤追蹤

### 中優先級
- [ ] **多票種支援** - 在 BaseTicketBot 中支援同時搶購多種票型
- [ ] **購票優先級** - 設定票種的搶購優先順序
- [ ] **驗證碼處理** - 在基礎類別中統一處理驗證碼
- [ ] **通知系統** - 搶票成功/失敗的通知機制
- [ ] **設定檔管理** - 多個活動設定檔管理

### 低優先級
- [ ] **GUI 介面** - 圖形化使用者介面
- [ ] **測試框架** - 完整的功能測試套件
- [ ] **效能監控** - 搶票流程效能分析
- [ ] **配置檔案熱重載** - 不重啟程式即可更新設定

## 注意事項

1. **合法使用**: 請遵守各票務平台的使用條款和相關法規
2. **帳號安全**: 程式不會儲存您的帳號密碼，需要手動登入
3. **頻率控制**: 程式已內建適當的等待時間，避免過於頻繁請求
4. **成功率**: 熱門活動競爭激烈，無法保證 100% 搶票成功

## 常見問題

### Q: Chrome 被偵測到自動化怎麼辦？
A: 程式使用 undetected_chromedriver，若仍被偵測請更新套件到最新版本。

### Q: 找不到票種怎麼辦？
A: 檢查 `ticket_type` 設定是否正確，或設為空字串 `""` 搶第一個可用票種。

### Q: 程式一直重新整理頁面？
A: 表示目標票種尚未開賣或已售完，程式會持續監控直到可購買。

### Q: 如何新增其他平台？
A: 建立繼承 `BaseTicketBot` 的新類別，實作所有抽象方法即可。

### Q: 如何停止程式？
A: 在終端機中按 `Ctrl+C` 強制停止程式。

## 開發說明

### 核心檔案說明

- **main.py**: 程式入口，平台工廠和流程控制
- **platforms/base.py**: 抽象基礎類別，定義統一介面
- **platforms/kktix.py**: KKTIX 平台實作
- **html_analysis/**: 包含各平台頁面分析結果

### CSS 選擇器 (KKTIX)

KKTIX 平台使用以下 CSS 選擇器定位頁面元素：
- 票種容器: `div.display-table-row`
- 票數輸入框: `input[type='text']`
- 同意條款: `#person_agree_terms`
- 下一步按鈕: `div.register-new-next-button-area > button`

## 授權條款

本專案採用 MIT 授權條款。

---

**使用前請確實理解各票務平台的使用條款，並自行承擔使用風險。** 