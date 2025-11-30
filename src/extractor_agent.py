## import dependencies
from src.state_schema import DocumentState
from src.language_model import API_BACKEND
import requests

## function definition for Extractor Agent
def extractor(state: DocumentState):
    # pytesseract_url = API_BACKEND + "/simpleOCR/parse"
    # paddle_ocr_url = API_BACKEND+"/paddleocr/parse"
    olmocr_url = API_BACKEND+"/olmocr/parse"

    ## hit API
    check_health = requests.get(API_BACKEND+"/olmocr/health")
    if check_health.status_code == 200:
        payload = {"file_path": state["file_path"]}
        response = requests.post(olmocr_url, json=payload)
        if response.status_code == 201:
            return {"raw_text": response.json()["rawtext"], "api_live": True}
        return None
    else:
            return {"raw_text": "<FAILED>", "api_live": False }

## ---- TEST ----
if __name__ == "__main__":
    initiate_state = {"file_path": "./data/dummy-pan-2.jpg"}
    result = extractor(initiate_state)
    print(result)