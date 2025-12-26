## import dependencies
from src.resources import llm
from src.agent_schema import DocumentState
from pydantic import create_model
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

## parser prompt
with open("./prompts/parser_agent_prompt.md", "r") as f:
    parser_prompt_template = f.read()

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

## ---- TEST ----
if __name__ == "__main__":
    initial_state = {
        "document_type": "Indian Aadhaar Card",
        "document_schema": {"aadhaar_number": int, "name": str, "father_name": str, "date_of_birth": str, "gender": str, "address": str},
        "raw_text": """
        GOVERNMENT OF INDIA
        UNIQUE IDENTIFICATION AUTHORITY OF INDIA

        Name
        SURESH KUMAR
        VERMA

        FATHER
        VINAY KUMAR                                 VERMA

        DOB
        12 / 03 / 1992

        Male

        Aadhaar No
        1234 5678 9012

        Address
        H NO 45
        STREET NO 2
        LAJPAT NAGAR
        NEW DELHI
        DELHI 110024

        Signature

        """
    }
    results = parser(initial_state)
    print(results)

    # """
    # (agentic-document-parser) C:\Users\sodey\Downloads\_projects\agentic-document-parser>uv run -m src.parser_agent
    # {'structured_output': {'aadhaar_number': 123456789012, 'name': 'SURESH KUMAR VERMA', 'father_name': 'VINAY KUMAR VERMA', 'date_of_birth': '12/03/1992', 'gender': 'Male', 'address': 'H NO 45, STREET NO 2, LAJPAT NAGAR, NEW DELHI, DELHI 110024'}}

    # Pretty JSON:
    # {
    #     "structured_output":{
    #         "aadhaar_number":123456789012,
    #         "name":"SURESH KUMAR VERMA",
    #         "father_name":"VINAY KUMAR VERMA",
    #         "date_of_birth":"12/03/1992",
    #         "gender":"Male",
    #         "address":"H NO 45, STREET NO 2, LAJPAT NAGAR, NEW DELHI, DELHI 110024"
    #     }
    # }
    # """