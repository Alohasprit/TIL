#!/bin/bash

# cron 작업 설정 스크립트

echo "cron 작업을 설정합니다..."

# 현재 사용자의 crontab에 작업 추가
(crontab -l 2>/dev/null; echo "0 8 * * * cd /Users/hoyounson/Desktop/workspace/TIL/11_Stock-Updater && python3 stock_updater.py >> stock_updater_cron.log 2>&1") | crontab -

echo "✅ cron 작업이 설정되었습니다."
echo "매일 오전 8시에 자동 실행됩니다."
echo ""
echo "cron 작업 확인: crontab -l"
echo "cron 로그 확인: tail -f stock_updater_cron.log"
echo "cron 작업 제거: crontab -e (해당 라인 삭제)"
