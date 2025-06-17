# Kiwoom MCP Server

키움 OPEN API(REST)를 활용한 .

## 🏗️ Project Structure

```
kiwoom_mcp/                       # Project root
├── __init__.py                   # Package initialization
├── main.py                       # Entry point (clean & simple)
├── server.py                     # Main MCP server class
├── pyproject.toml                # Project configuration
├── README.md                     # This file
├── config/                       # Configuration management
│   ├── __init__.py
│   ├── constants.py              # API constants and mappings
│   └── settings.py               # Configuration classes
├── models/                       # Data models and types
│   ├── __init__.py
│   ├── exceptions.py             # Custom exceptions
│   └── types.py                  # Request/Response models
├── kiwoom/                       # Kiwoom API client
│   ├── __init__.py
│   └── client.py                 # HTTP client for Kiwoom API
├── handlers/                     # MCP tool handlers
│   ├── __init__.py
│   ├── base.py                   # Base handler class
│   ├── auth.py                   # Authentication handlers
│   └── orders.py                 # Order management handlers
└── utils/                        # Utilities and helpers
    ├── __init__.py
    ├── datetime_utils.py         # Date/time utilities
    └── logging.py                # Logging configuration
```

## 🚀 특징징

- **모듈러 아키텍처**: Clean separation of concerns
- **Type Safety**: Full TypeScript-like typing with Python
- **Error Handling**: Comprehensive exception handling
- **Configuration**: Environment-based configuration
- **Logging**: Structured logging with multiple levels
- **Extensible**: Easy to add new features and handlers

## 📦 Available Tools

### Authentication
- `set_credentials` - Set API credentials
- `get_access_token` - Get access token from Kiwoom
- `set_access_token` - Set access token directly
- `check_token_status` - Check token status and expiration

### Trading
- `stock_buy_order` - Place buy orders
- `stock_sell_order` - Place sell orders
- `get_trade_types` - Get available trade types

## 🔧 Configuration

### Environment Variables

```bash
# Kiwoom API Configuration
KIWOOM_APPKEY=your_app_key
KIWOOM_SECRETKEY=your_secret_key
KIWOOM_IS_MOCK=false
KIWOOM_ACCESS_TOKEN=your_token
KIWOOM_TOKEN_EXPIRES_DT=20241231235959

# Server Configuration
MCP_SERVER_NAME=kiwoom-stock-mcp
MCP_SERVER_VERSION=1.0.0
LOG_LEVEL=INFO
```

### Programmatic Configuration

```python
from config.settings import KiwoomConfig, ServerConfig

# Create configurations
kiwoom_config = KiwoomConfig(
    appkey="your_app_key",
    secretkey="your_secret_key",
    is_mock=False
)

server_config = ServerConfig(
    name="custom-server-name",
    version="1.0.0",
    log_level="DEBUG"
)
```

## 🏃 Running the Server

### Basic Usage
```bash
python main.py
```

### With Environment Variables
```bash
export KIWOOM_APPKEY=your_app_key
export KIWOOM_SECRETKEY=your_secret_key
export KIWOOM_IS_MOCK=true
python main.py
```

## 🔌 Extending the Server

### Adding New Handlers

1. Create a new handler in `handlers/`:

```python
# handlers/portfolio.py
from .base import BaseHandler
from ..models.types import PortfolioRequest, PortfolioResponse

class PortfolioHandler(BaseHandler):
    async def get_portfolio(self, arguments: Dict[str, Any]) -> List[types.TextContent]:
        # Implementation here
        return self.create_success_response("Portfolio retrieved")
```

2. Register in `server.py`:

```python
# In KiwoomMCPServer.__init__()
self.portfolio_handler = PortfolioHandler(self.kiwoom_config)

# In _setup_handlers()
elif name == "get_portfolio":
    return await self.portfolio_handler.get_portfolio(arguments)
```

### Adding New API Endpoints

1. Add constants in `config/constants.py`:

```python
ENDPOINTS = {
    "TOKEN": "/oauth2/token",
    "STOCK_ORDER": "/api/dostk/ordr",
    "PORTFOLIO": "/api/portfolio",  # New endpoint
}
```

2. Extend the client in `kiwoom/client.py`:

```python
def get_portfolio(self, access_token: str) -> PortfolioResponse:
    # Implementation here
    pass
```

### Adding New Models

1. Define in `models/types.py`:

```python
@dataclass
class PortfolioRequest:
    account_number: str
    include_positions: bool = True

@dataclass  
class PortfolioResponse:
    success: bool
    positions: List[Position]
    total_value: float
```

## 🔍 Benefits of This Structure

1. **Maintainability**: Each component has a single responsibility
2. **Testability**: Easy to unit test individual components
3. **Scalability**: Simple to add new features without affecting existing code
4. **Reusability**: Components can be reused across different parts
5. **Type Safety**: Full typing for better IDE support and error catching
6. **Configuration Management**: Centralized and flexible configuration
7. **Error Handling**: Consistent error handling across all components

## 🚦 Migration from Monolithic Structure

The old 489-line `main.py` has been refactored into:
- **12 focused modules** with clear responsibilities
- **Type-safe interfaces** between components  
- **Proper separation** of configuration, business logic, and presentation
- **Extensible architecture** for future enhancements

This structure follows Python best practices and makes the codebase much more professional and maintainable. 