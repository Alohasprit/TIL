/**
 * 디버깅용 Google Apps Script
 * 메뉴가 보이지 않는 문제 해결
 */

// 설정
const STOCK_SYMBOLS = [
  'SGOV', 'SPY', 'QQQ', 'TSLA', 'NVDA', 'SMH', 'SMCI', 'GOOG', 
  'META', 'AAPL', 'AMZN', 'MSFT', 'CRWD', 'LLY', 'CPNG', 
  'IONQ', 'QBTS', 'RGTI', 'CRWV', 'QUBT', 'PLTR', 'SOUN', 'BOTZ'
];

const SHEET_NAME = '7. Raw';

/**
 * 스프레드시트 열기 시 자동 실행 (디버깅 버전)
 */
function onOpen() {
  try {
    console.log('onOpen 함수가 실행되었습니다!');
    
    const ui = SpreadsheetApp.getUi();
    console.log('UI 객체 생성 완료');
    
    // 메뉴 생성
    ui.createMenu('주식 업데이터')
      .addItem('주식 데이터 업데이트', 'updateStockData')
      .addItem('테스트 실행', 'testFunction')
      .addItem('디버그 정보', 'debugInfo')
      .addToUi();
    
    console.log('메뉴 생성 완료');
    
    // 알림 표시
    ui.alert('주식 업데이터 메뉴가 생성되었습니다!');
    
  } catch (error) {
    console.error('onOpen 함수 오류:', error);
    SpreadsheetApp.getUi().alert('오류 발생: ' + error.message);
  }
}

/**
 * 디버그 정보 표시
 */
function debugInfo() {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    let message = '디버그 정보:\n';
    message += `스프레드시트 ID: ${spreadsheet.getId()}\n`;
    message += `시트 이름: ${SHEET_NAME}\n`;
    message += `시트 존재 여부: ${sheet ? '예' : '아니오'}\n`;
    message += `주식 심볼 수: ${STOCK_SYMBOLS.length}\n`;
    
    SpreadsheetApp.getUi().alert(message);
    
  } catch (error) {
    SpreadsheetApp.getUi().alert('디버그 오류: ' + error.message);
  }
}

/**
 * 테스트 함수
 */
function testFunction() {
  try {
    SpreadsheetApp.getUi().alert('테스트 함수가 실행되었습니다!');
    console.log('테스트 함수 실행 완료');
  } catch (error) {
    SpreadsheetApp.getUi().alert('테스트 오류: ' + error.message);
  }
}

/**
 * 주식 데이터 업데이트
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
        // Google Finance 함수 사용
        const price = getStockPrice(symbol);
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
 * 주식 가격 조회
 */
function getStockPrice(symbol) {
  try {
    // Google Finance 함수 사용
    const formula = `=GOOGLEFINANCE("${symbol}")`;
    const tempSheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const tempRange = tempSheet.getRange("Z1");
    
    // 임시로 값을 설정하고 읽기
    tempRange.setFormula(formula);
    SpreadsheetApp.flush();
    
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
 * 수동으로 onOpen 함수 실행 (디버깅용)
 */
function manualOnOpen() {
  console.log('수동으로 onOpen 함수 실행');
  onOpen();
}
