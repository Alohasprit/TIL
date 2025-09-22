# 미국 주식 자동 업데이트 스크립트

매일 오전 8시에 미국 주식의 전날 종가를 Google 스프레드시트에 자동으로 업데이트하는 스크립트입니다.

## 기능

- 매일 오전 8시 자동 실행
- Yahoo Finance API를 통한 실시간 주식 데이터 조회
- Google Sheets API를 통한 스프레드시트 자동 업데이트
- 로깅 및 에러 처리
- 설정 가능한 주식 심볼 목록

## 설치 및 설정

### 1. 필요한 라이브러리 설치

```bash
pip install -r requirements.txt
```

### 2. Google Sheets API 설정

1. [Google Cloud Console](https://console.cloud.google.com/)에서 새 프로젝트 생성
2. Google Sheets API 활성화
3. 서비스 계정 생성 및 JSON 키 파일 다운로드
4. 다운로드한 키 파일을 `credentials.json`으로 저장
5. 스프레드시트에 서비스 계정 이메일을 공유자로 추가

### 3. 설정 파일 수정

`config.json` 파일을 수정하여 다음 정보를 입력하세요:

```json
{
  "google_credentials_file": "credentials.json",
  "spreadsheet_id": "YOUR_SPREADSHEET_ID_HERE",
  "sheet_name": "Stock Prices",
  "stock_symbols": [
    "AAPL",
    "GOOGL", 
    "MSFT",
    "AMZN",
    "TSLA"
  ]
}
```

- `spreadsheet_id`: Google 스프레드시트 URL에서 ID 부분을 복사
- `stock_symbols`: 조회할 주식 심볼 목록

### 4. 스프레드시트 준비

스프레드시트에 다음 헤더를 가진 시트를 준비하세요:
- A1: Symbol
- B1: Date  
- C1: Close Price

## 실행 방법

### 수동 실행

```bash
python stock_updater.py
```

### 백그라운드 실행 (Linux/Mac)

```bash
nohup python stock_updater.py > output.log 2>&1 &
```

### 시스템 서비스로 등록 (선택사항)

systemd 서비스 파일을 생성하여 시스템 부팅 시 자동 시작되도록 설정할 수 있습니다.

## 로그

- `stock_updater.log`: 상세한 실행 로그
- 콘솔 출력: 실시간 상태 확인

## 문제 해결

### 일반적인 오류

1. **Google Sheets API 오류**: 서비스 계정 권한 확인
2. **주식 데이터 조회 실패**: 인터넷 연결 및 심볼 확인
3. **스케줄링 오류**: 시스템 시간대 확인

### 로그 확인

```bash
tail -f stock_updater.log
```

## 커스터마이징

- `config.json`에서 주식 심볼 목록 수정
- 실행 시간 변경: `schedule.every().day.at("08:00")` 부분 수정
- 스프레드시트 형식 변경: `update_spreadsheet` 메서드 수정
