#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
미국 주식 전날 종가 자동 업데이트 스크립트
매일 오전 8시에 실행되어 스프레드시트를 업데이트합니다.
"""

import os
import json
import logging
import schedule
import time
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('stock_updater.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class StockUpdater:
    def __init__(self, config_file='config.json'):
        """주식 업데이터 초기화"""
        self.config = self.load_config(config_file)
        self.sheets_service = self.setup_google_sheets()
        
    def load_config(self, config_file):
        """설정 파일 로드"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info("설정 파일이 성공적으로 로드되었습니다.")
            return config
        except FileNotFoundError:
            logger.error(f"설정 파일 {config_file}을 찾을 수 없습니다.")
            raise
        except json.JSONDecodeError:
            logger.error("설정 파일 형식이 올바르지 않습니다.")
            raise
    
    def setup_google_sheets(self):
        """Google Sheets API 설정"""
        try:
            # 서비스 계정 키 파일 경로
            credentials = Credentials.from_service_account_file(
                self.config['google_credentials_file'],
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            service = build('sheets', 'v4', credentials=credentials)
            logger.info("Google Sheets API가 성공적으로 설정되었습니다.")
            return service
        except Exception as e:
            logger.error(f"Google Sheets API 설정 중 오류 발생: {e}")
            raise
    
    def get_stock_price(self, symbol):
        """주식 가격 조회"""
        try:
            ticker = yf.Ticker(symbol)
            # 전날 데이터 조회 (최근 거래일)
            hist = ticker.history(period="5d")  # 최근 5일 데이터 조회
            
            if hist.empty:
                logger.warning(f"{symbol}에 대한 데이터를 찾을 수 없습니다.")
                return None
            
            # 가장 최근 거래일의 종가
            latest_close = hist['Close'].iloc[-1]
            latest_date = hist.index[-1].strftime('%Y-%m-%d')
            
            logger.info(f"{symbol}: {latest_date} 종가 ${latest_close:.2f}")
            return {
                'symbol': symbol,
                'date': latest_date,
                'close_price': round(latest_close, 2)
            }
        except Exception as e:
            logger.error(f"{symbol} 가격 조회 중 오류 발생: {e}")
            return None
    
    def update_spreadsheet(self, stock_data):
        """스프레드시트 업데이트"""
        try:
            spreadsheet_id = self.config['spreadsheet_id']
            sheet_name = self.config['sheet_name']
            
            # 업데이트할 데이터 준비
            values = []
            for data in stock_data:
                if data:
                    values.append([data['symbol'], data['date'], data['close_price']])
            
            if not values:
                logger.warning("업데이트할 데이터가 없습니다.")
                return
            
            # 헤더 추가 (첫 번째 행)
            header = [['Symbol', 'Date', 'Close Price']]
            all_values = header + values
            
            # 스프레드시트 업데이트
            range_name = f"{sheet_name}!A1:C{len(all_values)}"
            
            body = {
                'values': all_values
            }
            
            result = self.sheets_service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            logger.info(f"스프레드시트가 성공적으로 업데이트되었습니다. {result.get('updatedCells')}개 셀이 업데이트됨")
            
        except HttpError as e:
            logger.error(f"스프레드시트 업데이트 중 오류 발생: {e}")
        except Exception as e:
            logger.error(f"예상치 못한 오류 발생: {e}")
    
    def run_update(self):
        """주식 데이터 업데이트 실행"""
        logger.info("주식 데이터 업데이트를 시작합니다...")
        
        stock_data = []
        for symbol in self.config['stock_symbols']:
            logger.info(f"{symbol} 데이터를 조회 중...")
            data = self.get_stock_price(symbol)
            stock_data.append(data)
        
        # 스프레드시트 업데이트
        self.update_spreadsheet(stock_data)
        logger.info("주식 데이터 업데이트가 완료되었습니다.")
    
    def start_scheduler(self):
        """스케줄러 시작"""
        # 매일 오전 8시에 실행
        schedule.every().day.at("08:00").do(self.run_update)
        
        logger.info("스케줄러가 시작되었습니다. 매일 오전 8시에 실행됩니다.")
        logger.info("프로그램을 종료하려면 Ctrl+C를 누르세요.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # 1분마다 체크
        except KeyboardInterrupt:
            logger.info("프로그램이 사용자에 의해 종료되었습니다.")

def main():
    """메인 함수"""
    try:
        updater = StockUpdater()
        updater.start_scheduler()
    except Exception as e:
        logger.error(f"프로그램 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
