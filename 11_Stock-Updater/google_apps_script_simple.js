/**
 * Google Apps Script - 간소화된 버전 (최소 권한)
 * 스프레드시트에서 Extensions > Apps Script에 이 코드를 붙여넣으세요
 */

// 설정
const STOCK_SYMBOLS = [
  'SGOV', 'SPY', 'QQQ', 'TSLA', 'NVDA', 'SMH', 'SMCI', 'GOOG', 
  'META', 'AAPL', 'AMZN', 'MSFT', 'CRWD', 'LLY', 'CPNG', 
  'IONQ', 'QBTS', 'RGTI', 'CRWV', 'QUBT', 'PLTR', 'SOUN', 'BOTZ'
];

const SHEET_NAME = '7. Raw';

/**
 * 스프레드시트 열기 시 자동 실행
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('주식 업데이터')
    .addItem('주식 데이터 업데이트', 'updateStockData')
    .addToUi();
}

/**
 * 주식 데이터 업데이트 (Google Finance 함수 사용)
 */
function updateStockData() {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      SpreadsheetApp.getUi().alert('시트를 찾을 수 없습니다: ' + SHEET_NAME);
      return;
    }
    
    // 헤더 설정
    sheet.getRange(1, 1, 1, 3).setValues([['Symbol', 'Date', 'Close Price']]);
    
    // 주식 데이터 조회 및 업데이트
    const data = [];
    for (let i = 0; i < STOCK_SYMBOLS.length; i++) {
      const symbol = STOCK_SYMBOLS[i];
      try {
        // Google Finance 함수 사용 (권한 최소화)
        const price = getStockPriceSimple(symbol);
        if (price) {
          data.push([symbol, price.date, price.close]);
        } else {
          data.push([symbol, 'N/A', 'N/A']);
        }
      } catch (error) {
        console.error(`${symbol} 조회 오류:`, error);
        data.push([symbol, 'ERROR', 'N/A']);
      }
    }
    
    // 데이터 업데이트
    if (data.length > 0) {
      sheet.getRange(2, 1, data.length, 3).setValues(data);
      SpreadsheetApp.getUi().alert(`주식 데이터가 업데이트되었습니다. (${data.length}개)`);
    }
    
  } catch (error) {
    console.error('업데이트 오류:', error);
    SpreadsheetApp.getUi().alert('업데이트 중 오류가 발생했습니다: ' + error.message);
  }
}

/**
 * 주식 가격 조회 (Google Finance 함수 사용 - 권한 최소화)
 */
function getStockPriceSimple(symbol) {
  try {
    // Google Finance 함수 사용 (외부 API 호출 없음)
    const formula = `=GOOGLEFINANCE("${symbol}")`;
    const tempSheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const tempRange = tempSheet.getRange("Z1");
    
    // 임시로 값을 설정하고 읽기
    tempRange.setFormula(formula);
    SpreadsheetApp.flush(); // 변경사항 적용 대기
    
    const value = tempRange.getValue();
    const date = new Date().toISOString().split('T')[0];
    
    // 임시 값 제거
    tempRange.clear();
    
    if (value && typeof value === 'number') {
      return {
        symbol: symbol,
        date: date,
        close: value
      };
    }
    
    return null;
  } catch (error) {
    console.error(`${symbol} 가격 조회 오류:`, error);
    return null;
  }
}

/**
 * 테스트 함수
 */
function testUpdate() {
  console.log('테스트 시작...');
  updateStockData();
  console.log('테스트 완료');
}
