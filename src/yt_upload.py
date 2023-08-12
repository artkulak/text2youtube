import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from src.logger import logger


def upload_video(
    credentials,
    video: str,
    title: str,
    description: str,
    thumbnail: str,
    privacy_status: str = "public",
):
    # Create the YouTube API service
    youtube = build("youtube", "v3", credentials=credentials)

    # Create a video resource
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": [],  # Add tags if needed
            # 'categoryId': '22'  # Change the category ID if needed
        },
        "status": {"privacyStatus": privacy_status},
    }

    # Upload the video
    media = MediaFileUpload(video)
    response = (
        youtube.videos()
        .insert(part="snippet,status", body=request_body, media_body=media)
        .execute()
    )

    # Print the video upload response
    logger.info(f"Video uploaded successfully. Video ID: {response['id']}")


def get_yt_credentials(cred_path: str):
    """
    Loads or generates YouTube API credentials from the specified credential path.

    :param cred_path: Path to the API credentials file.
    :return: Authenticated credentials object for YouTube API.
    :rtype: google.auth.credentials.Credentials or None
    """
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    # Load or generate credentials
    if os.path.exists(cred_path):
        return InstalledAppFlow.from_client_secrets_file(
            cred_path, scopes
        ).run_local_server(port=0)
    logger.warning("Please provide valid API credentials in 'credentials.json'")
