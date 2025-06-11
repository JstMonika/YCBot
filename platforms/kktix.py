#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KKTIX搶票邏輯 - 繼承基礎類別
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from .base import BaseTicketBot


class KKTIXBot(BaseTicketBot):
    """
    KKTIX 搶票機器人
    繼承 BaseTicketBot 並實作 KKTIX 平台特定的搶票邏輯
    """
    
    def get_platform_name(self):
        """取得平台名稱"""
        return "KKTIX"
    
    def setup_browser_and_navigate(self):
        """
        步驟1-2: 啟動瀏覽器並連到目標網頁
        """
        print("步驟1: 啟動瀏覽器...")
        
        # TODO: 增加選項來決定是否使用現有瀏覽器
        # if self.settings.get('use_existing_browser', False):
        #     # TODO: 連接到現有瀏覽器實例 (使用 Chrome DevTools Protocol)
        #     # driver = connect_to_existing_browser(self.settings.get('debug_port', 9222))
        # else:
        #     # 原有的啟動新瀏覽器邏輯
        
        options = uc.ChromeOptions()
        
        # TODO: 如果要支援接管現有瀏覽器，需要在這裡加入遠程調試設定
        # options.add_argument(f"--remote-debugging-port={self.settings.get('debug_port', 9222)}")
        
        # 基本設定
        if not self.settings.get('headless', False):
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
        else:
            options.add_argument("--headless")
        
        driver = uc.Chrome(options=options)
        driver.implicitly_wait(10)
        
        # 步驟2: 連到目標網頁
        event_url = self.settings.get('event_url')
        if not event_url:
            print("錯誤: 未設定 event_url")
            driver.quit()
            return None
        
        print(f"步驟2: 連接到 {event_url}")
        driver.get(event_url)
        
        return driver

    def wait_for_manual_login(self):
        """
        步驟3: 等待手動登入
        """
        print("步驟3: 請手動登入後按 Enter 繼續...")
        input()

    def ticket_booking_loop(self):
        """
        步驟4-7: 搶票循環
        """
        ticket_type = self.settings.get('ticket_type', '一般票')
        quantity = self.settings.get('quantity', 1)
        
        print(f"開始搶票: {ticket_type} x {quantity}")
        
        max_attempts = 300
        for attempt in range(max_attempts):
            try:
                print(f"第 {attempt + 1} 次嘗試...")
                
                # 步驟4: 尋找可選票種
                ticket_rows = self.driver.find_elements(By.CSS_SELECTOR, 'div.display-table-row')
                
                if not ticket_rows:
                    print("未找到票種，重新整理...")
                    self.driver.refresh()
                    time.sleep(1)
                    continue
                
                # 尋找目標票種
                target_input = None
                for row in ticket_rows:
                    try:
                        row_html = row.get_attribute('innerHTML')
                        row_text = row.text
                        
                        # 檢查是否有輸入框
                        if '<input type=' not in row_html:
                            continue
                        
                        # 檢查是否已售完
                        if any(sold_out in row_text for sold_out in ['未開賣', '暫無票', '已售完', 'Sold Out']):
                            continue
                        
                        # 檢查是否符合目標票種
                        if ticket_type in row_text or ticket_type == '':
                            input_element = row.find_element(By.CSS_SELECTOR, "input[type='text']")
                            if input_element.is_enabled():
                                target_input = input_element
                                print(f"找到目標票種: {row_text.strip()}")
                                break
                    except:
                        continue
                
                if target_input:
                    # 步驟5: 選擇數量
                    print(f"步驟5: 輸入數量 {quantity}")
                    target_input.clear()
                    target_input.send_keys(str(quantity))
                    time.sleep(0.2)
                    
                    # 步驟6: 勾選同意
                    print("步驟6: 勾選同意條款")
                    try:
                        agree_checkbox = self.driver.find_element(By.CSS_SELECTOR, '#person_agree_terms')
                        if not agree_checkbox.is_selected():
                            agree_checkbox.click()
                            time.sleep(0.2)
                    except:
                        print("同意條款處理失敗，繼續...")
                    
                    # 步驟7: 按下一步
                    print("步驟7: 點擊下一步")
                    try:
                        # 重新尋找按鈕避免stale element
                        time.sleep(0.5)
                        next_buttons = self.driver.find_elements(By.CSS_SELECTOR, "div.register-new-next-button-area > button")
                        if next_buttons:
                            self.driver.execute_script("arguments[0].click();", next_buttons[-1])
                            print("搶票成功！")
                            time.sleep(2)  # 等待頁面跳轉
                            print("請檢查訂單狀態")
                            return True
                        else:
                            print("找不到下一步按鈕")
                    except Exception as e:
                        print(f"點擊下一步失敗: {e}")
                        # 嘗試其他可能的按鈕
                        try:
                            all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                            for btn in all_buttons:
                                if "下一步" in btn.text or "next" in btn.text.lower():
                                    self.driver.execute_script("arguments[0].click();", btn)
                                    print("找到替代按鈕，搶票成功！")
                                    time.sleep(2)
                                    return True
                        except:
                            pass
                else:
                    print("目標票種不可選，重新整理...")
                    self.driver.refresh()
                    time.sleep(1)
                    
            except Exception as e:
                print(f"搶票過程出錯: {e}")
                self.driver.refresh()
                time.sleep(1)
        
        print("達到最大嘗試次數，搶票失敗")
        return False

    def validate_settings(self):
        """
        驗證 KKTIX 平台特定的設定
        """
        # 先執行基礎驗證
        if not super().validate_settings():
            return False
        
        # KKTIX 特定的驗證
        event_url = self.settings.get('event_url', '')
        if 'kktix.com' not in event_url.lower():
            print("event_url 不是 KKTIX 網址")
            return False
        
        return True


# 為了保持向後相容性，提供原有的函數接口
def start_booking(settings):
    """
    KKTIX搶票主函數 (向後相容接口)
    """
    bot = KKTIXBot(settings)
    if bot.validate_settings():
        return bot.start_booking()
    else:
        return False 