## import dependencies
from langchain_core.runnables.base import RunnableLambda
from pydantic import BaseModel, Field
from typing import List, Dict, Literal, Union
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.resources import llm
from src.agent_schema import DocumentState

## schema for pydantic object
class FieldDefinition(BaseModel):
    field_name: str = Field(default = '', description = 'Name of the required field for the Pydantic Schema')
    field_data_type: Literal['str', 'int', 'float', 'bool'] = Field(default = 'str', description="Data type of the required field for the Pydantic Schema")

class ExpectedOutput(BaseModel):
    fields: List[FieldDefinition] = Field(default = [], description='List of dictionaries of required fields and their respective data types')


## schema generator prompt template
with open("./prompts/schema_generator_agent_prompt.md", "r") as f:
    schema_generator_prompt_template = f.read()

## serialize output in JSON
def serialize_dict(model_out: Dict[str, List[Dict[str, str]]]) -> Dict[str, Union[str, int, float, bool]]:
    ## example of `model_out` -> {'fields': [{'name': 'str', 'pan_number': 'str}, ..., {'date_of_birth': 'str'}]}
    fields = dict()
    for item in model_out['fields']:
        fields[item['field_name']] = eval(item['field_data_type'])
    return fields

## chain for the output
def initiate_chain(model, serialization=serialize_dict):
    parser = JsonOutputParser(pydantic_object=ExpectedOutput)
    prompt = PromptTemplate(
        template=schema_generator_prompt_template,
        input_variables=['document_type'],
        partial_variables={'format_instructions': parser.get_format_instructions()}
    )
    chain = prompt | model | parser | RunnableLambda(serialization)
    return chain

## schema generator agent
def schema_generator(state: DocumentState):
    schema_chain = initiate_chain(model=llm)
    resp = schema_chain.invoke(
        {
            "document_type": state['document_type'],
            "raw_text": state['raw_text']
        }
    )
    return {"document_schema": resp}

if __name__=="__main__":
    initial_state = {
        "document_type": "Indian PAN Card",
        "raw_text": """
        INCOME TAX DEPARTM ENT
        GOVT OF INDIA

        PERMANENT ACCOUNT NUMB ER CARD

        Name
        RAHUL KUMAR
        SHARMA

        Father s Name
        ANIL KUMAR SHARMA

        Date of Birth
        14 / 08 / 1996

        PAN
        ABCPSI234F

        Signature
        RAHUL K SHARMA
        """
    }
    doc_schema = schema_generator(state=initial_state)
    print(doc_schema)