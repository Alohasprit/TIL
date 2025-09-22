# 스프레드시트 내장 함수 사용 방법

## Google Finance 함수 직접 사용

### 1. 스프레드시트에 직접 수식 입력

```
A1: Symbol
B1: Date  
C1: Close Price

A2: =GOOGLEFINANCE("AAPL")
B2: =TODAY()
C2: =GOOGLEFINANCE("AAPL","price")
```

### 2. 모든 주식에 대해 수식 복사

```
A3: =GOOGLEFINANCE("TSLA")
B3: =TODAY()
C3: =GOOGLEFINANCE("TSLA","price")

A4: =GOOGLEFINANCE("NVDA")
B4: =TODAY()
C4: =GOOGLEFINANCE("NVDA","price")
```

### 3. 자동 업데이트 설정

- 스프레드시트가 열릴 때마다 자동으로 최신 데이터 조회
- 외부 API 호출 불필요
- 권한 설정 불필요

## 장점

- ✅ 권한 설정 불필요
- ✅ 외부 스크립트 불필요  
- ✅ 자동 업데이트
- ✅ 실시간 데이터

## 단점

- ❌ 수동으로 수식 입력 필요
- ❌ 복잡한 로직 구현 어려움
- ❌ 에러 처리 제한적
