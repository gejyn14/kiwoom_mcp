"""
Settings and configuration for Kiwoom MCP Server
"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class KiwoomConfig:
    """Kiwoom API configuration"""
    appkey: Optional[str] = None
    secretkey: Optional[str] = None
    is_mock: bool = False
    access_token: Optional[str] = None
    token_expires_dt: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "KiwoomConfig":
        """Create config from environment variables"""
        return cls(
            appkey=os.getenv("KIWOOM_APPKEY"),
            secretkey=os.getenv("KIWOOM_SECRETKEY"),
            is_mock=os.getenv("KIWOOM_IS_MOCK", "false").lower() == "true",
            access_token=os.getenv("KIWOOM_ACCESS_TOKEN"),
            token_expires_dt=os.getenv("KIWOOM_TOKEN_EXPIRES_DT")
        )


@dataclass
class ServerConfig:
    """MCP Server configuration"""
    name: str = "kiwoom-stock-mcp"
    version: str = "1.0.0"
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "ServerConfig":
        """Create config from environment variables"""
        return cls(
            name=os.getenv("MCP_SERVER_NAME", "kiwoom-stock-mcp"),
            version=os.getenv("MCP_SERVER_VERSION", "1.0.0"),
            log_level=os.getenv("LOG_LEVEL", "INFO")
        ) 