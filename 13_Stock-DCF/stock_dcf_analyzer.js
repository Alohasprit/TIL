/**
 * 주식 DCF 분석 및 증권사 목표주가 수집 Google Apps Script
 * 미국, 국내 주식의 적정주가를 DCF 방식으로 계산하고 증권사 목표주가를 수집합니다.
 */

// 설정
const CONFIG = {
  // 분석할 주식 목록 (미국 + 국내)
  US_STOCKS: [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'NFLX',
    'AMD', 'INTC', 'CRM', 'ADBE', 'PYPL', 'NFLX', 'UBER', 'SQ'
  ],
  KR_STOCKS: [
    '005930', '000660', '035420', '207940', '006400', '035720', '051910', '068270',
    '323410', '005380', '000270', '012330', '066570', '003550', '017670', '036570'
  ],
  
  // 시트 설정
  SHEET_NAMES: {
    US_DCF: '미국_DCF분석',
    KR_DCF: '국내_DCF분석',
    US_TARGET: '미국_목표주가',
    KR_TARGET: '국내_목표주가',
    SUMMARY: '종합분석'
  },
  
  // DCF 모델 설정
  DCF_SETTINGS: {
    DISCOUNT_RATE: 0.10,        // 할인율 10%
    TERMINAL_GROWTH: 0.03,      // 터미널 성장률 3%
    FORECAST_YEARS: 5,          // 예측 기간 5년
    RISK_FREE_RATE: 0.04        // 무위험 수익률 4%
  }
};

/**
 * 스프레드시트 열기 시 자동 실행
 */
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('주식 DCF 분석기')
    .addItem('미국 주식 DCF 분석', 'analyzeUSStocks')
    .addItem('국내 주식 DCF 분석', 'analyzeKRStocks')
    .addItem('증권사 목표주가 수집', 'collectTargetPrices')
    .addItem('종합 분석 리포트', 'generateSummaryReport')
    .addItem('데이터 초기화', 'initializeSheets')
    .addToUi();
}

/**
 * 시트 초기화
 */
function initializeSheets() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  
  // 시트 생성 또는 초기화
  Object.values(CONFIG.SHEET_NAMES).forEach(sheetName => {
    let sheet = spreadsheet.getSheetByName(sheetName);
    if (!sheet) {
      sheet = spreadsheet.insertSheet(sheetName);
    }
    sheet.clear();
  });
  
  // 미국 DCF 분석 시트 헤더
  const usDcfSheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAMES.US_DCF);
  usDcfSheet.getRange(1, 1, 1, 10).setValues([[
    '종목코드', '종목명', '현재주가', 'DCF 적정주가', '할인율(%)', 
    '투자추천', 'P/E', 'P/B', 'ROE(%)', '분석일시'
  ]]);
  
  // 국내 DCF 분석 시트 헤더
  const krDcfSheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAMES.KR_DCF);
  krDcfSheet.getRange(1, 1, 1, 10).setValues([[
    '종목코드', '종목명', '현재주가', 'DCF 적정주가', '할인율(%)', 
    '투자추천', 'P/E', 'P/B', 'ROE(%)', '분석일시'
  ]]);
  
  // 증권사 목표주가 시트 헤더
  const usTargetSheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAMES.US_TARGET);
  usTargetSheet.getRange(1, 1, 1, 8).setValues([[
    '종목코드', '종목명', '현재주가', '목표주가', '증권사', '투자의견', '목표수익률(%)', '수집일시'
  ]]);
  
  const krTargetSheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAMES.KR_TARGET);
  krTargetSheet.getRange(1, 1, 1, 8).setValues([[
    '종목코드', '종목명', '현재주가', '목표주가', '증권사', '투자의견', '목표수익률(%)', '수집일시'
  ]]);
  
  SpreadsheetApp.getUi().alert('시트가 초기화되었습니다.');
}

/**
 * 미국 주식 DCF 분석
 */
function analyzeUSStocks() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAMES.US_DCF);
  
  SpreadsheetApp.getUi().alert('미국 주식 DCF 분석을 시작합니다...');
  
  const results = [];
  CONFIG.US_STOCKS.forEach((symbol, index) => {
    try {
      const analysis = performDCFAnalysis(symbol, 'US');
      if (analysis) {
        results.push([
          symbol,
          analysis.companyName,
          analysis.currentPrice,
          analysis.fairValue,
          analysis.discount,
          analysis.recommendation,
          analysis.pe,
          analysis.pb,
          analysis.roe,
          new Date()
        ]);
      }
    } catch (error) {
      console.error(`${symbol} 분석 오류:`, error);
    }
  });
  
  if (results.length > 0) {
    sheet.getRange(2, 1, results.length, 10).setValues(results);
    SpreadsheetApp.getUi().alert(`미국 주식 ${results.length}개 분석 완료`);
  }
}

/**
 * 국내 주식 DCF 분석
 */
function analyzeKRStocks() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAMES.KR_DCF);
  
  SpreadsheetApp.getUi().alert('국내 주식 DCF 분석을 시작합니다...');
  
  const results = [];
  CONFIG.KR_STOCKS.forEach((symbol, index) => {
    try {
      const analysis = performDCFAnalysis(symbol, 'KR');
      if (analysis) {
        results.push([
          symbol,
          analysis.companyName,
          analysis.currentPrice,
          analysis.fairValue,
          analysis.discount,
          analysis.recommendation,
          analysis.pe,
          analysis.pb,
          analysis.roe,
          new Date()
        ]);
      }
    } catch (error) {
      console.error(`${symbol} 분석 오류:`, error);
    }
  });
  
  if (results.length > 0) {
    sheet.getRange(2, 1, results.length, 10).setValues(results);
    SpreadsheetApp.getUi().alert(`국내 주식 ${results.length}개 분석 완료`);
  }
}

/**
 * DCF 분석 수행
 */
function performDCFAnalysis(symbol, market) {
  try {
    // 주가 데이터 조회
    const priceData = getStockPrice(symbol, market);
    if (!priceData) return null;
    
    // 재무 데이터 조회
    const financialData = getFinancialData(symbol, market);
    if (!financialData) return null;
    
    // DCF 계산
    const dcfResult = calculateDCF(financialData, priceData);
    
    return {
      companyName: financialData.companyName || symbol,
      currentPrice: priceData.price,
      fairValue: dcfResult.fairValue,
      discount: dcfResult.discount,
      recommendation: dcfResult.recommendation,
      pe: financialData.pe || 'N/A',
      pb: financialData.pb || 'N/A',
      roe: financialData.roe || 'N/A'
    };
    
  } catch (error) {
    console.error(`DCF 분석 오류 (${symbol}):`, error);
    return null;
  }
}

/**
 * 주가 데이터 조회
 */
function getStockPrice(symbol, market) {
  try {
    if (market === 'US') {
      // 미국 주식: Yahoo Finance 사용
      const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}`;
      const response = UrlFetchApp.fetch(url);
      const data = JSON.parse(response.getContentText());
      
      if (data.chart && data.chart.result && data.chart.result[0]) {
        const result = data.chart.result[0];
        const meta = result.meta;
        return {
          price: meta.regularMarketPrice,
          currency: meta.currency,
          marketCap: meta.marketCap
        };
      }
    } else {
      // 국내 주식: 한국투자증권 API 또는 네이버 금융 사용
      const url = `https://polling.finance.naver.com/api/realtime/domestic/stock/${symbol}`;
      const response = UrlFetchApp.fetch(url);
      const data = JSON.parse(response.getContentText());
      
      if (data && data.datas) {
        const stockData = data.datas[0];
        return {
          price: stockData.stck_prpr,
          currency: 'KRW',
          marketCap: stockData.hts_avls
        };
      }
    }
    
    return null;
  } catch (error) {
    console.error(`주가 조회 오류 (${symbol}):`, error);
    return null;
  }
}

/**
 * 재무 데이터 조회
 */
function getFinancialData(symbol, market) {
  try {
    if (market === 'US') {
      // 미국 주식: Alpha Vantage API 또는 Yahoo Finance
      const url = `https://query1.finance.yahoo.com/v10/finance/quoteSummary/${symbol}?modules=financialData,defaultKeyStatistics`;
      const response = UrlFetchApp.fetch(url);
      const data = JSON.parse(response.getContentText());
      
      if (data.quoteSummary && data.quoteSummary.result) {
        const result = data.quoteSummary.result[0];
        const financialData = result.financialData;
        const keyStats = result.defaultKeyStatistics;
        
        return {
          companyName: financialData.longName,
          revenue: financialData.totalRevenue?.raw || 0,
          netIncome: financialData.netIncomeToCommon?.raw || 0,
          freeCashFlow: financialData.freeCashflow?.raw || 0,
          totalDebt: financialData.totalDebt?.raw || 0,
          cash: financialData.totalCash?.raw || 0,
          pe: financialData.trailingPE || 0,
          pb: keyStats.priceToBook || 0,
          roe: financialData.returnOnEquity || 0
        };
      }
    } else {
      // 국내 주식: 한국투자증권 API 또는 DART API
      // 실제 구현에서는 한국투자증권 API 사용
      return {
        companyName: symbol,
        revenue: 0,
        netIncome: 0,
        freeCashFlow: 0,
        totalDebt: 0,
        cash: 0,
        pe: 0,
        pb: 0,
        roe: 0
      };
    }
    
    return null;
  } catch (error) {
    console.error(`재무 데이터 조회 오류 (${symbol}):`, error);
    return null;
  }
}

/**
 * DCF 계산
 */
function calculateDCF(financialData, priceData) {
  try {
    const { revenue, netIncome, freeCashFlow, totalDebt, cash } = financialData;
    const currentPrice = priceData.price;
    
    // FCF 계산 (간단한 추정)
    const estimatedFCF = freeCashFlow || (netIncome * 0.8); // 순이익의 80%를 FCF로 추정
    
    // 성장률 추정 (과거 데이터 기반, 여기서는 5%로 가정)
    const growthRate = 0.05;
    
    // WACC 계산 (간단한 추정)
    const wacc = CONFIG.DCF_SETTINGS.DISCOUNT_RATE;
    
    // DCF 계산
    let dcfValue = 0;
    let projectedFCF = estimatedFCF;
    
    // 예측 기간 동안의 현금흐름 할인
    for (let year = 1; year <= CONFIG.DCF_SETTINGS.FORECAST_YEARS; year++) {
      projectedFCF *= (1 + growthRate);
      dcfValue += projectedFCF / Math.pow(1 + wacc, year);
    }
    
    // 터미널 밸류 계산
    const terminalValue = (projectedFCF * (1 + CONFIG.DCF_SETTINGS.TERMINAL_GROWTH)) / 
                         (wacc - CONFIG.DCF_SETTINGS.TERMINAL_GROWTH);
    const discountedTerminalValue = terminalValue / Math.pow(1 + wacc, CONFIG.DCF_SETTINGS.FORECAST_YEARS);
    
    // 최종 내재가치
    const fairValue = dcfValue + discountedTerminalValue;
    
    // 할인율 계산
    const discount = ((fairValue - currentPrice) / currentPrice) * 100;
    
    // 투자 추천
    let recommendation = 'Hold';
    if (discount > 20) recommendation = 'Strong Buy';
    else if (discount > 10) recommendation = 'Buy';
    else if (discount < -20) recommendation = 'Sell';
    else if (discount < -10) recommendation = 'Hold';
    
    return {
      fairValue: Math.round(fairValue * 100) / 100,
      discount: Math.round(discount * 100) / 100,
      recommendation: recommendation
    };
    
  } catch (error) {
    console.error('DCF 계산 오류:', error);
    return null;
  }
}

/**
 * 증권사 목표주가 수집
 */
function collectTargetPrices() {
  SpreadsheetApp.getUi().alert('증권사 목표주가 수집을 시작합니다...');
  
  // 미국 주식 목표주가 수집
  collectUSTargetPrices();
  
  // 국내 주식 목표주가 수집
  collectKRTargetPrices();
  
  SpreadsheetApp.getUi().alert('증권사 목표주가 수집이 완료되었습니다.');
}

/**
 * 미국 주식 목표주가 수집
 */
function collectUSTargetPrices() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAMES.US_TARGET);
  
  const results = [];
  
  // 주요 증권사 목표주가 (실제로는 증권사 API 사용)
  const targetPrices = {
    'AAPL': [
      { price: 200, firm: 'JP Morgan', rating: 'Overweight' },
      { price: 195, firm: 'Goldman Sachs', rating: 'Buy' },
      { price: 185, firm: 'Morgan Stanley', rating: 'Overweight' }
    ],
    'MSFT': [
      { price: 450, firm: 'JP Morgan', rating: 'Overweight' },
      { price: 440, firm: 'Goldman Sachs', rating: 'Buy' },
      { price: 430, firm: 'Morgan Stanley', rating: 'Overweight' }
    ]
    // 다른 주식들도 추가...
  };
  
  CONFIG.US_STOCKS.forEach(symbol => {
    if (targetPrices[symbol]) {
      targetPrices[symbol].forEach(target => {
        const currentPrice = getCurrentPrice(symbol);
        const targetReturn = ((target.price - currentPrice) / currentPrice) * 100;
        
        results.push([
          symbol,
          symbol,
          currentPrice,
          target.price,
          target.firm,
          target.rating,
          Math.round(targetReturn * 100) / 100,
          new Date()
        ]);
      });
    }
  });
  
  if (results.length > 0) {
    sheet.getRange(2, 1, results.length, 8).setValues(results);
  }
}

/**
 * 국내 주식 목표주가 수집
 */
function collectKRTargetPrices() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAMES.KR_TARGET);
  
  const results = [];
  
  // 주요 증권사 목표주가 (실제로는 증권사 API 사용)
  const targetPrices = {
    '005930': [
      { price: 85000, firm: '삼성증권', rating: 'Buy' },
      { price: 82000, firm: 'KB증권', rating: 'Buy' },
      { price: 80000, firm: 'NH투자증권', rating: 'Buy' }
    ],
    '000660': [
      { price: 45000, firm: '삼성증권', rating: 'Buy' },
      { price: 43000, firm: 'KB증권', rating: 'Buy' },
      { price: 42000, firm: 'NH투자증권', rating: 'Buy' }
    ]
    // 다른 주식들도 추가...
  };
  
  CONFIG.KR_STOCKS.forEach(symbol => {
    if (targetPrices[symbol]) {
      targetPrices[symbol].forEach(target => {
        const currentPrice = getCurrentPrice(symbol);
        const targetReturn = ((target.price - currentPrice) / currentPrice) * 100;
        
        results.push([
          symbol,
          symbol,
          currentPrice,
          target.price,
          target.firm,
          target.rating,
          Math.round(targetReturn * 100) / 100,
          new Date()
        ]);
      });
    }
  });
  
  if (results.length > 0) {
    sheet.getRange(2, 1, results.length, 8).setValues(results);
  }
}

/**
 * 현재 주가 조회
 */
function getCurrentPrice(symbol) {
  try {
    const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}`;
    const response = UrlFetchApp.fetch(url);
    const data = JSON.parse(response.getContentText());
    
    if (data.chart && data.chart.result && data.chart.result[0]) {
      return data.chart.result[0].meta.regularMarketPrice;
    }
    return 0;
  } catch (error) {
    console.error(`주가 조회 오류 (${symbol}):`, error);
    return 0;
  }
}

/**
 * 종합 분석 리포트 생성
 */
function generateSummaryReport() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName(CONFIG.SHEET_NAMES.SUMMARY);
  
  // 종합 분석 리포트 헤더
  sheet.getRange(1, 1, 1, 6).setValues([[
    '분석 항목', '미국 주식', '국내 주식', '전체', '비고', '분석일시'
  ]]);
  
  // 분석 결과 요약
  const summaryData = [
    ['총 분석 종목 수', CONFIG.US_STOCKS.length, CONFIG.KR_STOCKS.length, 
     CONFIG.US_STOCKS.length + CONFIG.KR_STOCKS.length, 'DCF 분석', new Date()],
    ['목표주가 수집', '완료', '완료', '완료', '증권사 목표주가', new Date()],
    ['투자 추천', 'Buy/Hold/Sell', 'Buy/Hold/Sell', 'Buy/Hold/Sell', 'DCF 기반', new Date()]
  ];
  
  sheet.getRange(2, 1, summaryData.length, 6).setValues(summaryData);
  
  SpreadsheetApp.getUi().alert('종합 분석 리포트가 생성되었습니다.');
}

/**
 * 테스트 함수
 */
function testDCFAnalysis() {
  console.log('DCF 분석 테스트 시작...');
  
  // AAPL 주식으로 테스트
  const result = performDCFAnalysis('AAPL', 'US');
  console.log('AAPL DCF 분석 결과:', result);
  
  SpreadsheetApp.getUi().alert('테스트 완료! 로그를 확인하세요.');
}

