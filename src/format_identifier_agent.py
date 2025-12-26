## import dependencies
from src.agent_schema import DocumentState

## identify file extension
def identify_format(state: DocumentState):
    if state['file_path'].endswith('pdf'):
        return {'file_type': 'pdf', 'iterations': 1}
    elif state['file_path'].endswith(('png','jpg', 'jpeg')):
        return {'file_type': 'img', 'iterations': 1}
    else:
        return {'file_type': 'docx', 'iterations': 1}

def format_router(state: DocumentState):
    if state['file_type'] in ('pdf', 'docx'):
        return 'non_OCR_extraction'
    else:
        return 'OCR_extraction'