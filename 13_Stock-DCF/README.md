# 주식 DCF (Discounted Cash Flow) 분석기

주식의 내재가치를 DCF 모델을 통해 분석하는 프로젝트입니다.

## 📊 프로젝트 개요

### **DCF 모델이란?**
- **Discounted Cash Flow**: 할인된 현금흐름 분석
- **내재가치 계산**: 주식의 실제 가치를 계산
- **투자 판단**: 현재 주가와 내재가치 비교

### **주요 기능**
- 주식 재무제표 데이터 수집
- FCF (Free Cash Flow) 계산
- 성장률 예측
- WACC (Weighted Average Cost of Capital) 계산
- DCF 모델을 통한 내재가치 계산
- 투자 매력도 분석

## 🚀 기술 스택

- **Python**: 데이터 분석 및 계산
- **yfinance**: 주식 데이터 수집
- **pandas**: 데이터 처리
- **numpy**: 수치 계산
- **matplotlib/seaborn**: 시각화
- **Google Sheets API**: 결과 저장

## 📁 프로젝트 구조

```
13_Stock-DCF/
├── README.md
├── requirements.txt
├── dcf_analyzer.py
├── data_collector.py
├── calculator.py
├── visualizer.py
├── config.json.template
└── examples/
    ├── aapl_dcf_analysis.ipynb
    └── sample_analysis.py
```

## 🔧 설치 및 설정

### **1. 필요한 라이브러리 설치**
```bash
pip install -r requirements.txt
```

### **2. 설정 파일 생성**
```bash
cp config.json.template config.json
# config.json에서 설정 수정
```

### **3. 실행**
```bash
python dcf_analyzer.py
```

## 📈 DCF 모델 공식

### **내재가치 계산**
```
V = Σ(CFt / (1 + r)^t) + TV / (1 + r)^n

여기서:
- V: 내재가치
- CFt: t년차 현금흐름
- r: 할인율 (WACC)
- TV: 터미널 밸류
- n: 예측 기간
```

### **주요 지표**
- **FCF**: Free Cash Flow (잉여현금흐름)
- **WACC**: Weighted Average Cost of Capital
- **Terminal Growth Rate**: 터미널 성장률
- **Fair Value**: 공정가치 (내재가치)

## 🎯 사용 예시

### **주식 분석**
```python
from dcf_analyzer import DCFAnalyzer

analyzer = DCFAnalyzer("AAPL")
result = analyzer.analyze()
print(f"내재가치: ${result['fair_value']:.2f}")
print(f"현재가격: ${result['current_price']:.2f}")
print(f"할인율: {result['discount']:.1f}%")
```

### **포트폴리오 분석**
```python
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN"]
for stock in stocks:
    analyzer = DCFAnalyzer(stock)
    result = analyzer.analyze()
    print(f"{stock}: {result['recommendation']}")
```

## 📊 분석 결과

### **출력 정보**
- 내재가치 (Fair Value)
- 현재 주가
- 할인율 (Margin of Safety)
- 투자 추천 (Buy/Hold/Sell)
- 민감도 분석
- 시나리오 분석

### **시각화**
- DCF 모델 차트
- 현금흐름 예측 그래프
- 민감도 분석 차트
- 비교 분석 테이블

## 🔍 분석 프로세스

1. **데이터 수집**: 재무제표, 주가 데이터
2. **FCF 계산**: 잉여현금흐름 계산
3. **성장률 예측**: 과거 데이터 기반 예측
4. **WACC 계산**: 가중평균자본비용
5. **DCF 모델**: 내재가치 계산
6. **투자 판단**: 현재가 vs 내재가치

## ⚠️ 주의사항

- **예측의 한계**: 미래 현금흐름은 추정치
- **가정의 중요성**: 성장률, 할인율 등 가정이 결과에 큰 영향
- **시장 상황**: 거시경제 환경 고려 필요
- **투자 참고용**: 실제 투자 결정 시 추가 분석 필요

## 📚 참고 자료

- [DCF 모델 가이드](https://www.investopedia.com/terms/d/dcf.asp)
- [WACC 계산 방법](https://www.investopedia.com/terms/w/wacc.asp)
- [FCF 계산 방법](https://www.investopedia.com/terms/f/freecashflow.asp)

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

MIT License

