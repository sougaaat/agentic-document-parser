## import dependencies
from src.language_model import llm
from src.state_schema import DocumentState
from pydantic import create_model
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

## parser prompt
with open("./prompts/parser_agent_prompt.txt", "r") as f:
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
        "document_schema": {"aadhaar_number": int, "name": str, "father_name": str, "date_of_birth": str, "gender": str},
        "raw_text": """
        Indlan Govt iD  
        Aadhr No :  4823 9B7  1102
        Name :   SOUGAT  DE¥
        F/Name: Gopal  Dey
        DOB : 12/0B/19B9
        Gendr : M ALE 
        
        — uidai.g0v.in —
        """
    }
    results = parser(initial_state)
    print(results)