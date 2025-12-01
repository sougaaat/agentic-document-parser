## What I have completed so far
- Script to check if the GPU is available
- Created a FastAPI backend for serving olmOCR
    - Script to generate paths given just the URL of the model in cloud -> to assist in managing the paths
    - Script to download the model -> in case of the model is not available locally
    - Model inference is written in different script


## Pending
- Need similar FastAPI Interface for Docling as well
- Need similar FastAPI Interface for Paddle OCR as well (For not so complicated need of OCR capability)
- Validator
    - If the extracted content is any good
    - If the schema is right for that particular document type
- Schema Database -> to stop regenerating the schema every time for same type of documents
- figure out the 