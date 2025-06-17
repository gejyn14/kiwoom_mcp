"""
Base handler class for MCP tools
"""

import logging
from typing import List, Dict, Any

import mcp.types as types


class BaseHandler:
    """Base class for MCP tool handlers"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def create_success_response(self, message: str) -> List[types.TextContent]:
        """Create successful response"""
        return [types.TextContent(type="text", text=f"✅ {message}")]
    
    def create_error_response(self, message: str) -> List[types.TextContent]:
        """Create error response"""
        return [types.TextContent(type="text", text=f"❌ {message}")]
    
    def create_info_response(self, message: str) -> List[types.TextContent]:
        """Create info response"""
        return [types.TextContent(type="text", text=f"ℹ️ {message}")]
    
    def create_warning_response(self, message: str) -> List[types.TextContent]:
        """Create warning response"""
        return [types.TextContent(type="text", text=f"⚠️ {message}")]
    
    async def handle(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Handle tool call - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement handle method") 