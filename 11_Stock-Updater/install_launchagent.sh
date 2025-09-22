#!/bin/bash

# macOS LaunchAgent 설치 스크립트

echo "macOS LaunchAgent를 설치합니다..."

# LaunchAgent 디렉토리 생성
mkdir -p ~/Library/LaunchAgents

# plist 파일 복사
cp com.stockupdater.plist ~/Library/LaunchAgents/

# 권한 설정
chmod 644 ~/Library/LaunchAgents/com.stockupdater.plist

# LaunchAgent 로드
launchctl load ~/Library/LaunchAgents/com.stockupdater.plist

echo "✅ LaunchAgent가 설치되었습니다."
echo "시스템 부팅 시 자동으로 시작됩니다."
echo ""
echo "관리 명령어:"
echo "  시작: launchctl start com.stockupdater"
echo "  중지: launchctl stop com.stockupdater"
echo "  상태: launchctl list | grep com.stockupdater"
echo "  제거: launchctl unload ~/Library/LaunchAgents/com.stockupdater.plist"
