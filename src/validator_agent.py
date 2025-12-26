## import dependencies
from langchain_core.prompts import PromptTemplate
from src.resources import llm
from src.agent_schema import DocumentState
from pydantic import BaseModel, Field
from typing import List
from langchain_core.output_parsers import JsonOutputParser

## validator agent prompt
with open("./prompts/validator_agent_prompt.md", "r") as f:
    validator_agent_prompt = f.read()

## validation schema
class ValidationSchema(BaseModel):
    valid_fields: List[str] = Field(
        default=[],
        description=(
            "List of field names from the provided JSON whose values are verified as correct "
            "based on the raw text of the document. Only include field names that appear in "
            "the JSON and whose values can be confidently matched or validated against the "
            "extracted raw text and the expected structure of the specified document type."
        )
    )

## function definition for the validator agent
def validator(state: DocumentState):
    output_parser = JsonOutputParser(pydantic_object=ValidationSchema)
    validator_prompt = PromptTemplate(
        template=validator_agent_prompt,
        input_variables=["document_type", "raw_text", "document_json"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()},
    )
    chain = validator_prompt | llm | output_parser
    resp = chain.invoke(
        {
            "document_type": state["document_type"],
            "raw_text": state["raw_text"],
            "document_json": state["structured_output"],
        }
    )
    validation_score = round(len(resp["valid_fields"])/len(state["document_schema"]), 3)
    return {"validated_features": resp["valid_fields"], "validation_score": validation_score}

def validation_router(state: DocumentState):
    if (state['validation_score'] < state['validation_score_threshold']) or (state['max_iterations_allowed'] < state['iterations']):
        return "retry"
    else:
        return "approved"

## ---- TEST -----
if __name__ == "__main__":
    initial_state = {
        "document_type": "Indian Aadhaar Card",
        "document_schema": {"aadhaar_number": int, "name": str, "father_name": str, "date_of_birth": str,
                            "gender": str, "address": str},
        "raw_text": """
            Indlan Govt iD  
            Aadhr No :  4823 9B7  1102
            Name :   SOUGAT  DE¥
            F/Name: Gopal  Dey
            DOB : 12/0B/19B9
            Gendr : M ALE
            
            Kolkata, 
            West Bengal

            — uidai.g0v.in —
            """,
        "structured_output": {'aadhaar_number': 4823971102, 'name': 'SOUGAT DEY', 'father_name': 'Gopal Dey', 'date_of_birth': '12/08/1989', 'gender': 'MALE', 'address': ''},
    }
    result = validator(initial_state)
    print(result)

    # """
    # (agentic-document-parser) C:\Users\sodey\Downloads\_projects\agentic-document-parser>uv run -m src.validator_agent
    # {'validated_features': ['aadhaar_number', 'name', 'father_name', 'date_of_birth', 'gender'], 'validation_score': 0.833}

    # Pretty JSON:
    # {
    #     "validated_features":[
    #         "aadhaar_number",
    #         "name",
    #         "father_name",
    #         "date_of_birth",
    #         "gender"
    #     ],
    #     "validation_score":0.833
    # }

    # Explanation: The `validation_score` is 0.833 is because the structured output does not have a key for the key `address`, therefore validation score is 5/6 ≈ 0.833.
    # """