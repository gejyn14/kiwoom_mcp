"""
Data types and models for Kiwoom API
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class OrderRequest:
    """Stock order request model"""
    stock_code: str
    quantity: int
    price: Optional[str] = ""
    trade_type: str = "시장가"
    exchange: str = "KRX"
    condition_price: Optional[str] = ""
    
    def to_api_dict(self, exchange_code: str, trade_type_code: str) -> Dict[str, Any]:
        """Convert to API request format"""
        return {
            "dmst_stex_tp": exchange_code,
            "stk_cd": self.stock_code,
            "ord_qty": str(self.quantity),
            "ord_uv": self.price or "",
            "trde_tp": trade_type_code,
            "cond_uv": self.condition_price or ""
        }


@dataclass
class OrderResponse:
    """Stock order response model"""
    success: bool
    order_number: Optional[str] = None
    message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
    status_code: Optional[int] = None


@dataclass
class TokenRequest:
    """Token request model"""
    appkey: str
    secretkey: str
    grant_type: str = "client_credentials"
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to API request format"""
        return {
            "grant_type": self.grant_type,
            "appkey": self.appkey,
            "secretkey": self.secretkey
        }


@dataclass
class TokenResponse:
    """Token response model"""
    success: bool
    token: Optional[str] = None
    token_type: Optional[str] = None
    expires_dt: Optional[str] = None
    message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class OrderModifyRequest:
    """Stock order modification request model"""
    exchange: str  # 국내거래소구분 (KRX, NXT, SOR)
    original_order_number: str  # 원주문번호
    stock_code: str  # 종목코드
    modify_quantity: str  # 정정수량
    modify_price: str  # 정정단가
    modify_condition_price: Optional[str] = ""  # 정정조건단가
    
    def to_api_dict(self, exchange_code: str) -> Dict[str, Any]:
        """Convert to API request format"""
        return {
            "dmst_stex_tp": exchange_code,
            "orig_ord_no": self.original_order_number,
            "stk_cd": self.stock_code,
            "mdfy_qty": self.modify_quantity,
            "mdfy_uv": self.modify_price,
            "mdfy_cond_uv": self.modify_condition_price or ""
        }


@dataclass
class OrderModifyResponse:
    """Stock order modification response model"""
    success: bool
    order_number: Optional[str] = None  # 주문번호
    base_original_order_number: Optional[str] = None  # 모주문번호
    modify_quantity: Optional[str] = None  # 정정수량
    exchange_type: Optional[str] = None  # 국내거래소구분
    message: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None
    status_code: Optional[int] = None 