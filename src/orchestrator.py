## import dependencies
from src.agent_schema import DocumentState
from langgraph.graph import StateGraph, START, END

## import agents
from src.init_state import init_state
from src.format_identifier_agent import identify_format, format_router
from src.extractor_agent import document_extractor, image_extractor
from src.classifier_agent import classifier
from src.schema_generator_agent import schema_generator
from src.parser_agent import parser
from src.validator_agent import validator, validation_router
from src.redactor_agent import redactor

## define the Graph
def build_graph():
    graph = StateGraph(state_schema=DocumentState)

    ## add nodes
    graph.add_node("init_state", init_state)
    graph.add_node("format_identifier", identify_format)
    graph.add_node("document_extractor", document_extractor)
    graph.add_node("image_extractor", image_extractor)
    graph.add_node("classifier", classifier)
    graph.add_node("schema_generator", schema_generator)
    graph.add_node("parser", parser)
    graph.add_node("validator", validator)
    graph.add_node("redactor", redactor)

    ## add edges
    graph.add_edge(START, "init_state")

    graph.add_edge("init_state", "format_identifier")

    graph.add_conditional_edges(
        source="format_identifier",
        path=format_router,
        path_map={"non_OCR_extraction": "document_extractor", "OCR_extraction": "image_extractor"},
    )

    graph.add_edge("document_extractor", "classifier")
    graph.add_edge("image_extractor", "classifier")

    graph.add_edge("classifier", "schema_generator")
    graph.add_edge("schema_generator", "parser")
    graph.add_edge("parser", "validator")

    graph.add_conditional_edges(
        source="validator",
        path=validation_router,
        path_map={"retry": "format_identifier", "approved": "redactor"},
    )

    graph.add_edge("redactor", END)

    ## compile
    workflow = graph.compile()

    return workflow

## ---- TEST ----
if __name__ == "__main__":
    workflow = build_graph()
    