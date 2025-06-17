"""
Logging utilities for Kiwoom MCP Server
"""

import logging
from typing import Optional


def setup_logging(level: str = "INFO", name: Optional[str] = None) -> logging.Logger:
    """Setup logging configuration"""
    logger = logging.getLogger(name or "kiwoom-mcp")
    
    # Don't add handlers if already configured
    if logger.handlers:
        return logger
    
    # Set level
    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')
    
    logger.setLevel(numeric_level)
    
    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(numeric_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(handler)
    
    return logger 