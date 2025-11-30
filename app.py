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
from src.state_schema import DocumentState
from langgraph.graph import StateGraph, START, END

## import agents
from src.extractor_agent import extractor
from src.classifier_agent import classifier
from src.schema_generator_agent import schema_generator
from src.parser_agent import parser
from src.validator_agent import validator
from src.redactor_agent import redactor

## define the Graph
graph = StateGraph(state_schema=DocumentState)

## add nodes
graph.add_node("extractor", extractor)
graph.add_node("classifier", classifier)
graph.add_node("schema_generator", schema_generator)
graph.add_node("parser", parser)
graph.add_node("validator", validator)
graph.add_node("redactor", redactor)

## add edges
graph.add_edge(START, "extractor")
graph.add_edge("extractor", "classifier")
graph.add_edge("classifier", "schema_generator")
graph.add_edge("schema_generator", "parser")
graph.add_edge("parser", "validator")
graph.add_edge("validator", "redactor")
graph.add_edge("redactor", END)

## compile
workflow = graph.compile()

if __name__ == "__main__":
    filepath = "./data/dummy-pan.png"
    initiate_state = {
        "file_path": filepath,
        "extraction_confidence_threshold": 0.7
    }
    results = workflow.invoke(initiate_state)
    print(results)