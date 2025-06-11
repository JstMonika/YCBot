#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
各票務平台的設定資訊
包含URL、選擇器、流程設定等
"""

from typing import Dict, Any


class PlatformConfig:
    """平台設定管理類別"""
    
    # 拓元票務設定
    TIXCRAFT = {
        "name": "拓元票務",
        "base_url": "https://tixcraft.com",
        "login_url": "https://tixcraft.com/login",
        "selectors": {
            "login_button": "",
            "username_field": "",
            "password_field": "",
            "date_selector": "",
            "seat_selector": "",
            "quantity_selector": "",
            "captcha_image": "",
            "captcha_input": "",
            "submit_button": ""
        },
        "wait_times": {
            "page_load": 10,
            "element_wait": 5,
            "captcha_wait": 3
        }
    }
    
    # KKTIX設定
    KKTIX = {
        "name": "KKTIX",
        "base_url": "https://kktix.com",
        "login_url": "https://kktix.com/users/sign_in",
        "selectors": {
            "login_button": "",
            "username_field": "",
            "password_field": "",
            "date_selector": "",
            "seat_selector": "",
            "quantity_selector": "",
            "captcha_image": "",
            "captcha_input": "",
            "submit_button": ""
        },
        "wait_times": {
            "page_load": 10,
            "element_wait": 5,
            "captcha_wait": 3
        }
    }
    
    # 遠大票務設定
    FAMITICKET = {
        "name": "遠大票務",
        "base_url": "https://www.famiticket.com.tw",
        "login_url": "https://www.famiticket.com.tw/Home/Login",
        "selectors": {
            "login_button": "",
            "username_field": "",
            "password_field": "",
            "date_selector": "",
            "seat_selector": "",
            "quantity_selector": "",
            "captcha_image": "",
            "captcha_input": "",
            "submit_button": ""
        },
        "wait_times": {
            "page_load": 10,
            "element_wait": 5,
            "captcha_wait": 3
        }
    }
    
    @classmethod
    def get_platform_config(cls, platform: str) -> Dict[str, Any]:
        """
        根據平台名稱取得對應設定
        支援的平台：tixcraft, kktix, famiticket
        """
        pass
    
    @classmethod
    def get_all_platforms(cls) -> Dict[str, Dict[str, Any]]:
        """
        取得所有平台的設定清單
        返回所有支援平台的設定字典
        """
        pass
    
    @classmethod
    def update_selectors(cls, platform: str, selectors: Dict[str, str]):
        """
        更新特定平台的選擇器設定
        當網站改版時可以動態更新選擇器
        """
        pass 