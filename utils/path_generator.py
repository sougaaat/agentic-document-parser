import os
from dotenv import load_dotenv
from typing import Dict

def generate(url: str) -> Dict:
    file_name = url.split("/")[-1]
    zip_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", file_name)
    extract_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
    model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", os.path.splitext(file_name)[0])
    return {"zip_path": zip_path, "extract_path": extract_path,  "model_path": model_path}

if __name__=="__main__":
    load_dotenv()
    model_url = os.getenv("model_url")
    zip_path, extract_path, model_path = generate(url=model_url).values()
    print(generate(url=model_url))