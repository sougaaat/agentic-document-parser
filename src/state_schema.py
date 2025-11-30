## import dependencies
from typing import TypedDict, List, Dict


## define graph
class DocumentState(TypedDict):
    file_path: str
    # extraction_confidence_threshold: float
    raw_text: str
    api_live: bool
    # extraction_confidence_score: float
    document_type: str
    document_schema: Dict
    structured_output: Dict
    validated_features: List[str]
    validation_score: float
    redacted_output: Dict
    redacted_features: List