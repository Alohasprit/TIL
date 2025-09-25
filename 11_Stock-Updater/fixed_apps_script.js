/**
 * 수정된 Apps Script - UI 컨텍스트 문제 해결
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
  try {
    const ui = SpreadsheetApp.getUi();
    ui.createMenu('📊 주식 업데이터')
      .addItem('🔄 지금 업데이트', 'updateStockData')
      .addItem('🧪 테스트', 'testFunction')
      .addItem('🔍 디버깅', 'debugFunction')
      .addToUi();
    
    console.log('메뉴가 생성되었습니다.');
    
  } catch (error) {
    console.error('onOpen 오류:', error);
  }
}

/**
 * 테스트 함수 (UI 없이)
 */
function testFunction() {
  try {
    console.log('테스트 시작...');
    
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      console.error('시트를 찾을 수 없습니다: ' + SHEET_NAME);
      return;
    }
    
    // 간단한 테스트 값 입력
    sheet.getRange('A1').setValue('테스트');
    sheet.getRange('B1').setValue(new Date());
    sheet.getRange('C1').setValue(123.45);
    
    console.log('테스트 완료 - A1: 테스트, B1: 현재 날짜, C1: 123.45');
    
  } catch (error) {
    console.error('테스트 오류:', error);
  }
}

/**
 * 디버깅 함수
 */
function debugFunction() {
  try {
    console.log('디버깅 시작...');
    
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    const info = {
      spreadsheetId: spreadsheet.getId(),
      spreadsheetName: spreadsheet.getName(),
      sheetName: sheet ? sheet.getName() : 'NOT FOUND',
      sheetCount: spreadsheet.getSheets().length,
      allSheets: spreadsheet.getSheets().map(s => s.getName()),
      stockCount: STOCK_SYMBOLS.length
    };
    
    console.log('디버깅 정보:', info);
    
  } catch (error) {
    console.error('디버깅 오류:', error);
  }
}

/**
 * 주식 데이터 업데이트
 */
function updateStockData() {
  try {
    console.log('주식 데이터 업데이트 시작...');
    
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      console.error('시트를 찾을 수 없습니다: ' + SHEET_NAME);
      return;
    }
    
    // 헤더 설정
    sheet.getRange(1, 1, 1, 3).setValues([['Symbol', 'Date', 'Close Price']]);
    console.log('헤더 설정 완료');
    
    // 각 주식에 대해 Google Finance 함수 설정
    let successCount = 0;
    let errorCount = 0;
    
    for (let i = 0; i < STOCK_SYMBOLS.length; i++) {
      const symbol = STOCK_SYMBOLS[i];
      const row = i + 2;
      
      try {
        console.log(`${symbol} 설정 중... (${i + 1}/${STOCK_SYMBOLS.length})`);
        
        // A열에 심볼
        sheet.getRange(row, 1).setValue(symbol);
        
        // B열에 날짜
        sheet.getRange(row, 2).setValue(new Date().toISOString().split('T')[0]);
        
        // C열에 Google Finance 함수
        sheet.getRange(row, 3).setFormula(`=GOOGLEFINANCE("${symbol}")`);
        
        successCount++;
        console.log(`${symbol} 설정 완료`);
        
      } catch (error) {
        console.error(`${symbol} 설정 오류:`, error);
        sheet.getRange(row, 1, 1, 3).setValues([[symbol, 'ERROR', 'N/A']]);
        errorCount++;
      }
    }
    
    console.log(`업데이트 완료 - 성공: ${successCount}개, 오류: ${errorCount}개`);
    
  } catch (error) {
    console.error('업데이트 오류:', error);
  }
}

/**
 * 배치 업데이트 (더 안정적)
 */
function batchUpdateStockData() {
  try {
    console.log('배치 업데이트 시작...');
    
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getSheetByName(SHEET_NAME);
    
    if (!sheet) {
      console.error('시트를 찾을 수 없습니다: ' + SHEET_NAME);
      return;
    }
    
    // 헤더 설정
    sheet.getRange(1, 1, 1, 3).setValues([['Symbol', 'Date', 'Close Price']]);
    
    // 모든 주식 심볼을 한 번에 설정
    const symbols = STOCK_SYMBOLS.map(symbol => [symbol]);
    const dates = STOCK_SYMBOLS.map(() => [new Date().toISOString().split('T')[0]]);
    
    // A열에 심볼들 설정
    sheet.getRange(2, 1, STOCK_SYMBOLS.length, 1).setValues(symbols);
    
    // B열에 날짜들 설정
    sheet.getRange(2, 2, STOCK_SYMBOLS.length, 1).setValues(dates);
    
    // C열에 Google Finance 함수들 설정
    const formulas = STOCK_SYMBOLS.map(symbol => [`=GOOGLEFINANCE("${symbol}")`]);
    sheet.getRange(2, 3, STOCK_SYMBOLS.length, 1).setFormulas(formulas);
    
    console.log(`배치 업데이트 완료 - ${STOCK_SYMBOLS.length}개 주식 설정됨`);
    
  } catch (error) {
    console.error('배치 업데이트 오류:', error);
  }
}
