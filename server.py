"""
Main MCP Server for Kiwoom Securities API
"""

from typing import List, Dict, Any

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from config.settings import KiwoomConfig, ServerConfig
from config.constants import TRADE_TYPES, EXCHANGE_TYPES
from handlers.auth import AuthHandler
from handlers.orders import OrderHandler
from utils.logging import setup_logging


class KiwoomMCPServer:
    """Kiwoom MCP Server"""
    
    def __init__(self, kiwoom_config: KiwoomConfig = None, server_config: ServerConfig = None):
        # Initialize configs
        self.kiwoom_config = kiwoom_config or KiwoomConfig()
        self.server_config = server_config or ServerConfig()
        
        # Setup logging
        self.logger = setup_logging(self.server_config.log_level, "kiwoom-mcp-server")
        
        # Initialize MCP server
        self.server = Server(self.server_config.name)
        
        # Initialize handlers
        self.auth_handler = AuthHandler(self.kiwoom_config)
        self.order_handler = OrderHandler(self.kiwoom_config)
        
        # Setup handlers
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup MCP handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List available tools"""
            return [
                types.Tool(
                    name="set_credentials",
                    description="키움증권 API 앱키와 시크릿키 설정",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "appkey": {
                                "type": "string",
                                "description": "키움증권 앱키"
                            },
                            "secretkey": {
                                "type": "string",
                                "description": "키움증권 시크릿키"
                            },
                            "is_mock": {
                                "type": "boolean",
                                "description": "모의투자 여부 (기본값: false)",
                                "default": False
                            }
                        },
                        "required": ["appkey", "secretkey"]
                    }
                ),
                types.Tool(
                    name="get_access_token",
                    description="키움증권 API 접근 토큰 발급 (au10001)",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="set_access_token",
                    description="키움증권 API 접근 토큰 직접 설정 (이미 발급받은 토큰 사용)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "token": {
                                "type": "string",
                                "description": "키움증권 API 접근 토큰"
                            },
                            "expires_dt": {
                                "type": "string",
                                "description": "토큰 만료일시 (YYYYMMDDHHMMSS 형식)",
                                "default": ""
                            },
                            "is_mock": {
                                "type": "boolean",
                                "description": "모의투자 여부 (기본값: false)",
                                "default": False
                            }
                        },
                        "required": ["token"]
                    }
                ),
                types.Tool(
                    name="check_token_status",
                    description="현재 토큰 상태 및 만료시간 확인",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="stock_buy_order",
                    description="주식 매수 주문 (kt10000)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "stock_code": {
                                "type": "string",
                                "description": "종목코드 (예: 005930)"
                            },
                            "quantity": {
                                "type": "integer",
                                "description": "주문수량"
                            },
                            "price": {
                                "type": "string",
                                "description": "주문단가 (시장가의 경우 빈 문자열)",
                                "default": ""
                            },
                            "trade_type": {
                                "type": "string",
                                "description": "매매구분",
                                "enum": list(TRADE_TYPES.keys()),
                                "default": "시장가"
                            },
                            "exchange": {
                                "type": "string",
                                "description": "거래소구분",
                                "enum": list(EXCHANGE_TYPES.keys()),
                                "default": "KRX"
                            },
                            "condition_price": {
                                "type": "string",
                                "description": "조건단가",
                                "default": ""
                            }
                        },
                        "required": ["stock_code", "quantity"]
                    }
                ),
                types.Tool(
                    name="stock_sell_order",
                    description="주식 매도 주문 (kt10001)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "stock_code": {
                                "type": "string",
                                "description": "종목코드 (예: 005930)"
                            },
                            "quantity": {
                                "type": "integer",
                                "description": "주문수량"
                            },
                            "price": {
                                "type": "string",
                                "description": "주문단가 (시장가의 경우 빈 문자열)",
                                "default": ""
                            },
                            "trade_type": {
                                "type": "string",
                                "description": "매매구분",
                                "enum": list(TRADE_TYPES.keys()),
                                "default": "시장가"
                            },
                            "exchange": {
                                "type": "string",
                                "description": "거래소구분",
                                "enum": list(EXCHANGE_TYPES.keys()),
                                "default": "KRX"
                            },
                            "condition_price": {
                                "type": "string",
                                "description": "조건단가",
                                "default": ""
                            }
                        },
                        "required": ["stock_code", "quantity"]
                    }
                ),
                types.Tool(
                    name="get_trade_types",
                    description="사용 가능한 매매구분 목록 조회",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, arguments: Dict[str, Any]
        ) -> List[types.TextContent]:
            """Handle tool calls"""
            
            self.logger.info(f"Tool called: {name}")
            
            try:
                if name == "set_credentials":
                    return await self.auth_handler.set_credentials(arguments)
                elif name == "get_access_token":
                    return await self.auth_handler.get_access_token()
                elif name == "set_access_token":
                    return await self.auth_handler.set_access_token(arguments)
                elif name == "check_token_status":
                    return await self.auth_handler.check_token_status()
                elif name == "stock_buy_order":
                    return await self.order_handler.stock_buy_order(arguments)
                elif name == "stock_sell_order":
                    return await self.order_handler.stock_sell_order(arguments)
                elif name == "get_trade_types":
                    return await self.order_handler.get_trade_types()
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                self.logger.error(f"Tool call failed: {name}, error: {e}")
                return [
                    types.TextContent(
                        type="text",
                        text=f"❌ 도구 실행 중 오류가 발생했습니다: {str(e)}"
                    )
                ]

    async def run(self):
        """Run the MCP server"""
        self.logger.info(f"Starting {self.server_config.name} v{self.server_config.version}")
        
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=self.server_config.name,
                    server_version=self.server_config.version,
                    capabilities=self.server.get_capabilities(
                        notification_options=None,
                        experimental_capabilities=None,
                    )
                )
            ) 