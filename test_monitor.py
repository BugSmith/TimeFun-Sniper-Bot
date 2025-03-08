# -*- coding: utf-8 -*-
import time
import signal
import sys
from twitter_monitor import TwitterMonitor
from dotenv import load_dotenv

def signal_handler(sig, frame):
    """处理Ctrl+C信号，优雅地退出程序"""
    print("\n正在退出程序...")
    sys.exit(0)

def handle_new_promotion(username):
    """处理新发现的推广用户"""
    print(f"发现新推广用户: {username}")
    print(f"用户页面: https://time.fun/{username}")
    print("-" * 50)

if __name__ == "__main__":
    # 加载环境变量
    load_dotenv(dotenv_path=".env.utf8")
    
    # 注册信号处理器，处理Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=== Twitter监控测试 ===")
    print("正在初始化Twitter监控模块...")
    
    # 初始化Twitter监控模块
    monitor = TwitterMonitor()
    
    print("初始化完成，开始监控...")
    print("按Ctrl+C退出")
    print("-" * 50)
    
    try:
        # 开始监控Twitter
        monitor.monitor(handle_new_promotion)
    except Exception as e:
        print(f"程序运行出错: {e}")
        sys.exit(1) 