import os
import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from app.api.auth import get_current_user
from app.rag.indexer import index_file

router = APIRouter()

UPLOAD_DIR = Path("./data/uploads").resolve()
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_TYPES = {"application/pdf", "text/plain", "text/csv"}


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed: PDF, TXT, CSV",
        )

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    # Prevent path traversal: strip to bare filename only
    safe_name = Path(file.filename).name
    filepath = UPLOAD_DIR / safe_name

    # Confirm the resolved path is still inside UPLOAD_DIR
    if not str(filepath).startswith(str(UPLOAD_DIR)):
        raise HTTPException(status_code=400, detail="Invalid filename.")

    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = index_file(str(filepath))
    return {"message": f"File '{safe_name}' uploaded and indexed.", **result}
