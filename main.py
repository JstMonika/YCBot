#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
極簡KKTIX搶票機器人
"""

import json
import os
from platforms.kktix import KKTIXBot

def load_settings():
    """載入設定檔案"""
    try:
        with open('settings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"載入設定失敗: {e}")
        return None
    
def create_bot(settings):
    """
    根據設定建立對應的搶票機器人
    """
    event_url = settings.get('event_url', '').lower()
    
    if 'kktix' in event_url:
        return KKTIXBot(settings)
    # TODO: 未來可以新增其他平台
    # elif 'tixcraft' in event_url:
    #     from platforms.tixcraft import TixCraftBot
    #     return TixCraftBot(settings)
    # elif 'famiticket' in event_url:
    #     from platforms.famiticket import FamiTicketBot
    #     return FamiTicketBot(settings)
    else:
        print(f"不支援的平台網址: {event_url}")
        return None

def main():
    print("=== TicketBot 自動購票機器人 ===")
    
    # 載入設定
    settings = load_settings()
    if not settings:
        return
    
    # 顯示設定
    print(f"目標網址: {settings.get('event_url')}")
    print(f"票種: {settings.get('ticket_type')}")
    print(f"數量: {settings.get('quantity')}")
    
    # 建立搶票機器人
    bot = create_bot(settings)
    if not bot:
        return
    
    # 驗證設定
    if not bot.validate_settings():
        print("設定驗證失敗，請檢查設定檔")
        return
    
    # 開始搶票
    print(f"\n準備開始 {bot.get_platform_name()} 搶票...")
    success = bot.start_booking()
    
    if success:
        print("搶票流程完成")
    else:
        print("搶票流程失敗")

if __name__ == "__main__":
    main() 