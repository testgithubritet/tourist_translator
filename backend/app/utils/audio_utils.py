import os
import shutil
import tempfile
from fastapi import UploadFile


def save_temp_audio(upload_file: UploadFile) -> str:
    """Saves incoming browser audio to a temporary file on disk."""
    suffix = os.path.splitext(upload_file.filename or "")[-1]
    if not suffix:
        suffix = ".webm"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_audio:
        shutil.copyfileobj(upload_file.file, temp_audio)
        return temp_audio.name


def cleanup_temp_file(file_path: str) -> None:
    """Safely removes temporary files."""
    if file_path and os.path.exists(file_path):
        os.remove(file_path)