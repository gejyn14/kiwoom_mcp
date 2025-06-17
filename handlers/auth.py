"""
Authentication handler for Kiwoom API
"""

import json
from typing import List, Dict, Any

import mcp.types as types

from handlers.base import BaseHandler
from config.settings import KiwoomConfig
from kiwoom.client import KiwoomAPIClient
from models.types import TokenRequest
from models.exceptions import AuthenticationError, ConfigurationError
from utils.datetime_utils import is_token_expired, format_datetime, get_remaining_time


class AuthHandler(BaseHandler):
    """Handle authentication related operations"""
    
    def __init__(self, config: KiwoomConfig):
        super().__init__()
        self.config = config
        self.client = KiwoomAPIClient(config.is_mock)
    
    async def set_credentials(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Set API credentials"""
        try:
            self.config.appkey = arguments["appkey"]
            self.config.secretkey = arguments["secretkey"]
            self.config.is_mock = arguments.get("is_mock", False)
            
            # Update client with new mock setting
            self.client = KiwoomAPIClient(self.config.is_mock)
            
            mode = "모의투자" if self.config.is_mock else "실전투자"
            message = f"키움증권 API 인증 정보가 설정되었습니다. ({mode} 모드)\n"
            message += "이제 get_access_token을 사용하여 접근 토큰을 발급받으세요."
            
            return self.create_success_response(message)
            
        except Exception as e:
            self.logger.error(f"Failed to set credentials: {e}")
            return self.create_error_response(f"인증 정보 설정 실패: {str(e)}")
    
    async def get_access_token(self) -> List[types.TextContent]:
        """Get access token from Kiwoom API"""
        try:
            if not self.config.appkey or not self.config.secretkey:
                return self.create_error_response(
                    "앱키와 시크릿키가 설정되지 않았습니다. 먼저 set_credentials를 사용하세요."
                )
            
            token_request = TokenRequest(
                appkey=self.config.appkey,
                secretkey=self.config.secretkey
            )
            
            response = self.client.get_token(token_request)
            
            if response.success:
                # Update config with new token
                self.config.access_token = response.token
                self.config.token_expires_dt = response.expires_dt
                
                mode = "모의투자" if self.config.is_mock else "실전투자"
                message = f"접근 토큰이 성공적으로 발급되었습니다! ({mode} 모드)\n\n"
                message += f"🔑 토큰 정보:\n"
                message += f"- 토큰 타입: {response.token_type or 'N/A'}\n"
                message += f"- 만료일시: {format_datetime(response.expires_dt) if response.expires_dt else 'N/A'}\n"
                message += f"- 토큰: {response.token[:20] if response.token else 'N/A'}...\n\n"
                message += f"💡 이제 주식 주문을 실행할 수 있습니다!"
                
                return self.create_success_response(message)
            else:
                message = f"토큰 발급 실패\n\n"
                message += f"응답: {json.dumps(response.raw_response, indent=2, ensure_ascii=False)}"
                return self.create_error_response(message)
                
        except AuthenticationError as e:
            return self.create_error_response(f"인증 오류: {str(e)}")
        except Exception as e:
            self.logger.error(f"Token request failed: {e}")
            return self.create_error_response(f"토큰 발급 중 오류가 발생했습니다: {str(e)}")
    
    async def set_access_token(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Set access token directly"""
        try:
            self.config.access_token = arguments["token"]
            self.config.token_expires_dt = arguments.get("expires_dt", "")
            self.config.is_mock = arguments.get("is_mock", False)
            
            # Update client with new mock setting
            self.client = KiwoomAPIClient(self.config.is_mock)
            
            mode = "모의투자" if self.config.is_mock else "실전투자"
            message = f"키움증권 API 접근 토큰이 설정되었습니다. ({mode} 모드)\n"
            
            if self.config.token_expires_dt:
                message += f"만료일시: {format_datetime(self.config.token_expires_dt)}"
            
            return self.create_success_response(message)
            
        except Exception as e:
            self.logger.error(f"Failed to set access token: {e}")
            return self.create_error_response(f"토큰 설정 실패: {str(e)}")
    
    async def check_token_status(self) -> List[types.TextContent]:
        """Check current token status"""
        try:
            if not self.config.access_token:
                return self.create_error_response("설정된 접근 토큰이 없습니다.")
            
            message = f"현재 토큰 상태:\n\n"
            message += f"- 토큰: {self.config.access_token[:20]}...\n"
            message += f"- 만료일시: {format_datetime(self.config.token_expires_dt) if self.config.token_expires_dt else 'N/A'}\n"
            message += f"- 모드: {'모의투자' if self.config.is_mock else '실전투자'}\n"
            
            if self.config.token_expires_dt:
                if is_token_expired(self.config.token_expires_dt):
                    message += f"- 상태: ❌ 만료됨\n"
                else:
                    remaining = get_remaining_time(self.config.token_expires_dt)
                    message += f"- 상태: ✅ 유효 (남은 시간: {remaining})\n"
            else:
                message += f"- 상태: ⚠️ 만료시간 정보 없음\n"
            
            return self.create_info_response(message)
            
        except Exception as e:
            self.logger.error(f"Failed to check token status: {e}")
            return self.create_error_response(f"토큰 상태 확인 실패: {str(e)}") 