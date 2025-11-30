## import dependencies
from PIL import Image
import pytesseract

## environment setup
import os
from dotenv import load_dotenv
load_dotenv()
tesseract_path = os.getenv("TESSERACT_PATH")
assert tesseract_path, "[ATTENTION] TESSERACT PATH ISN'T FOUND!"
os.environ["TESSERACT_PATH"] = tesseract_path

## pytesseract PATH
pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_path, "tesseract.exe")

## parse
parsed_text = pytesseract.image_to_string(Image.open("./data/dummy-pan-2.jpg"))
print(parsed_text)