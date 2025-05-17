from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
import uuid
from app.utils.file_utils import save_temp_file
from app.services.ocr_service import extract_text_boxes
from app.services.pii_masker import mask_pii

router = APIRouter()


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    temp_path = save_temp_file(file)
    text_data = extract_text_boxes(temp_path)
    output_path = mask_pii(temp_path, text_data)
    return FileResponse(output_path, media_type="image/png")
