## import dependencies
from src.agent_schema import DocumentState

## identify file extension
def identify_format(state: DocumentState):
    if state['file_path'].endswith('pdf'):
        return {'file_type': 'pdf', 'iterations': 1}
    elif state['file_path'].endswith(('png','jpg', 'jpeg')):
        return {'file_type': 'img', 'iterations': 1}
    elif state['file_path'].endswith('.docx'):
        return {'file_type': 'docx', 'iterations': 1}
    elif state['file_path'].endswith(('.txt', '.md')):
        return {'file_type': 'plain_text', 'iterations': 1}
    else:
        return {'file_type': 'html', 'iterations': 1}

def format_router(state: DocumentState):
    if state['file_type'] in ('pdf', 'docx'):
        return 'text_from_document'
    elif state['file_type'] == 'img':
        return 'text_from_image'
    elif state['file_type'] == 'plain_text':
        return 'plain_text'
    else:
        return 'web_text_extraction'