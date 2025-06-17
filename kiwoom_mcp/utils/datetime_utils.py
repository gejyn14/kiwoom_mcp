"""
Datetime utilities for Kiwoom MCP Server
"""

from datetime import datetime
from typing import Optional


def is_token_expired(expires_dt: str) -> bool:
    """Check if token is expired"""
    try:
        expire_dt = datetime.strptime(expires_dt, "%Y%m%d%H%M%S")
        current_dt = datetime.now()
        return current_dt >= expire_dt
    except (ValueError, TypeError):
        return True  # Assume expired if can't parse


def format_datetime(dt_str: str) -> str:
    """Format datetime string for display"""
    try:
        dt = datetime.strptime(dt_str, "%Y%m%d%H%M%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return dt_str


def get_remaining_time(expires_dt: str) -> Optional[str]:
    """Get remaining time until expiration"""
    try:
        expire_dt = datetime.strptime(expires_dt, "%Y%m%d%H%M%S")
        current_dt = datetime.now()
        
        if current_dt >= expire_dt:
            return None
        
        remaining = expire_dt - current_dt
        return str(remaining).split('.')[0]  # Remove microseconds
    except (ValueError, TypeError):
        return None 