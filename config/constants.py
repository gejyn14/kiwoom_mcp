"""
Constants for Kiwoom MCP Server
"""

# API Hosts
KIWOOM_REAL_HOST = "https://api.kiwoom.com"
KIWOOM_MOCK_HOST = "https://mockapi.kiwoom.com"

# API Endpoints
ENDPOINTS = {
    "TOKEN": "/oauth2/token",
    "STOCK_ORDER": "/api/dostk/ordr",
}

# Exchange Types
EXCHANGE_TYPES = {
    "KRX": "KRX",
    "KOSDAQ": "NXT", 
    "SOR": "SOR"
}

# Trade Types
TRADE_TYPES = {
    "보통": "0",
    "시장가": "3",
    "조건부지정가": "5",
    "장마감후시간외": "81",
    "장시작전시간외": "61",
    "시간외단일가": "62",
    "최유리지정가": "6",
    "최우선지정가": "7",
    "보통IOC": "10",
    "시장가IOC": "13",
    "최유리IOC": "16",
    "보통FOK": "20",
    "시장가FOK": "23",
    "최유리FOK": "26",
    "스톱지정가": "28",
    "중간가": "29",
    "중간가IOC": "30",
    "중간가FOK": "31"
}

# API IDs
API_IDS = {
    "TOKEN": "au10001",
    "BUY_ORDER": "kt10000",
    "SELL_ORDER": "kt10001"
} 