## import dependencies
from src.agent_schema import DocumentState

## function definition for extraction validator agent and the router
def validate_extraction(state: DocumentState):
    if state['raw_text'].strip() == '':
        return {"successful_extraction": False}
    else:
        return {"successful_extraction": True}

def validate_extraction_router(state: DocumentState):
    if not state['successful_extraction'] and state['file_type'] == 'pdf' and not state['triggered_pdf2image']:
        return "PDF-to-Image"
    elif not state['successful_extraction']:
        return "FAILED"
    else:
        return "SUCCESSFUL"