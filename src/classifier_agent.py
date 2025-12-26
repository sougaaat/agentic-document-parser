## import dependencies
from src.agent_schema import DocumentState
from src.resources import llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

## prompt for document classification
with open("./prompts/classifier_agent_prompt.md", "r") as f:
    classifier_prompt_template = f.read()

## Pydantic Object to identify document type
class DocumentTypeIdentify(BaseModel):
    document_type: str = Field(
        default="",
        description="The classified document type inferred from the raw extracted text."
    )

## function definition for Classifier Agent
def classifier(state: DocumentState):
    parser = JsonOutputParser(pydantic_object=DocumentTypeIdentify)
    classifier_prompt = PromptTemplate(
        template=classifier_prompt_template,
        input_variables=["raw_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = classifier_prompt | llm | parser
    resp = chain.invoke({"raw_text": state['raw_text']})
    return {"document_type": resp["document_type"]}

## ---- TESTING ----
if __name__=="__main__":
    initial_state = {
        "raw_text": """
        SUNSET CINEMA MULTIPLEX
        Screen 3 - IMAX
        
        Movie: DUNE: PART TWO
        Date: 24 Dec 2024
        Time: 7:30 PM
        
        Seat: G-15 (Premium)
        Ticket Type: Adult
        Price: ₹450.00
        
        Booking ID: SC24122401573
        GST: GSTIN 27AABCU9603R1ZM
        
        Food Combo Available at Counter
        Enjoy the show!
        
        [QR CODE]
        """
    }
    resp = classifier(initial_state)
    print(resp)

    # """
    # Output:
    # (agentic-document-parser) C:\Users\sodey\Downloads\_projects\agentic-document-parser>uv run -m src.classifier_agent
    # {'document_type': 'Movie Ticket'}
    # """