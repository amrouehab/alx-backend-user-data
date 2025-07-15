cat > README.md << 'EOF'
# 0x01. Basic Authentication

## Description
This project implements Basic Authentication for a simple API. It includes:

- Error handlers for 401 (Unauthorized) and 403 (Forbidden) HTTP status codes
- Authentication system with Base64 encoding/decoding
- User credential extraction and validation
- Request filtering and authentication checking

## Requirements
- Ubuntu 18.04 LTS
- Python 3.7
- pycodestyle 2.5
- Flask

## Files
- `api/v1/app.py` - Main Flask application with error handlers and request filtering
- `api/v1/views/index.py` - API endpoints including unauthorized and forbidden routes
- `api/v1/auth/auth.py` - Base authentication class
- `api/v1/auth/basic_auth.py` - Basic authentication implementation
- Various test files (`main_*.py`)

## Usage
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the server
API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app

# Test with Basic Auth
API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=basic_auth python3 -m api.v1.app
