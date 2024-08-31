
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
import httpx
from fastapi.responses import StreamingResponse
from app.utils.file_extraction_utility import download_public_s3_file_to_dataframe
from app.utils.jwt_utility import get_current_user
from app.services.process_file import start_stop_detection
from app.models.user_model import UserBase


router = APIRouter()


@router.get("/file/")
async def get_file(url: str):
    
    try:
        file_stream = download_public_s3_file_to_dataframe(url)
        return StreamingResponse(file_stream, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=downloaded_file.csv"})
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))

@router.post("/process_file/")
async def detect_start(url:str, significance_threshold: int):
    return await start_stop_detection(url, significance_threshold)