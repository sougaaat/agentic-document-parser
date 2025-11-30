## import dependencies
from langchain_core.runnables.base import RunnableLambda
from pydantic import BaseModel, Field, create_model
from typing import List, Dict, Literal
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.language_model import llm
from src.state_schema import DocumentState

## schema for pydantic object
class FieldDefinition(BaseModel):
    field_name: str = Field(default = '', description = 'Name of the required field for the Pydantic Schema')
    field_data_type: Literal['str', 'int', 'float', 'bool'] = Field(default = 'str', description="Data type of the required field for the Pydantic Schema")
class ExpectedOutput(BaseModel):
    fields: List[FieldDefinition] = Field(default = [], description='List of dictionaries of required fields and their respective data types')


## schema generator prompt template
with open("./prompts/schema_generator_agent_prompt.txt", "r") as f:
    schema_generator_prompt_template = f.read()

## serialize output in JSON
def serialize_dict(model_out: Dict) -> Dict:
    fields = dict()
    dtypes = {'str': str, 'int': int, 'float': float, 'bool': bool}
    for item in model_out['fields']:
        fields[item['field_name']] = dtypes[item['field_data_type']]
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
            "document_type": state["document_type"]
        }
    )
    return {"document_schema": resp}

if __name__=="__main__":
    initial_state = {"document_type": "Indian PAN Card"}
    doc_schema = schema_generator(state=initial_state)
    print(doc_schema)