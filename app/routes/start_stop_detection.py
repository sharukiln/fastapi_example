
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import httpx
from fastapi.responses import StreamingResponse
from app.utils.file_extraction_utility import download_public_s3_file
from app.utils.jwt_utility import get_current_user
from app.services.process_file import start_stop_detection
from app.models.user_model import UserBase


router = APIRouter()


@router.get("/file/")
async def get_file(url: str):
    
    """
    Given a URL, download the file from the URL and return a StreamingResponse
    containing the file data. The file is expected to be a CSV file.

    Args:
        url (str): URL of the file to download.

    Returns:
        StreamingResponse: A StreamingResponse containing the file data.
    """
    try:
        file_stream = download_public_s3_file(url)
        return StreamingResponse(file_stream, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=downloaded_file.csv"})
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

@router.post("/process_file/")
async def detect_start(url:str, significance_threshold: int):
    """
    Run the start-stop detection algorithm on a CSV file.

    Args:
        url (str): URL of the CSV file to process.
        significance_threshold (int): The minimum number of data points
            required to consider a start or stop event as significant.

    Returns:
        The result of the start-stop detection algorithm.
    """
    return await start_stop_detection(url, significance_threshold)