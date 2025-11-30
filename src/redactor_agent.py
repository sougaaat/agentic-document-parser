## import dependencies
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from src.state_schema import DocumentState
from src.language_model import llm
from pydantic import BaseModel, Field
from typing import List

## redaction prompt
with open("./prompts/redaction_agent_prompt.txt", "r") as f:
    redaction_prompt_template = f.read()

## schema for output
class RedactionSchema(BaseModel):
    redacted_features: List[str] = Field(
        default=[],
        description="List of field names from the document JSON that contain PII and should be redacted."
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
    redacted_features = resp["redacted_features"]
    redacted_output = {k:v for k, v in state["structured_output"].items() if k not in redacted_features}
    return {"redacted_output": redacted_output, "redacted_features": redacted_features}

## ---- TEST -----
if __name__ == "__main__":
    initial_state = {
        "document_type":"Courier Delivery Receipt",
        "structured_output": {
          "tracking_id": "BLD-99231-44",
          "package_weight": "1.24kg",
          "ship_date": "14/09/24",
          "estimated_delivery": "16/09/24",
          "receiver_name": "Sougat Dey",
          "contact_number": "+91 98 07 44 2190",
          "delivery_address": "12/4B Laxmi Nagar, Kolkata 700082",
          "signature": "S Dey",
          "status": "Delivered",
          "otp": "4429",
          "remarks": "Gate was closed, customer came down",
          "fee_paid": "₹65.00",
          "payment_mode": "UPI (...2190)"
        }
    }
    result = redactor(initial_state)
    print(result)