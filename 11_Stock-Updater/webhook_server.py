#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
웹훅 서버 - 스프레드시트 열기 감지 시 주식 데이터 업데이트
"""

from flask import Flask, request, jsonify
import json
import logging
from stock_updater import StockUpdater

# Flask 앱 설정
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# StockUpdater 인스턴스
updater = None

@app.route('/webhook/spreadsheet-opened', methods=['POST'])
def spreadsheet_opened():
    """스프레드시트 열기 웹훅"""
    try:
        data = request.get_json()
        logging.info(f"스프레드시트 열기 감지: {data}")
        
        # 주식 데이터 업데이트 실행
        updater.run_update()
        
        return jsonify({
            'status': 'success',
            'message': '주식 데이터가 업데이트되었습니다.'
        })
        
    except Exception as e:
        logging.error(f"웹훅 처리 오류: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """헬스 체크"""
    return jsonify({'status': 'healthy'})

def main():
    """메인 함수"""
    global updater
    
    try:
        # StockUpdater 초기화
        updater = StockUpdater()
        logging.info("웹훅 서버가 시작되었습니다.")
        
        # Flask 서버 실행
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except Exception as e:
        logging.error(f"서버 시작 오류: {e}")

if __name__ == "__main__":
    main()
