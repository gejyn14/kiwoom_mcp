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