# Google OAuth, Drive Integration, and WebSocket Chat

## Overview
This project integrates Google OAuth 2.0 for authentication, Google Drive API for file management, and WebSockets for real-time chat between users using Django.

## Features
- **Google Authentication**: Users can log in using their Google account.
- **Google Drive Integration**: Upload files to Google Drive and list files.
- **WebSocket Chat**: Real-time chat between two pre-configured users.

## Setup Instructions

### Prerequisites
- Python 3.11+
- Django
- Redis (for WebSockets)
- Google Developer Console account

### Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/your-username/google-integration.git
   cd google-integration
   ```
2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

### Configuration
1. **Set up Google OAuth Credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create OAuth credentials
   - Add redirect URI: `http://127.0.0.1:8000/auth/callback/`
   - Get `CLIENT_ID` and `CLIENT_SECRET`

2. **Set up `.env` file:**
   ```sh
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_REDIRECT_URI=http://127.0.0.1:8000/auth/callback/
   GOOGLE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
   GOOGLE_TOKEN_URI=https://oauth2.googleapis.com/token
   ```

### Running the Project
1. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```
2. **Start Redis Server:**
   ```sh
   redis-server
   ```
3. **Run Django server:**
   ```sh
   python manage.py runserver
   ```

## API Endpoints
### Google Authentication
- **Login:** `[GET] /auth/login/`
- **Callback:** `[GET] /auth/callback/?code=XYZ`

### Google Drive
- **Upload File:** `[POST] /drive/upload/`
- **List Files:** `[GET] /drive/list/`

### WebSocket Chat
1. Connect using a WebSocket client (e.g., Postman) to:
   ```
   ws://127.0.0.1:8000/ws/chat/
   ```
2. Send a message in JSON format:
   ```json
   {"message": "Hello, WebSocket!"}
   ```

## Testing with Postman
1. Use Postman to test **Google Auth** and **Drive API**.
2. Use a WebSocket client to test **real-time chat**.

## Deployment
For production, configure **Redis, Gunicorn, and Nginx**.

## License
This project is open-source under the MIT License.

