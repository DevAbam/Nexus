from imagekitio import ImageKit
from fastapi import UploadFile, HTTPException, status
from src.config.settings import settings

# ✅ Initialize ImageKit with correct keys
imagekit = ImageKit(
    private_key=settings.IMAGEKIT_PRIVATE_KEY,  # required for server-side uploads
)

# Allowed image types and max size
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_image_type(file: UploadFile):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only image files (JPEG, PNG, WEBP) are allowed",
        )


async def validate_file_size(file: UploadFile) -> bytes:
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image size must be less than 5MB",
        )
    await file.seek(0)  # Reset the cursor after reading
    return contents


def upload_event_poster(file_bytes: bytes, filename: str) -> str:
    """
    Upload bytes to ImageKit and return the public URL.
    """
    try:
        response = imagekit.files.upload(
            file=file_bytes,
            file_name=filename,
            folder="/events/posters",
            tags=["event", "poster"],
            use_unique_file_name=True,
        )
        return {
            "url": response.url,
            "fileId": response.file_id,
        }  # The uploaded file URL
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload image: {e}",
        )


def delete_event_poster(file_id: str):
    try:
        return imagekit.files.delete(file_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting image: {str(e)}",
        )
