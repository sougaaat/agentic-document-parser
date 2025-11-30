## import dependencies
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Dict
import uvicorn
import os

## import models
from models.olmOCR import make_inference, model_path
# from models.paddleOCR import invoke_paddleocr

## in case the models isn't downloaded
# from utils.download_olmocr import ModelSetup

## FastAPI App
app = FastAPI()


## Request Body Pydantic Schema
class InputPath(BaseModel):
    file_path: str = Field(pattern=r"\.(jpg|png|tiff)$")


## /health endpoint -> check if the models is running
@app.get("/olmocr/health", status_code=status.HTTP_200_OK)
async def check_health():
    if model_path is None or not os.path.exists(model_path) or len(os.listdir(model_path)) == 0:
        raise HTTPException(status_code=500, detail="Model not found! ⚠️")
    else:
        return {"status": "ok"}


# @app.get("/paddleocr/health", status_code=status.HTTP_200_OK)
# async def check_health():
#     return {"status": "ok"}


## /parse endpoints -> extract and structured output (using olmOCR)
@app.post("/olmocr/parse", status_code=status.HTTP_201_CREATED)
async def parse(image_path: InputPath):
    metadata, rawtext = make_inference(image_path=image_path.file_path).values()
    return {"metadata": metadata, "rawtext": rawtext}

# @app.post("/paddleocr/parse", status_code=status.HTTP_201_CREATED)
# async def parse(image_path: InputPath):
#     pass


### ------------------------------
if __name__ == '__main__':
    uvicorn.run(app="serve_OCRs:app", port=8050, reload=True)

##---- PENDING IMPLEMENTATION ----
"""the models should be available for auto download"""
