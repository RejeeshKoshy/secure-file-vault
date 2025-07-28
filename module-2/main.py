from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import FileResponse
import os

from encryption_utils import encrypt_file, decrypt_file
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File, Form, HTTPException


app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

STORAGE = "vault"

MAX_FILE_SIZE_MB = 5  # Set your preferred limit (e.g., 5MB)

@app.post("/upload")
async def upload(file: UploadFile = File(...), password: str = Form(...)):
    try:
        # ✅ File type check
        if file.content_type not in ["image/jpeg", "image/png", "application/pdf", "text/plain"]:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # ✅ File size check
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File size exceeds limit")

        # ✅ Encryption
        encrypted = encrypt_file(contents, password)
        save_path = os.path.join(STORAGE, file.filename + ".enc")
        with open(save_path, "wb") as f:
            f.write(encrypted)

        return {"message": "File encrypted and uploaded!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/download")
async def download(filename: str = Form(...), password: str = Form(...)):
    path = os.path.join(STORAGE, filename + ".enc")

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Encrypted file not found")

    try:
        with open(path, "rb") as f:
            encrypted = f.read()

        decrypted = decrypt_file(encrypted, password)

        decrypted_path = os.path.join(STORAGE, "temp_" + filename)
        with open(decrypted_path, "wb") as f:
            f.write(decrypted)

        return FileResponse(decrypted_path, filename=filename)
    except Exception as e:
        raise HTTPException(status_code=403, detail="Incorrect password or decryption failed")

@app.get("/list_files")
def list_files():
    try:
        files = [
            f.replace(".enc", "")
            for f in os.listdir(STORAGE)
            if f.endswith(".enc")
        ]
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/delete")
async def delete_file(filename: str = Form(...)):
    path = os.path.join(STORAGE, filename + ".enc")
    
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        os.remove(path)
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/list")
async def list_files():
    files = [
        f.replace(".enc", "") for f in os.listdir(STORAGE)
        if f.endswith(".enc")
    ]
    return files