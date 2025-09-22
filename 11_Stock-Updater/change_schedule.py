#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
스케줄 시간 변경 스크립트
"""

import sys
import re

def change_schedule_time(new_time):
    """스케줄 시간을 변경합니다."""
    try:
        # stock_updater.py 파일 읽기
        with open('stock_updater.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 현재 시간 패턴 찾기 및 교체
        pattern = r'schedule\.every\(\)\.day\.at\("([^"]+)"\)\.do\(self\.run_update\)'
        replacement = f'schedule.every().day.at("{new_time}").do(self.run_update)'
        
        new_content = re.sub(pattern, replacement, content)
        
        # 파일에 다시 쓰기
        with open('stock_updater.py', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ 스케줄 시간이 {new_time}으로 변경되었습니다.")
        return True
        
    except Exception as e:
        print(f"❌ 스케줄 시간 변경 중 오류 발생: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("사용법: python3 change_schedule.py <시간>")
        print("예시: python3 change_schedule.py 09:30")
        sys.exit(1)
    
    new_time = sys.argv[1]
    
    # 시간 형식 검증 (HH:MM)
    if not re.match(r'^\d{1,2}:\d{2}$', new_time):
        print("❌ 잘못된 시간 형식입니다. HH:MM 형식을 사용하세요.")
        print("예시: 08:00, 09:30, 14:15")
        sys.exit(1)
    
    if change_schedule_time(new_time):
        print(f"이제 매일 {new_time}에 실행됩니다.")
        print("변경사항을 적용하려면 스크립트를 다시 시작하세요.")

if __name__ == "__main__":
    main()
