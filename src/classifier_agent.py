## import dependencies
from src.state_schema import DocumentState
from src.language_model import llm
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

## prompt for document classification
with open("./prompts/classifier_agent_prompt.txt", "r") as f:
    classifier_prompt_template = f.read()

## Pydantic Object to identify document type
class DocumentTypeIdentify(BaseModel):
    document_type: str = Field(
        default="",
        description="The classified document type inferred from the raw extracted text, such as Aadhaar, PAN, Passport, Invoice, or Parking Receipt."
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
        GOVT COLLEGE OF ARTS & SCI
        STUDENT ID CARD
    
        Name: Sougat D
        Dept: Comp Sci
        RegNo: 21CS041
        Blood: B+
        Valid till: 2026
    
        (barcode smudged)
        """
    }
    resp = classifier(initial_state)
    print(resp)