"""
Kiwoom API Client
"""

import requests
import logging
from typing import Dict, Any, Optional

from ..config.constants import KIWOOM_REAL_HOST, KIWOOM_MOCK_HOST, ENDPOINTS, API_IDS
from ..models.types import TokenRequest, TokenResponse, OrderRequest, OrderResponse
from ..models.exceptions import KiwoomAPIError, AuthenticationError, OrderError


class KiwoomAPIClient:
    """Kiwoom API client"""
    
    def __init__(self, is_mock: bool = False):
        self.is_mock = is_mock
        self.base_url = KIWOOM_MOCK_HOST if is_mock else KIWOOM_REAL_HOST
        self.logger = logging.getLogger(__name__)
        
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to Kiwoom API"""
        url = self.base_url + endpoint
        
        default_headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        
        if headers:
            default_headers.update(headers)
        
        self.logger.debug(f"Making {method} request to {url}")
        
        try:
            if method.upper() == "POST":
                response = requests.post(url, headers=default_headers, json=data)
            else:
                response = requests.get(url, headers=default_headers, params=data)
            
            response_data = response.json()
            
            if response.status_code != 200:
                raise KiwoomAPIError(
                    f"API request failed: {response.status_code}",
                    status_code=response.status_code,
                    response_data=response_data
                )
            
            return response_data
            
        except requests.RequestException as e:
            self.logger.error(f"Request error: {e}")
            raise KiwoomAPIError(f"Request failed: {str(e)}")
    
    def get_token(self, token_request: TokenRequest) -> TokenResponse:
        """Get access token"""
        try:
            response_data = self._make_request(
                "POST",
                ENDPOINTS["TOKEN"],
                token_request.to_api_dict()
            )
            
            if response_data.get("return_code") == 0:
                return TokenResponse(
                    success=True,
                    token=response_data.get("token"),
                    token_type=response_data.get("token_type"),
                    expires_dt=response_data.get("expires_dt"),
                    raw_response=response_data
                )
            else:
                return TokenResponse(
                    success=False,
                    message=response_data.get("return_msg", "Unknown error"),
                    raw_response=response_data
                )
                
        except Exception as e:
            self.logger.error(f"Token request failed: {e}")
            raise AuthenticationError(f"Token request failed: {str(e)}")
    
    def place_order(
        self, 
        order_request: OrderRequest, 
        access_token: str,
        is_buy: bool,
        exchange_code: str,
        trade_type_code: str
    ) -> OrderResponse:
        """Place stock order"""
        try:
            api_id = API_IDS["BUY_ORDER"] if is_buy else API_IDS["SELL_ORDER"]
            
            headers = {
                "authorization": f"Bearer {access_token}",
                "cont-yn": "N",
                "next-key": "",
                "api-id": api_id
            }
            
            response_data = self._make_request(
                "POST",
                ENDPOINTS["STOCK_ORDER"],
                order_request.to_api_dict(exchange_code, trade_type_code),
                headers
            )
            
            # Check if the response indicates success
            # This might need adjustment based on actual API response format
            return OrderResponse(
                success=True,  # Assume success if no exception
                order_number=response_data.get("ord_no"),
                message=response_data.get("return_msg"),
                raw_response=response_data,
                status_code=200
            )
            
        except Exception as e:
            self.logger.error(f"Order request failed: {e}")
            raise OrderError(f"Order request failed: {str(e)}") 