import redis
import os
import json
import time
import PyPDF2
from datetime import datetime
print("Worker function started")
def start_worker():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    UPLOAD_DIR = "uploaded_files"
    METADATA_DIR = "metadata"
    QUEUE_NAME = "file_queue"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(METADATA_DIR, exist_ok=True)
    print("Worker started. Waiting for files...")

    while True:
        try:
            # Block and wait for items in the queue
            item = r.brpop(QUEUE_NAME, timeout=0)
            if item:
                _, file_uuid = item  # Unpack the tuple to get only the UUID
                print(f"Received UUID: {file_uuid}")
                metadata_path = os.path.join(METADATA_DIR, f"{file_uuid}.json")
            
                # Check if metadata file exists
                if not os.path.exists(metadata_path):
                    print(f"Metadata file not found for UUID: {file_uuid}")
                    continue

                # Load metadata
                try:
                    with open(metadata_path, "r") as meta_file:
                        metadata = json.load(meta_file)
                except Exception as e:
                    print(f"Error reading metadata for UUID {file_uuid}: {e}")
                    continue
                
                # Update status to processing
                metadata["status"] = "processing"
                metadata["processing_started"] = datetime.now().isoformat()
                
                try:
                    with open(metadata_path, "w") as meta_file:
                        json.dump(metadata, meta_file, indent=2)
                except Exception as e:
                    print(f"Error updating metadata to processing: {e}")
                    continue
                
                print(f"Processing file: {metadata.get('original_filename', 'Unknown')}")
                
                # Use the stored filename from metadata
                stored_filename = metadata.get("stored_filename")
                if not stored_filename:
                    print(f"No stored filename found in metadata for UUID: {file_uuid}")
                    continue
                pdf_path = os.path.join(UPLOAD_DIR, stored_filename)
                
                # Check if file actually exists
                if not os.path.exists(pdf_path):
                    print(f"File not found: {pdf_path}")
                    metadata["status"] = "failed"
                    metadata["error"] = "File not found"
                    metadata["processing_completed"] = datetime.now().isoformat()
                    
                    with open(metadata_path, "w") as meta_file:
                        json.dump(metadata, meta_file, indent=2)
                    continue
                
                # Extract content from PDF
                content = ""
                try:
                    with open(pdf_path, "rb") as pdf_file:
                        reader = PyPDF2.PdfReader(pdf_file)
                        page_count = len(reader.pages)
                        
                        for page_num, page in enumerate(reader.pages):
                            try:
                                page_text = page.extract_text() or ""
                                content += page_text
                                print(f"Processed page {page_num + 1}/{page_count}")
                            except Exception as e:
                                print(f"Error extracting text from page {page_num + 1}: {e}")
                                continue
                        
                        if not content.strip():
                            content = "No text content found in PDF."
                            
                except Exception as e:
                    print(f"Error reading PDF {pdf_path}: {e}")
                    content = f"Failed to extract content: {str(e)}"
                    metadata["status"] = "failed"
                    metadata["error"] = str(e)
                else:
                    metadata["status"] = "completed"
                
                # Update metadata with results
                metadata["content"] = content
                metadata["content_length"] = len(content)
                metadata["processing_completed"] = datetime.now().isoformat()
                
                try:
                    with open(metadata_path, "w") as meta_file:
                        json.dump(metadata, meta_file, indent=2)
                    print(f"Finished processing: {metadata.get('original_filename', 'Unknown')} - Status: {metadata['status']}")
                except Exception as e:
                    print(f"Error saving final metadata: {e}")

        except KeyboardInterrupt:
            print("Worker stopped by user")
            break
        except Exception as e:
            print(f"Worker error: {e}")
            time.sleep(1)  # Small delay to prevent rapid error loops

if __name__ == "__main__":
    start_worker()
