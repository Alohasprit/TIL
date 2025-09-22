#!/bin/bash

# 주식 업데이터 중지 스크립트

echo "주식 업데이터를 중지합니다..."

# PID 파일이 있는지 확인
if [ -f "stock_updater.pid" ]; then
    PID=$(cat stock_updater.pid)
    echo "프로세스 ID: $PID"
    
    # 프로세스가 실행 중인지 확인
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✅ 주식 업데이터가 중지되었습니다."
        rm stock_updater.pid
    else
        echo "❌ 프로세스가 실행 중이 아닙니다."
        rm stock_updater.pid
    fi
else
    echo "❌ PID 파일을 찾을 수 없습니다."
    echo "수동으로 중지하려면: pkill -f stock_updater.py"
fi
