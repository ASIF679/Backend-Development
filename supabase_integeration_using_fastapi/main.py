from fastapi import FastAPI, File, UploadFile
import redis
import redis.exceptions
from uuid import uuid4
from fastapi import HTTPException
import os, shutil, json 
app = FastAPI()

#Connect to Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
# Directories and queue name
UPLOAD_DIR = "uploaded_files"
METADATA_DIR = "metadata"
QUEUE_NAME = "file_queue"

# check wether directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(METADATA_DIR, exist_ok=True)

# Test FastAPI
@app.get("/fastapi-status")
def test_fastapi():
    return {"message": "FastAPI is running"}

# Test Redis
@app.get("/redis-health")
def redis_health():
    try:
        response = r.ping()
        return {"status": "connected", "ping": response}
    except redis.exceptions.ConnectionError:
        return {"status": "disconnected", "ping": False}

# Upload file + save metadata + push to Redis queue
@app.post("/upload-file")
async def upload_file(file: UploadFile):
    try:
        file_id = str(uuid4())
        # Create unique filename to avoid conflicts
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{file_id}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        metadata_path = os.path.join(METADATA_DIR, f"{file_id}.json")

        # Save uploaded file with unique name
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Create metadata with both original and stored filenames
        metadata = {
            "uuid": file_id,
            "original_filename": file.filename,
            "stored_filename": unique_filename,
            "file_path": file_path,
            "status": "pending"
        }

        # Save metadata to JSON
        with open(metadata_path, "w") as meta_file:
            json.dump(metadata, meta_file, indent=2)

        # Push UUID to Redis queue
        r.lpush(QUEUE_NAME, file_id)
        return {
            "message": "File uploaded successfully",
            "uuid": file_id,
            "original_filename": file.filename,
            "stored_filename": unique_filename,
            "metadata_path": metadata_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# Route for viewing the metadata json format
@app.get("/metadata/{uuid}")
def get_metadata(uuid: str):
    metadata_path = os.path.join(METADATA_DIR, f"{uuid}.json")
    
    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="Metadata not found")
    
    try:
        with open(metadata_path, "r") as meta_file:
            metadata = json.load(meta_file)
        return metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading metadata: {str(e)}")

# Route for viewing the Redis queue
# @app.get("/queue")
# def get_queue():
#     try:
#         queue_items = r.lrange(QUEUE_NAME, 0, -1)
#         return {"queue": queue_items, "count": len(queue_items)}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error accessing queue: {str(e)}")

# Route to check file processing status
@app.get("/status/{uuid}")
def get_status(uuid: str):
    metadata_path = os.path.join(METADATA_DIR, f"{uuid}.json")
    
    if not os.path.exists(metadata_path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        with open(metadata_path, "r") as meta_file:
            metadata = json.load(meta_file)
        return {"uuid": uuid, "status": metadata.get("status", "unknown")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading status: {str(e)}")