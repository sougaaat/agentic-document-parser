## import dependencies
from typing import TypedDict, List, Dict, Annotated, Literal
from operator import add

## graph schema
class DocumentState(TypedDict):
    file_path: str ## user_input
    validation_score_threshold: float ## user_input
    max_iterations_allowed: int ## user_input
    iterations: Annotated[int, add]
    file_type: Literal['plain_text', 'pdf', 'docx', 'img', 'html']
    raw_text: str
    successful_extraction: bool
    triggered_pdf2image: bool
    document_type: str
    document_schema: Dict
    structured_output: Dict
    validated_features: List[str]
    validation_score: float
    redacted_output: Dict
    redacted_features: List