## import dependencies
import os
from pathlib import Path
from pdf2image import convert_from_path
from src.resources import POPPLER_PATH
from src.agent_schema import DocumentState

def convert_pdf_to_image(state: DocumentState):
    ## if `temp` doesn't exists, create a directory
    temp_dir = os.path.join(os.getcwd(), 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    ## only convert the first page of the pdf to a png
    images = convert_from_path(state['file_path'], first_page=1, last_page=1, poppler_path=POPPLER_PATH)

    ## save the png in the 'temp' directory and return the file path
    image_file_path = os.path.join(temp_dir, 'page_1.png')
    images[0].save(image_file_path, 'PNG')

    return {'file_path': image_file_path, 'triggered_pdf2image': True}

## ---- TEST ----
if __name__=='__main__':
    dummy_file = './data/hand-written-parking-receipt.pdf'

    initial_state = {
        'file_path': dummy_file
    }

    image_path, status = convert_pdf_to_image(initial_state).values()
    print(f"Saved image at: {image_path}")