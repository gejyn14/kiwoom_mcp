"""
Order handler for stock trading operations
"""

import json
from typing import List, Dict, Any

import mcp.types as types

from handlers.base import BaseHandler
from config.settings import KiwoomConfig
from config.constants import EXCHANGE_TYPES, TRADE_TYPES
from kiwoom.client import KiwoomAPIClient
from models.types import OrderRequest
from models.exceptions import OrderError, AuthenticationError


class OrderHandler(BaseHandler):
    """Handle stock order operations"""
    
    def __init__(self, config: KiwoomConfig):
        super().__init__()
        self.config = config
        self.client = KiwoomAPIClient(config.is_mock)
    
    async def stock_buy_order(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle stock buy order"""
        return await self._stock_order(arguments, is_buy=True)
    
    async def stock_sell_order(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle stock sell order"""
        return await self._stock_order(arguments, is_buy=False)
    
    async def _stock_order(self, arguments: Dict[str, Any], is_buy: bool) -> List[types.TextContent]:
        """Execute stock order"""
        try:
            if not self.config.access_token:
                return self.create_error_response(
                    "접근 토큰이 설정되지 않았습니다. 먼저 set_access_token을 사용하세요."
                )
            
            # Create order request
            order_request = OrderRequest(
                stock_code=arguments["stock_code"],
                quantity=arguments["quantity"],
                price=arguments.get("price", ""),
                trade_type=arguments.get("trade_type", "시장가"),
                exchange=arguments.get("exchange", "KRX"),
                condition_price=arguments.get("condition_price", "")
            )
            
            # Get exchange and trade type codes
            exchange_code = EXCHANGE_TYPES.get(order_request.exchange, "KRX")
            trade_type_code = TRADE_TYPES.get(order_request.trade_type, "3")
            
            # Update client with current mock setting
            self.client = KiwoomAPIClient(self.config.is_mock)
            
            # Place order
            response = self.client.place_order(
                order_request=order_request,
                access_token=self.config.access_token,
                is_buy=is_buy,
                exchange_code=exchange_code,
                trade_type_code=trade_type_code
            )
            
            order_type = "매수" if is_buy else "매도"
            
            if response.success:
                message = f"{order_type} 주문이 성공적으로 처리되었습니다.\n\n"
                message += f"📋 주문 정보:\n"
                message += f"- 종목코드: {order_request.stock_code}\n"
                message += f"- 주문수량: {order_request.quantity:,}주\n"
                message += f"- 주문단가: {order_request.price or '시장가'}\n"
                message += f"- 매매구분: {order_request.trade_type} ({trade_type_code})\n"
                message += f"- 거래소: {order_request.exchange}\n\n"
                
                if response.order_number:
                    message += f"🔢 주문번호: {response.order_number}\n"
                
                if response.message:
                    message += f"💬 응답메시지: {response.message}\n"
                
                if response.raw_response:
                    message += f"\n📊 전체 응답:\n```json\n{json.dumps(response.raw_response, indent=2, ensure_ascii=False)}\n```"
                
                return self.create_success_response(message)
            else:
                message = f"{order_type} 주문 실패\n\n"
                if response.raw_response:
                    message += f"응답: {json.dumps(response.raw_response, indent=2, ensure_ascii=False)}"
                else:
                    message += f"오류: {response.message or 'Unknown error'}"
                
                return self.create_error_response(message)
                
        except OrderError as e:
            return self.create_error_response(f"주문 오류: {str(e)}")
        except AuthenticationError as e:
            return self.create_error_response(f"인증 오류: {str(e)}")
        except Exception as e:
            self.logger.error(f"Order processing failed: {e}")
            return self.create_error_response(f"주문 처리 중 오류가 발생했습니다: {str(e)}")
    
    async def get_trade_types(self) -> List[types.TextContent]:
        """Get available trade types"""
        try:
            message = "사용 가능한 매매구분:\n\n"
            
            for korean_name, code in TRADE_TYPES.items():
                message += f"- {korean_name}: {code}\n"
            
            return self.create_info_response(message)
            
        except Exception as e:
            self.logger.error(f"Failed to get trade types: {e}")
            return self.create_error_response(f"매매구분 조회 실패: {str(e)}") 