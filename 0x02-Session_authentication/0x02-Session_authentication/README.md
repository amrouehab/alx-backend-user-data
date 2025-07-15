# Create README.md
cat > README.md << 'EOF'
# 0x02. Session authentication

This project implements Session authentication as an extension to the Basic authentication system.

## Requirements

- Python 3.7
- Ubuntu 18.04 LTS
- pycodestyle 2.5
- All files must be executable
- All modules, classes, and functions must have documentation

## Tasks

0. Et moi et moi et moi! - Copy Basic auth project and add /users/me endpoint
1. Empty session - Create SessionAuth class
2. Create a session - Implement session creation
3. User ID for Session ID - Implement session-to-user mapping
4. Session cookie - Add cookie handling
5. Before request - Update authentication flow
6. Use Session ID for identifying a User - Complete session auth
7. New view for Session Authentication - Add login endpoint
8. Logout - Add logout functionality
9. Expiration - Add session expiration
10. Sessions in database - Store sessions in database

## Usage

```bash
API_HOST=0.0.0.0 API_PORT=5000 AUTH_TYPE=session_auth SESSION_NAME=_my_session_id python3 -m api.v1.app
