## import dependencies
from langchain_core.messages import HumanMessage
from src.agent_schema import DocumentState
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from src.resources import ocr_llm
import base64

## pdf/docx loader
def document_extractor(state: DocumentState):
    if state['file_type'] == 'pdf':
        loader = PyPDFLoader(file_path=state['file_path'])
    else:
        loader = Docx2txtLoader(file_path=state['file_path'])

    raw_text = ""
    docs = loader.load()
    for doc in docs:
        raw_text += doc.page_content
    return {'raw_text': raw_text}
    
## text extraction from image using GPT 4.1 Nano
def image_extractor(state: DocumentState):
    ## open the images in base64
    with open(state["file_path"], "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()

    ## construct image url for the language model
    image_url = f"data:image/png;base64,{image_base64}" if state['file_path'].endswith(".png") else f"data:image/jpeg;base64,{image_base64}"

    ## send the prompt + image url in a message format
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Extract all readable text from this receipt."},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    )

    resp = ocr_llm.invoke([message])
    return {'raw_text': resp.content}

## ---- TEST ----
if __name__ == "__main__":
    # ## text extraction from documents(pdf, docx)
    # initial_state = {
    #     "file_type": "docx",
    #     "file_path": "./data/GenAI Engineer Learning Path Beginnerv0.3.docx"
    # }
    # result = document_extractor(initial_state)

    ## text extraction from images(png, jpg, jpeg)
    initial_state = {
        "file_type": "png",
        "file_path": "./data/hand-written-parking-receipt.jpg"
    }
    result = image_extractor(initial_state)

    ## print extracted text
    print(result['raw_text'])

    # """
    # (agentic-document-parser) C:\Users\sodey\Downloads\_projects\agentic-document-parser>uv run -m src.extractor_agent
    # Parking Ticket
    # Entry Time: 11:05 AM
    # Exit Time: 12:30 PM
    # Charges: Rs. 120
    # Category: Car
    # """