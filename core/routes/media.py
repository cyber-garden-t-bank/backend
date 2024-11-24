from fastapi import File, UploadFile, APIRouter
from io import BytesIO


router = APIRouter(
    prefix="/finance",
    tags=["media"],
)

@router.post("/upload/")
async def upload_file(img: UploadFile = File(...)):
    buffer = BytesIO()

    contents = await img.read()
    buffer.write(contents)

    return {"filename": img.filename, "size": len(contents)}

# Запустите приложение с помощью uvicorn:
# uvicorn your_module_name:app --reload
