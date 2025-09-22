#!/bin/bash

# 주식 업데이터 백그라운드 실행 스크립트

echo "주식 업데이터를 백그라운드에서 시작합니다..."

# 현재 디렉토리로 이동
cd /Users/hoyounson/Desktop/workspace/TIL/11_Stock-Updater

# 백그라운드에서 실행
nohup python3 stock_updater.py > stock_updater_output.log 2>&1 &

# 프로세스 ID 저장
echo $! > stock_updater.pid

echo "✅ 주식 업데이터가 백그라운드에서 시작되었습니다."
echo "프로세스 ID: $(cat stock_updater.pid)"
echo "로그 파일: stock_updater_output.log"
echo "실행 상태 확인: ps aux | grep stock_updater.py"
echo "중지하려면: kill $(cat stock_updater.pid)"
