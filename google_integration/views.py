import requests
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from googleapiclient.http import MediaFileUpload
from urllib.parse import urlencode
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Google OAuth Login
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


# Google OAuth Callback

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

    return JsonResponse({
        "access_token": token_json["access_token"],
        "refresh_token": token_json.get("refresh_token"),
        "expires_in": token_json["expires_in"],
    })


def upload_to_drive(request):
    if "access_token" not in request.GET:
        return JsonResponse({"error": "Missing access token"}, status=400)

    creds = Credentials(token=request.GET["access_token"])
    service = build("drive", "v3", credentials=creds)

    uploaded_file = request.FILES.get("file")
    if not uploaded_file:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    file_path = default_storage.save(uploaded_file.name, uploaded_file)

    file_metadata = {"name": uploaded_file.name}
    media = MediaFileUpload(file_path, mimetype=uploaded_file.content_type)

    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    return JsonResponse({"file_id": file.get("id")})



# List Files from Google Drive
def list_drive_files(request):
    if "access_token" not in request.GET:
        return JsonResponse({"error": "Missing access token"}, status=400)

    creds = Credentials(token=request.GET["access_token"])
    service = build("drive", "v3", credentials=creds)

    results = service.files().list(
        pageSize=50,
        fields="files(id, name, mimeType, webViewLink, webContentLink)",
    ).execute()

    return JsonResponse(results)

def download_file(request):
    if "access_token" not in request.GET or "file_id" not in request.GET:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    creds = Credentials(token=request.GET["access_token"])
    service = build("drive", "v3", credentials=creds)

    file_id = request.GET["file_id"]
    request = service.files().get_media(fileId=file_id)

    file_path = f"downloads/{file_id}.jpg"
    with open(file_path, "wb") as file:
        file.write(request.execute())

    return JsonResponse({"message": "File downloaded successfully", "file_path": file_path})

