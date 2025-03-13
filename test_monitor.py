# -*- coding: utf-8 -*-
import time
import signal
import sys
from twitter_monitor import TwitterMonitor
from dotenv import load_dotenv

def signal_handler(sig, frame):
    """����Ctrl+C�źţ����ŵ��˳�����"""
    print("\n�����˳�����...")
    sys.exit(0)

def handle_new_promotion(username):
    """�����·��ֵ��ƹ��û�"""
    print(f"�������ƹ��û�: {username}")
    print(f"�û�ҳ��: https://time.fun/{username}")
    print("-" * 50)

if __name__ == "__main__":
    # ���ػ�������
    load_dotenv(dotenv_path=".env.utf8")
    
    # ע���źŴ�����������Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=== Twitter��ز��� ===")
    print("���ڳ�ʼ��Twitter���ģ��...")
    
    # ��ʼ��Twitter���ģ��
    monitor = TwitterMonitor()
    
    print("��ʼ����ɣ���ʼ���...")
    print("��Ctrl+C�˳�")
    print("-" * 50)
    
    try:
        # ��ʼ���Twitter
        monitor.monitor(handle_new_promotion)
    except Exception as e:
        print(f"�������г���: {e}")
        sys.exit(1) 