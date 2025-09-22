// Google Sheets 열기 감지 및 주식 데이터 업데이트

console.log('Stock Updater 확장 프로그램이 로드되었습니다.');

// 스프레드시트 URL 패턴 감지
const SPREADSHEET_PATTERN = /docs\.google\.com\/spreadsheets\/d\/([a-zA-Z0-9-_]+)/;

// 페이지 로드 시 실행
if (SPREADSHEET_PATTERN.test(window.location.href)) {
  console.log('Google Sheets 감지됨');
  
  // 스프레드시트 ID 추출
  const match = window.location.href.match(SPREADSHEET_PATTERN);
  const spreadsheetId = match[1];
  
  // 로컬 스토리지에서 마지막 업데이트 시간 확인
  const lastUpdate = localStorage.getItem('lastStockUpdate');
  const now = new Date();
  
  // 1시간 이상 지났으면 업데이트
  if (!lastUpdate || (now - new Date(lastUpdate)) > 60 * 60 * 1000) {
    updateStockData(spreadsheetId);
    localStorage.setItem('lastStockUpdate', now.toString());
  }
}

// 주식 데이터 업데이트 함수
async function updateStockData(spreadsheetId) {
  try {
    console.log('주식 데이터 업데이트 시작...');
    
    // 외부 API 호출 (로컬 서버)
    const response = await fetch('http://localhost:5000/webhook/spreadsheet-opened', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        spreadsheetId: spreadsheetId,
        timestamp: new Date().toISOString()
      })
    });
    
    if (response.ok) {
      const result = await response.json();
      console.log('주식 데이터 업데이트 성공:', result);
      
      // 사용자에게 알림
      showNotification('주식 데이터가 업데이트되었습니다!');
    } else {
      console.error('업데이트 실패:', response.statusText);
    }
    
  } catch (error) {
    console.error('주식 데이터 업데이트 오류:', error);
  }
}

// 알림 표시 함수
function showNotification(message) {
  // 간단한 알림 생성
  const notification = document.createElement('div');
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #4CAF50;
    color: white;
    padding: 15px 20px;
    border-radius: 5px;
    z-index: 10000;
    font-family: Arial, sans-serif;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
  `;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  // 3초 후 제거
  setTimeout(() => {
    if (notification.parentNode) {
      notification.parentNode.removeChild(notification);
    }
  }, 3000);
}
