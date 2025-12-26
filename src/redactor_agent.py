## import dependencies
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from src.agent_schema import DocumentState
from src.resources import llm
from pydantic import BaseModel, Field
from typing import List
import copy

## redaction prompt
with open("./prompts/redaction_agent_prompt.md", "r") as f:
    redaction_prompt_template = f.read()

## schema for output
class RedactionSchema(BaseModel):
    redacted_features: List[str] = Field(
        default=[],
        description="List of field names from the document" \
        " JSON that contain Personally Identifiable Information aka PII and should be redacted."
    )

## function definition for the Redactor Agent
def redactor(state: DocumentState):
    output_parser = JsonOutputParser(pydantic_object=RedactionSchema)
    redaction_prompt = PromptTemplate(
        template=redaction_prompt_template,
        input_variables=["document_type", "document_json"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )
    chain = redaction_prompt | llm | output_parser
    resp = chain.invoke(
        {
            "document_type": state["document_type"],
            "document_json": state["structured_output"],
        }
    )
    # redacted_features = resp["redacted_features"]
    # redacted_output = {k:v for k, v in state["structured_output"].items() if k not in redacted_features}

    redacted_output = copy.deepcopy(state["structured_output"])
    for key in resp['redacted_features']:
        redacted_output[key] = '<REDACTED>'

    return {"redacted_output": redacted_output, "redacted_features": resp["redacted_features"]}

## ---- TEST -----
if __name__ == "__main__":
    # ## example one
    # initial_state = {
    #     "document_type":"Courier Delivery Receipt",
    #     "structured_output": {
    #       "tracking_id": "BLD-99231-44",
    #       "package_weight": "1.24kg",
    #       "ship_date": "14/09/24",
    #       "estimated_delivery": "16/09/24",
    #       "receiver_name": "Sougat Dey",
    #       "contact_number": "+91 98 07 44 2190",
    #       "delivery_address": "12/4B Laxmi Nagar, Kolkata 700082",
    #       "signature": "S Dey",
    #       "status": "Delivered",
    #       "otp": "4429",
    #       "remarks": "Gate was closed, customer came down",
    #       "fee_paid": "₹65.00",
    #       "payment_mode": "UPI (...2190)"
    #     }
    # }

    ## example two
    initial_state = {
        "document_type": "Indian Aadhaar Card",
        "structured_output": {'aadhaar_number': 123456789012, 'name': 'SURESH KUMAR VERMA', 'father_name': 'VINAY KUMAR VERMA', 'date_of_birth': '12/03/1992', 'gender': 'Male', 'address': 'H NO 45, STREET NO 2, LAJPAT NAGAR, NEW DELHI, DELHI 110024'}
    }

    result = redactor(initial_state)
    print(result)

    # """
    # Output:
    # ----------------- Example One -----------------
    # (agentic-document-parser) C:\Users\sodey\Downloads\_projects\agentic-document-parser>uv run -m src.redactor_agent
    # {'redacted_output': {'tracking_id': 'BLD-99231-44', 'package_weight': '1.24kg', 'ship_date': '14/09/24', 'estimated_delivery': '16/09/24', 'receiver_name': '<REDACTED>', 'contact_number': '<REDACTED>', 'delivery_address': '<REDACTED>', 'signature': '<REDACTED>', 'status': 'Delivered', 'otp': '<REDACTED>', 'remarks': 'Gate was closed, customer came down', 'fee_paid': '₹65.00', 'payment_mode': '<REDACTED>'}, 'redacted_features': ['receiver_name', 'contact_number', 'delivery_address', 'signature', 'otp', 'payment_mode']}
    #
    # Pretty JSON:
    # {
    #    "redacted_output":{
    #       "tracking_id":"BLD-99231-44",
    #       "package_weight":"1.24kg",
    #       "ship_date":"14/09/24",
    #       "estimated_delivery":"16/09/24",
    #       "receiver_name":"<REDACTED>",
    #       "contact_number":"<REDACTED>",
    #       "delivery_address":"<REDACTED>",
    #       "signature":"<REDACTED>",
    #       "status":"Delivered",
    #       "otp":"<REDACTED>",
    #       "remarks":"Gate was closed, customer came down",
    #       "fee_paid":"₹65.00",
    #       "payment_mode":"<REDACTED>"
    #    },
    #    "redacted_features":[
    #       "receiver_name",
    #       "contact_number",
    #       "delivery_address",
    #       "signature",
    #       "otp",
    #       "payment_mode"
    #    ]
    # }

    # ----------------- Example Two -----------------
    # (agentic-document-parser) C:\Users\sodey\Downloads\_projects\agentic-document-parser>uv run -m src.redactor_agent
    # {'redacted_output': {'aadhaar_number': 123456789012, 'name': 'SURESH KUMAR VERMA', 'father_name': 'VINAY KUMAR VERMA', 'date_of_birth': '12/03/1992', 'gender': 'Male', 'address': 'H NO 45, STREET NO 2, LAJPAT NAGAR, NEW DELHI, DELHI 110024'}, 'redacted_features': []}
    # 
    # Pretty JSON:
    # {
    #     "redacted_output":{
    #         "aadhaar_number":123456789012,
    #         "name":"SURESH KUMAR VERMA",
    #         "father_name":"VINAY KUMAR VERMA",
    #         "date_of_birth":"12/03/1992",
    #         "gender":"Male",
    #         "address":"H NO 45, STREET NO 2, LAJPAT NAGAR, NEW DELHI, DELHI 110024"
    #     },
    #     "redacted_features":[]
    # }
    # """