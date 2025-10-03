#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
주식 DCF 분석기 - Python 버전
미국, 국내 주식의 DCF 분석 및 증권사 목표주가 수집
"""

import json
import logging
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DCFAnalyzer:
    """DCF 분석기 클래스"""
    
    def __init__(self, config_file: str = 'config.json'):
        """DCF 분석기 초기화"""
        self.config = self.load_config(config_file)
        self.dcf_settings = self.config.get('dcf_settings', {})
        
    def load_config(self, config_file: str) -> dict:
        """설정 파일 로드"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"설정 파일 {config_file}을 찾을 수 없습니다. 기본 설정을 사용합니다.")
            return self.get_default_config()
    
    def get_default_config(self) -> dict:
        """기본 설정 반환"""
        return {
            'dcf_settings': {
                'discount_rate': 0.10,
                'terminal_growth_rate': 0.03,
                'forecast_years': 5,
                'risk_free_rate': 0.04,
                'market_risk_premium': 0.06
            },
            'stocks': {
                'us_stocks': ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'],
                'kr_stocks': ['005930', '000660', '035420']
            }
        }
    
    def get_stock_data(self, symbol: str, market: str = 'US') -> Optional[dict]:
        """주식 데이터 조회"""
        try:
            if market == 'US':
                return self.get_us_stock_data(symbol)
            else:
                return self.get_kr_stock_data(symbol)
        except Exception as e:
            logger.error(f"{symbol} 데이터 조회 오류: {e}")
            return None
    
    def get_us_stock_data(self, symbol: str) -> Optional[dict]:
        """미국 주식 데이터 조회"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # 기본 정보
            data = {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'current_price': info.get('currentPrice', 0),
                'market_cap': info.get('marketCap', 0),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'currency': info.get('currency', 'USD')
            }
            
            # 재무 데이터
            financial_data = {
                'revenue': info.get('totalRevenue', 0),
                'net_income': info.get('netIncomeToCommon', 0),
                'free_cash_flow': info.get('freeCashflow', 0),
                'total_debt': info.get('totalDebt', 0),
                'cash': info.get('totalCash', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'pb_ratio': info.get('priceToBook', 0),
                'roe': info.get('returnOnEquity', 0),
                'debt_to_equity': info.get('debtToEquity', 0)
            }
            
            data.update(financial_data)
            return data
            
        except Exception as e:
            logger.error(f"미국 주식 {symbol} 데이터 조회 오류: {e}")
            return None
    
    def get_kr_stock_data(self, symbol: str) -> Optional[dict]:
        """국내 주식 데이터 조회 (네이버 금융 사용)"""
        try:
            # 네이버 금융에서 데이터 조회
            url = f"https://polling.finance.naver.com/api/realtime/domestic/stock/{symbol}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data and 'datas' in data:
                stock_data = data['datas'][0]
                return {
                    'symbol': symbol,
                    'name': stock_data.get('hts_kor_isnm', symbol),
                    'current_price': float(stock_data.get('stck_prpr', 0)),
                    'market_cap': stock_data.get('hts_avls', 0),
                    'currency': 'KRW',
                    'revenue': 0,  # 국내 주식은 별도 API 필요
                    'net_income': 0,
                    'free_cash_flow': 0,
                    'total_debt': 0,
                    'cash': 0,
                    'pe_ratio': 0,
                    'pb_ratio': 0,
                    'roe': 0,
                    'debt_to_equity': 0
                }
            return None
            
        except Exception as e:
            logger.error(f"국내 주식 {symbol} 데이터 조회 오류: {e}")
            return None
    
    def calculate_dcf(self, stock_data: dict) -> dict:
        """DCF 계산"""
        try:
            # 기본 설정
            discount_rate = self.dcf_settings.get('discount_rate', 0.10)
            terminal_growth = self.dcf_settings.get('terminal_growth_rate', 0.03)
            forecast_years = self.dcf_settings.get('forecast_years', 5)
            
            # FCF 추정 (간단한 방법)
            revenue = stock_data.get('revenue', 0)
            net_income = stock_data.get('net_income', 0)
            free_cash_flow = stock_data.get('free_cash_flow', 0)
            
            # FCF가 없으면 순이익의 80%로 추정
            if free_cash_flow == 0 and net_income > 0:
                estimated_fcf = net_income * 0.8
            else:
                estimated_fcf = free_cash_flow
            
            if estimated_fcf <= 0:
                return {'error': 'FCF 데이터가 없습니다.'}
            
            # 성장률 추정 (간단한 방법)
            growth_rate = 0.05  # 5% 성장률 가정
            
            # DCF 계산
            dcf_value = 0
            projected_fcf = estimated_fcf
            
            # 예측 기간 동안의 현금흐름 할인
            for year in range(1, forecast_years + 1):
                projected_fcf *= (1 + growth_rate)
                dcf_value += projected_fcf / ((1 + discount_rate) ** year)
            
            # 터미널 밸류 계산
            terminal_value = (projected_fcf * (1 + terminal_growth)) / (discount_rate - terminal_growth)
            discounted_terminal_value = terminal_value / ((1 + discount_rate) ** forecast_years)
            
            # 최종 내재가치
            fair_value = dcf_value + discounted_terminal_value
            
            # 할인율 계산
            current_price = stock_data.get('current_price', 0)
            if current_price > 0:
                discount = ((fair_value - current_price) / current_price) * 100
            else:
                discount = 0
            
            # 투자 추천
            if discount > 20:
                recommendation = 'Strong Buy'
            elif discount > 10:
                recommendation = 'Buy'
            elif discount < -20:
                recommendation = 'Sell'
            elif discount < -10:
                recommendation = 'Hold'
            else:
                recommendation = 'Hold'
            
            return {
                'fair_value': round(fair_value, 2),
                'current_price': current_price,
                'discount': round(discount, 2),
                'recommendation': recommendation,
                'dcf_value': round(dcf_value, 2),
                'terminal_value': round(discounted_terminal_value, 2),
                'growth_rate': growth_rate,
                'discount_rate': discount_rate
            }
            
        except Exception as e:
            logger.error(f"DCF 계산 오류: {e}")
            return {'error': str(e)}
    
    def analyze_stocks(self, symbols: List[str], market: str = 'US') -> pd.DataFrame:
        """주식 목록 DCF 분석"""
        results = []
        
        for symbol in symbols:
            logger.info(f"{symbol} DCF 분석 중...")
            
            # 주식 데이터 조회
            stock_data = self.get_stock_data(symbol, market)
            if not stock_data:
                continue
            
            # DCF 계산
            dcf_result = self.calculate_dcf(stock_data)
            if 'error' in dcf_result:
                logger.warning(f"{symbol} DCF 계산 실패: {dcf_result['error']}")
                continue
            
            # 결과 저장
            result = {
                'symbol': symbol,
                'name': stock_data.get('name', symbol),
                'current_price': stock_data.get('current_price', 0),
                'fair_value': dcf_result.get('fair_value', 0),
                'discount': dcf_result.get('discount', 0),
                'recommendation': dcf_result.get('recommendation', 'Hold'),
                'pe_ratio': stock_data.get('pe_ratio', 0),
                'pb_ratio': stock_data.get('pb_ratio', 0),
                'roe': stock_data.get('roe', 0),
                'market_cap': stock_data.get('market_cap', 0),
                'sector': stock_data.get('sector', ''),
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            results.append(result)
            logger.info(f"{symbol} 분석 완료: {dcf_result.get('recommendation', 'Hold')}")
        
        return pd.DataFrame(results)
    
    def get_target_prices(self, symbols: List[str], market: str = 'US') -> pd.DataFrame:
        """증권사 목표주가 수집 (모의 데이터)"""
        results = []
        
        # 모의 증권사 목표주가 데이터
        mock_targets = {
            'AAPL': [
                {'firm': 'JP Morgan', 'target_price': 200, 'rating': 'Overweight'},
                {'firm': 'Goldman Sachs', 'target_price': 195, 'rating': 'Buy'},
                {'firm': 'Morgan Stanley', 'target_price': 185, 'rating': 'Overweight'}
            ],
            'MSFT': [
                {'firm': 'JP Morgan', 'target_price': 450, 'rating': 'Overweight'},
                {'firm': 'Goldman Sachs', 'target_price': 440, 'rating': 'Buy'},
                {'firm': 'Morgan Stanley', 'target_price': 430, 'rating': 'Overweight'}
            ],
            '005930': [
                {'firm': '삼성증권', 'target_price': 85000, 'rating': 'Buy'},
                {'firm': 'KB증권', 'target_price': 82000, 'rating': 'Buy'},
                {'firm': 'NH투자증권', 'target_price': 80000, 'rating': 'Buy'}
            ]
        }
        
        for symbol in symbols:
            if symbol in mock_targets:
                for target in mock_targets[symbol]:
                    # 현재 주가 조회
                    stock_data = self.get_stock_data(symbol, market)
                    current_price = stock_data.get('current_price', 0) if stock_data else 0
                    
                    if current_price > 0:
                        target_return = ((target['target_price'] - current_price) / current_price) * 100
                    else:
                        target_return = 0
                    
                    result = {
                        'symbol': symbol,
                        'name': stock_data.get('name', symbol) if stock_data else symbol,
                        'current_price': current_price,
                        'target_price': target['target_price'],
                        'firm': target['firm'],
                        'rating': target['rating'],
                        'target_return': round(target_return, 2),
                        'collection_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    results.append(result)
        
        return pd.DataFrame(results)
    
    def export_to_excel(self, dcf_results: pd.DataFrame, target_results: pd.DataFrame, 
                       filename: str = 'stock_dcf_analysis.xlsx'):
        """Excel 파일로 내보내기"""
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # DCF 분석 결과
                dcf_results.to_excel(writer, sheet_name='DCF_Analysis', index=False)
                
                # 목표주가 결과
                target_results.to_excel(writer, sheet_name='Target_Prices', index=False)
                
                # 종합 분석
                summary_data = {
                    '분석 항목': ['총 분석 종목 수', 'DCF 분석 완료', '목표주가 수집 완료'],
                    '값': [len(dcf_results), len(dcf_results), len(target_results)],
                    '비고': ['DCF 모델', '내재가치 계산', '증권사 목표주가'],
                    '분석일시': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 3
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            logger.info(f"Excel 파일이 생성되었습니다: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Excel 파일 생성 오류: {e}")
            return False

def main():
    """메인 함수"""
    try:
        # DCF 분석기 초기화
        analyzer = DCFAnalyzer()
        
        # 미국 주식 분석
        logger.info("미국 주식 DCF 분석 시작...")
        us_stocks = analyzer.config.get('stocks', {}).get('us_stocks', ['AAPL', 'MSFT', 'GOOGL'])
        us_dcf_results = analyzer.analyze_stocks(us_stocks, 'US')
        
        # 국내 주식 분석
        logger.info("국내 주식 DCF 분석 시작...")
        kr_stocks = analyzer.config.get('stocks', {}).get('kr_stocks', ['005930', '000660'])
        kr_dcf_results = analyzer.analyze_stocks(kr_stocks, 'KR')
        
        # 목표주가 수집
        logger.info("증권사 목표주가 수집 시작...")
        all_stocks = us_stocks + kr_stocks
        target_results = analyzer.get_target_prices(all_stocks)
        
        # 결과 합치기
        all_dcf_results = pd.concat([us_dcf_results, kr_dcf_results], ignore_index=True)
        
        # Excel 파일로 내보내기
        filename = f"stock_dcf_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        analyzer.export_to_excel(all_dcf_results, target_results, filename)
        
        # 결과 출력
        print("\n=== DCF 분석 결과 ===")
        print(all_dcf_results[['symbol', 'name', 'current_price', 'fair_value', 'discount', 'recommendation']])
        
        print("\n=== 목표주가 결과 ===")
        print(target_results[['symbol', 'name', 'current_price', 'target_price', 'firm', 'rating']])
        
        logger.info("DCF 분석이 완료되었습니다.")
        
    except Exception as e:
        logger.error(f"메인 실행 오류: {e}")

if __name__ == "__main__":
    main()

