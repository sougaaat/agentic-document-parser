"""
Flow of the application:
    1. Extractor Agent
        I. Input
            A. File Path (for now only images)
        II. Output: Extracted Raw Text, Confidence Score based on the extraction
    2. Classifier Agent
        I. Input:
            A. Raw Text (from Extractor Agent)
        II. Output: {'document_type': _, 'document_schema': _}
    3. Paser Agent
        I. Input:
            A. Raw Text (from Extractor Agent)
            B. Document Type (from classifier Agent)
            C. Document Schema (from classifier Agent)
        II. Output: Structured Output based on the Pydantic document schema
    4. Validator Agent:
        I. Input:
            A. Raw Text (from Extractor Agent)
            B. Document Type (from classifier Agent)
            C. Document Schema (from classifier Agent)
            D. Structured Output (from Parser Agent)
        II. Output: {"validation_score": _, "validated_structured_output": _} (Validation Score is based on custom logic defined below)
    5. Redactor Agent
        I. Input:
            A. Validated Structured Output (from Validator Agent)
            B. Document Type
        II. Identify PII (Personally Identifiable Information) fields
        III. Redact those fields
        IV. Output: {"redacted_output: _, "redacted_features": _}
    6. Reporter Agent
        I. Input:
            A. State
        II. Output: print entire state
"""

## import dependencies
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Dict, List
import requests
from pydantic import BaseModel, create_model
from langchain_cohere import ChatCohere
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

## setup environment
import os
from dotenv import load_dotenv
load_dotenv()
API_BACKEND = os.getenv('API_BACKEND')
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
assert API_BACKEND, "[ATTENTION] API BACKEND NOT FOUND!!"
assert COHERE_API_KEY, "[ATTENTION] COHERE_API_KEY NOT FOUND!!"

## prompts
with open("./prompts/classifier_agent_prompt.txt", "r") as f:
    classifier_prompt_template = f.read()

with open("./prompts/parser_agent_prompt.txt", "r") as f:
    parser_prompt_template = f.read()

## load the model
llm = ChatCohere(temperature=0.01)

## Pydantic Object to identify document type
class DocumentTypeIdentify(BaseModel):
    pass

## define graph
class DocumentState(TypedDict):
    file_path: str
    raw_text: str
    extraction_confidence_threshold: float
    api_status: str
    extraction_confidence_score: float
    document_type: str
    document_schema: Dict
    structured_output: Dict
    validation_score: float
    redacted_output: Dict
    redacted_features: List

## function definition for Extractor Agent
def extractor(state: DocumentState):
    paddle_ocr_url = API_BACKEND+"/paddleocr/parse"
    olmocr_url = API_BACKEND+"/olmocr/parse"
    """
    If the confidence_score_threshold is met then the loop will break
    """
    for ocr_url in (paddle_ocr_url, olmocr_url):
        resp = requests.post(ocr_url)
        if resp.status_code == 201:
            resp = resp.json()
            if resp['extraction_confidence_score'] >= state['extraction_confidence_threshold']:
                return {"raw_text": resp.json()['raw_text'], "extraction_confidence_score": resp.json()['extraction_confidence_score']}
        else:
            return {"api_state": "Down"}


## function definition for Classifier Agent
def classifier(state: DocumentState):
    output_parser = JsonOutputParser(pydantic_object=DocumentTypeIdentify)
    classifier_prompt = PromptTemplate(
        template=classifier_prompt_template,
        input_variables=["raw_text"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )
    chain = classifier_prompt | llm | output_parser
    resp = chain.invoke({"raw_text": state['raw_text']})
    return {"document_type": resp["document_type"], "document_schema": resp["document_schema"]}

## function definition for Parser Agent
def parser(state: DocumentState):
    pydantic_schema = create_model("DocumentSchema", **state["document_schema"])
    output_parser = JsonOutputParser(pydantic_object=pydantic_schema)
    parser_prompt = PromptTemplate(
        template=parser_prompt_template,
        input_variables=["raw_text", "document_type"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )
    chain = parser_prompt | llm | output_parser
    resp = chain.invoke(
        {
            "document_type": state["document_type"],
            "raw_text": state["raw_text"]
        }
    )
    return {"structured_output": resp}

## function definition for Validator Agent