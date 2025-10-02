/**
 * 한국 아파트 매매, 전세, 월세 매물 및 실거래가 정보를 스프레드시트에 가져오는 Apps Script
 * 공공데이터포털의 부동산 실거래가 API를 활용
 * 
 * 사용 전 준비사항:
 * 1. 공공데이터포털(https://www.data.go.kr/)에서 API 키 발급
 * 2. 아래 API_KEY 변수에 발급받은 키 입력
 * 3. 원하는 지역 코드(LAWD_CD) 설정
 */

// ===== 설정 변수 =====
const API_KEY = 'YOUR_API_KEY_HERE'; // 공공데이터포털에서 발급받은 API 키를 입력하세요
const REGION_CODE = '11110'; // 지역 코드 (예: 11110 = 서울특별시 종로구)
const DEAL_YEAR = '2024'; // 조회할 연도
const DEAL_MONTH = '12'; // 조회할 월

// API 엔드포인트
const API_ENDPOINTS = {
  APT_TRADE: 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade', // 아파트 매매
  APT_RENT: 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent', // 아파트 전세
  OFFICE_TRADE: 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiTrade', // 오피스텔 매매
  OFFICE_RENT: 'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiRent' // 오피스텔 전세
};

/**
 * 메인 실행 함수 - 모든 부동산 데이터를 수집하여 스프레드시트에 저장
 */
function fetchAllRealEstateData() {
  try {
    console.log('부동산 데이터 수집을 시작합니다...');
    
    // 스프레드시트 초기화
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    clearAllSheets(spreadsheet);
    
    // 1. 아파트 매매 데이터 수집
    console.log('아파트 매매 데이터를 수집합니다...');
    const aptTradeData = fetchAptTradeData();
    if (aptTradeData && aptTradeData.length > 0) {
      writeToSheet(spreadsheet, '아파트_매매', aptTradeData, getAptTradeHeaders());
    }
    
    // 2. 아파트 전세 데이터 수집
    console.log('아파트 전세 데이터를 수집합니다...');
    const aptRentData = fetchAptRentData();
    if (aptRentData && aptRentData.length > 0) {
      writeToSheet(spreadsheet, '아파트_전세', aptRentData, getAptRentHeaders());
    }
    
    // 3. 오피스텔 매매 데이터 수집
    console.log('오피스텔 매매 데이터를 수집합니다...');
    const officeTradeData = fetchOfficeTradeData();
    if (officeTradeData && officeTradeData.length > 0) {
      writeToSheet(spreadsheet, '오피스텔_매매', officeTradeData, getOfficeTradeHeaders());
    }
    
    // 4. 오피스텔 전세 데이터 수집
    console.log('오피스텔 전세 데이터를 수집합니다...');
    const officeRentData = fetchOfficeRentData();
    if (officeRentData && officeRentData.length > 0) {
      writeToSheet(spreadsheet, '오피스텔_전세', officeRentData, getOfficeRentHeaders());
    }
    
    console.log('모든 부동산 데이터 수집이 완료되었습니다.');
    
  } catch (error) {
    console.error('데이터 수집 중 오류가 발생했습니다:', error);
    throw error;
  }
}

/**
 * 아파트 매매 데이터 수집
 */
function fetchAptTradeData() {
  const url = buildApiUrl(API_ENDPOINTS.APT_TRADE, {
    LAWD_CD: REGION_CODE,
    DEAL_YMD: DEAL_YEAR + DEAL_MONTH,
    serviceKey: API_KEY
  });
  
  return fetchRealEstateData(url, '아파트매매');
}

/**
 * 아파트 전세 데이터 수집
 */
function fetchAptRentData() {
  const url = buildApiUrl(API_ENDPOINTS.APT_RENT, {
    LAWD_CD: REGION_CODE,
    DEAL_YMD: DEAL_YEAR + DEAL_MONTH,
    serviceKey: API_KEY
  });
  
  return fetchRealEstateData(url, '아파트전세');
}

/**
 * 오피스텔 매매 데이터 수집
 */
function fetchOfficeTradeData() {
  const url = buildApiUrl(API_ENDPOINTS.OFFICE_TRADE, {
    LAWD_CD: REGION_CODE,
    DEAL_YMD: DEAL_YEAR + DEAL_MONTH,
    serviceKey: API_KEY
  });
  
  return fetchRealEstateData(url, '오피스텔매매');
}

/**
 * 오피스텔 전세 데이터 수집
 */
function fetchOfficeRentData() {
  const url = buildApiUrl(API_ENDPOINTS.OFFICE_RENT, {
    LAWD_CD: REGION_CODE,
    DEAL_YMD: DEAL_YEAR + DEAL_MONTH,
    serviceKey: API_KEY
  });
  
  return fetchRealEstateData(url, '오피스텔전세');
}

/**
 * API URL 생성
 */
function buildApiUrl(endpoint, params) {
  const queryString = Object.keys(params)
    .map(key => `${key}=${encodeURIComponent(params[key])}`)
    .join('&');
  
  return `${endpoint}?${queryString}`;
}

/**
 * 부동산 데이터 API 호출 및 파싱
 */
function fetchRealEstateData(url, dataType) {
  try {
    console.log(`${dataType} 데이터를 가져오는 중... URL: ${url}`);
    
    const response = UrlFetchApp.fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/xml'
      }
    });
    
    const xmlContent = response.getContentText();
    console.log(`${dataType} API 응답 받음`);
    
    // XML 파싱
    const document = XmlService.parse(xmlContent);
    const root = document.getRootElement();
    
    // 에러 체크
    const resultCode = root.getChild('header')?.getChild('resultCode')?.getText();
    if (resultCode !== '00') {
      const resultMsg = root.getChild('header')?.getChild('resultMsg')?.getText();
      console.error(`API 오류: ${resultMsg}`);
      return [];
    }
    
    const items = root.getChild('body')?.getChild('items')?.getChildren('item');
    if (!items || items.length === 0) {
      console.log(`${dataType} 데이터가 없습니다.`);
      return [];
    }
    
    console.log(`${dataType} ${items.length}건의 데이터를 찾았습니다.`);
    
    // 데이터 변환
    const data = items.map(item => parseRealEstateItem(item, dataType));
    return data;
    
  } catch (error) {
    console.error(`${dataType} 데이터 수집 중 오류:`, error);
    return [];
  }
}

/**
 * XML 아이템을 객체로 파싱
 */
function parseRealEstateItem(item, dataType) {
  const getText = (childName) => {
    const child = item.getChild(childName);
    return child ? child.getText() : '';
  };
  
  const baseData = {
    거래일자: getText('년') + '-' + getText('월').padStart(2, '0') + '-' + getText('일').padStart(2, '0'),
    법정동: getText('법정동'),
    아파트명: getText('아파트'),
    전용면적: getText('전용면적'),
    층: getText('층'),
    건축년도: getText('건축년도')
  };
  
  if (dataType.includes('매매')) {
    return {
      ...baseData,
      거래금액: getText('거래금액'),
      거래유형: '매매'
    };
  } else {
    return {
      ...baseData,
      보증금: getText('보증금'),
      월세: getText('월세'),
      거래유형: '전세'
    };
  }
}

/**
 * 스프레드시트 초기화
 */
function clearAllSheets(spreadsheet) {
  const sheets = spreadsheet.getSheets();
  sheets.forEach(sheet => {
    if (sheet.getName() !== '설정') {
      sheet.clear();
    }
  });
}

/**
 * 데이터를 스프레드시트에 작성
 */
function writeToSheet(spreadsheet, sheetName, data, headers) {
  let sheet = spreadsheet.getSheetByName(sheetName);
  
  if (!sheet) {
    sheet = spreadsheet.insertSheet(sheetName);
  }
  
  // 헤더 작성
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  
  // 데이터 작성
  if (data.length > 0) {
    const values = data.map(row => headers.map(header => row[header] || ''));
    sheet.getRange(2, 1, values.length, headers.length).setValues(values);
    
    // 헤더 스타일링
    const headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setBackground('#4285f4');
    headerRange.setFontColor('white');
    headerRange.setFontWeight('bold');
    
    // 자동 열 너비 조정
    sheet.autoResizeColumns(1, headers.length);
  }
  
  console.log(`${sheetName} 시트에 ${data.length}건의 데이터를 저장했습니다.`);
}

/**
 * 아파트 매매 헤더
 */
function getAptTradeHeaders() {
  return ['거래일자', '법정동', '아파트명', '전용면적', '층', '건축년도', '거래금액', '거래유형'];
}

/**
 * 아파트 전세 헤더
 */
function getAptRentHeaders() {
  return ['거래일자', '법정동', '아파트명', '전용면적', '층', '건축년도', '보증금', '월세', '거래유형'];
}

/**
 * 오피스텔 매매 헤더
 */
function getOfficeTradeHeaders() {
  return ['거래일자', '법정동', '아파트명', '전용면적', '층', '건축년도', '거래금액', '거래유형'];
}

/**
 * 오피스텔 전세 헤더
 */
function getOfficeRentHeaders() {
  return ['거래일자', '법정동', '아파트명', '전용면적', '층', '건축년도', '보증금', '월세', '거래유형'];
}

/**
 * 특정 지역의 데이터만 수집하는 함수
 */
function fetchDataByRegion(regionCode, year, month) {
  const originalRegion = REGION_CODE;
  const originalYear = DEAL_YEAR;
  const originalMonth = DEAL_MONTH;
  
  // 설정 변경
  REGION_CODE = regionCode;
  DEAL_YEAR = year;
  DEAL_MONTH = month;
  
  try {
    fetchAllRealEstateData();
  } finally {
    // 원래 설정으로 복원
    REGION_CODE = originalRegion;
    DEAL_YEAR = originalYear;
    DEAL_MONTH = originalMonth;
  }
}

/**
 * 자동 실행을 위한 트리거 설정 함수
 */
function setupTrigger() {
  // 기존 트리거 삭제
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'fetchAllRealEstateData') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
  
  // 매일 오전 9시에 실행되는 트리거 생성
  ScriptApp.newTrigger('fetchAllRealEstateData')
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();
  
  console.log('자동 실행 트리거가 설정되었습니다. 매일 오전 9시에 실행됩니다.');
}

/**
 * 트리거 삭제 함수
 */
function deleteTrigger() {
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => {
    if (trigger.getHandlerFunction() === 'fetchAllRealEstateData') {
      ScriptApp.deleteTrigger(trigger);
    }
  });
  console.log('자동 실행 트리거가 삭제되었습니다.');
}

/**
 * 설정 시트 생성 함수
 */
function createConfigSheet() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  let configSheet = spreadsheet.getSheetByName('설정');
  
  if (!configSheet) {
    configSheet = spreadsheet.insertSheet('설정');
  }
  
  const configData = [
    ['설정 항목', '값', '설명'],
    ['API_KEY', API_KEY, '공공데이터포털에서 발급받은 API 키'],
    ['REGION_CODE', REGION_CODE, '지역 코드 (예: 11110 = 서울 종로구)'],
    ['DEAL_YEAR', DEAL_YEAR, '조회할 연도'],
    ['DEAL_MONTH', DEAL_MONTH, '조회할 월'],
    ['', '', ''],
    ['사용법', '', ''],
    ['1. API_KEY를 공공데이터포털에서 발급받아 입력', '', ''],
    ['2. fetchAllRealEstateData() 함수 실행', '', ''],
    ['3. setupTrigger() 함수로 자동 실행 설정', '', ''],
    ['', '', ''],
    ['주요 지역 코드', '', ''],
    ['11110', '서울특별시 종로구', ''],
    ['11140', '서울특별시 중구', ''],
    ['11170', '서울특별시 용산구', ''],
    ['11200', '서울특별시 성동구', ''],
    ['11215', '서울특별시 광진구', ''],
    ['11230', '서울특별시 동대문구', ''],
    ['11260', '서울특별시 중랑구', ''],
    ['11290', '서울특별시 성북구', ''],
    ['11305', '서울특별시 강북구', ''],
    ['11320', '서울특별시 도봉구', ''],
    ['11350', '서울특별시 노원구', ''],
    ['11380', '서울특별시 은평구', ''],
    ['11410', '서울특별시 서대문구', ''],
    ['11440', '서울특별시 마포구', ''],
    ['11470', '서울특별시 양천구', ''],
    ['11500', '서울특별시 강서구', ''],
    ['11530', '서울특별시 구로구', ''],
    ['11545', '서울특별시 금천구', ''],
    ['11560', '서울특별시 영등포구', ''],
    ['11590', '서울특별시 동작구', ''],
    ['11620', '서울특별시 관악구', ''],
    ['11650', '서울특별시 서초구', ''],
    ['11680', '서울특별시 강남구', ''],
    ['11710', '서울특별시 송파구', ''],
    ['11740', '서울특별시 강동구', '']
  ];
  
  configSheet.getRange(1, 1, configData.length, 3).setValues(configData);
  
  // 스타일링
  configSheet.getRange(1, 1, 1, 3).setBackground('#4285f4').setFontColor('white').setFontWeight('bold');
  configSheet.autoResizeColumns(1, 3);
  
  console.log('설정 시트가 생성되었습니다.');
}

