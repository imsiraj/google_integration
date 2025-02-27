import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from django.http import JsonResponse

import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from googleapiclient.http import MediaFileUpload
from urllib.parse import urlencode

def google_login(request):
    params = {
        "response_type": "code",
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "scope": "email profile https://www.googleapis.com/auth/drive.file",
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"{settings.GOOGLE_AUTH_URI}?{urlencode(params)}"
    return redirect(auth_url)


def google_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Authorization failed"}, status=400)

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(settings.GOOGLE_TOKEN_URI, data=token_data)
    token_json = token_response.json()

    if "access_token" not in token_json:
        return JsonResponse({"error": "Failed to retrieve access token", "details": token_json}, status=400)

    # Fetch user info
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {token_json['access_token']}"},
    ).json()

    return JsonResponse({
        "user_info": user_info,
        "access_token": token_json["access_token"],
        "refresh_token": token_json.get("refresh_token"),
        "expires_in": token_json["expires_in"],
    })



from django.core.files.storage import default_storage

def upload_to_drive(request):
    if "access_token" not in request.GET:
        return JsonResponse({"error": "Missing access token"}, status=400)

    creds = Credentials(token=request.GET["access_token"])
    service = build("drive", "v3", credentials=creds)

    # Handle file upload
    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    # Save file temporarily
    file_path = default_storage.save(uploaded_file.name, uploaded_file)

    file_metadata = {"name": uploaded_file.name}
    media = MediaFileUpload(file_path, mimetype=uploaded_file.content_type)

    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    return JsonResponse({"file_id": file.get("id")})

def list_drive_files(request):
    if "access_token" not in request.GET:
        return JsonResponse({"error": "Missing access token"}, status=400)

    creds = Credentials(token=request.GET["access_token"])
    service = build("drive", "v3", credentials=creds)

    results = service.files().list(
        pageSize=50,  # Limit number of results
        fields="files(id, name, mimeType, webViewLink, webContentLink)",
    ).execute()

    return JsonResponse(results)

