#!/usr/bin/env python3
"""
Kiwoom MCP Server - Entry Point
"""

import asyncio
from server import KiwoomMCPServer
from config.settings import KiwoomConfig, ServerConfig


async def main():
    """Main entry point"""
    # Load configuration from environment or use defaults
    kiwoom_config = KiwoomConfig.from_env()
    server_config = ServerConfig.from_env()
    
    # Create and run server
    server = KiwoomMCPServer(kiwoom_config, server_config)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
