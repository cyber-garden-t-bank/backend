from fastapi import File, UploadFile, APIRouter
from io import BytesIO


router = APIRouter(
    prefix="/media",
    tags=["media"],
)

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    buffer = BytesIO()

    contents = await file.read()
    buffer.write(contents)

    return {"filename": file.filename, "size": len(contents)}

# Запустите приложение с помощью uvicorn:
# uvicorn your_module_name:app --reload
