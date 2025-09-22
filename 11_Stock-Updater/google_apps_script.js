/**
 * Google Apps Script - 스프레드시트 열기 시 주식 데이터 업데이트
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
    .addItem('자동 업데이트 설정', 'setupAutoUpdate')
    .addToUi();
  
  // 자동 업데이트 체크
  checkAutoUpdate();
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
        const price = getStockPrice(symbol);
        if (price) {
          data.push([symbol, price.date, price.close]);
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
 * 주식 가격 조회 (Yahoo Finance API 대신 간단한 방법)
 */
function getStockPrice(symbol) {
  try {
    // Google Finance 함수 사용 (제한적이지만 무료)
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}`;
    const response = UrlFetchApp.fetch(url);
    const data = JSON.parse(response.getContentText());
    
    if (data.chart && data.chart.result && data.chart.result[0]) {
      const result = data.chart.result[0];
      const meta = result.meta;
      const timestamp = meta.regularMarketTime;
      const price = meta.regularMarketPrice;
      
      return {
        symbol: symbol,
        date: new Date(timestamp * 1000).toISOString().split('T')[0],
        close: price
      };
    }
    
    return null;
  } catch (error) {
    console.error(`${symbol} 가격 조회 오류:`, error);
    return null;
  }
}

/**
 * 자동 업데이트 설정
 */
function setupAutoUpdate() {
  // 5분마다 체크하는 트리거 설정
  ScriptApp.newTrigger('checkAutoUpdate')
    .timeBased()
    .everyMinutes(5)
    .create();
  
  SpreadsheetApp.getUi().alert('자동 업데이트가 설정되었습니다. (5분마다 체크)');
}

/**
 * 자동 업데이트 체크
 */
function checkAutoUpdate() {
  const lastUpdate = PropertiesService.getScriptProperties().getProperty('lastUpdate');
  const now = new Date();
  
  // 마지막 업데이트가 1시간 이상 지났으면 업데이트
  if (!lastUpdate || (now - new Date(lastUpdate)) > 60 * 60 * 1000) {
    updateStockData();
    PropertiesService.getScriptProperties().setProperty('lastUpdate', now.toString());
  }
}
