#!/bin/bash

# 미국 주식 자동 업데이트 스크립트 설치 스크립트

echo "미국 주식 자동 업데이트 스크립트 설치를 시작합니다..."

# Python 가상환경 생성 (선택사항)
read -p "가상환경을 생성하시겠습니까? (y/n): " create_venv
if [ "$create_venv" = "y" ]; then
    echo "가상환경을 생성합니다..."
    python3 -m venv stock_updater_env
    source stock_updater_env/bin/activate
    echo "가상환경이 활성화되었습니다."
fi

# 필요한 라이브러리 설치
echo "필요한 라이브러리를 설치합니다..."
pip install -r requirements.txt

# 실행 권한 부여
chmod +x stock_updater.py

echo "설치가 완료되었습니다!"
echo ""
echo "다음 단계를 수행하세요:"
echo "1. Google Cloud Console에서 서비스 계정을 생성하고 credentials.json 파일을 다운로드하세요"
echo "2. config.json 파일에서 스프레드시트 ID와 주식 심볼을 설정하세요"
echo "3. Google 스프레드시트에 서비스 계정 이메일을 공유자로 추가하세요"
echo "4. python stock_updater.py 명령으로 스크립트를 실행하세요"
