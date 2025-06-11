#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搶票機器人基礎類別
定義通用的搶票流程架構
"""

from abc import ABC, abstractmethod


class BaseTicketBot(ABC):
    """
    搶票機器人基礎抽象類別
    定義標準的搶票流程，各平台繼承並實作具體方法
    """
    
    def __init__(self, settings):
        """
        初始化搶票機器人
        
        Args:
            settings (dict): 搶票設定參數
        """
        self.settings = settings
        self.driver = None
        
    @abstractmethod
    def setup_browser_and_navigate(self):
        """
        步驟1-2: 啟動瀏覽器並導航到目標網頁
        
        Returns:
            WebDriver: 瀏覽器驅動物件，失敗則返回 None
        """
        pass
    
    @abstractmethod
    def wait_for_manual_login(self):
        """
        步驟3: 等待使用者手動登入
        各平台可根據需求自定義登入流程
        """
        pass
    
    @abstractmethod
    def ticket_booking_loop(self):
        """
        步驟4-7: 執行搶票主循環
        
        Returns:
            bool: 搶票成功返回 True，失敗返回 False
        """
        pass
    
    def start_booking(self):
        """
        主控流程：協調執行完整搶票流程
        這是所有平台共用的流程架構
        """
        try:
            print(f"=== {self.get_platform_name()} 搶票開始 ===")
            
            # 步驟1-2: 啟動瀏覽器並導航
            self.driver = self.setup_browser_and_navigate()
            if not self.driver:
                print("瀏覽器啟動失敗，終止程序")
                return False
            
            # 步驟3: 等待手動登入
            self.wait_for_manual_login()
            
            # 步驟4-7: 執行搶票循環
            success = self.ticket_booking_loop()
            
            # 處理搶票結果
            if success:
                print("搶票成功！")
                input("按 Enter 關閉瀏覽器...")
                return True
            else:
                print("搶票失敗")
                input("按 Enter 關閉瀏覽器...")
                return False
                
        except KeyboardInterrupt:
            print("\n使用者中斷搶票")
            return False
            
        except Exception as e:
            print(f"搶票過程發生錯誤: {e}")
            return False
            
        finally:
            # 清理資源
            self.cleanup()
    
    def cleanup(self):
        """
        清理資源：關閉瀏覽器等
        """
        if self.driver:
            try:
                self.driver.quit()
                print("瀏覽器已關閉")
            except Exception as e:
                print(f"關閉瀏覽器時發生錯誤: {e}")
    
    @abstractmethod
    def get_platform_name(self):
        """
        取得平台名稱
        
        Returns:
            str: 平台名稱（如 "KKTIX", "TixCraft" 等）
        """
        pass
    
    def validate_settings(self):
        """
        驗證設定檔案的必要欄位
        子類別可以重寫此方法來檢查平台特定的設定
        
        Returns:
            bool: 設定有效返回 True，否則返回 False
        """
        required_fields = ['event_url']
        
        for field in required_fields:
            if not self.settings.get(field):
                print(f"缺少必要設定: {field}")
                return False
        
        return True 