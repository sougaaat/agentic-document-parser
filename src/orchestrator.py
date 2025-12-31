## import dependencies
from src.agent_schema import DocumentState
from langgraph.graph import StateGraph, START, END

## import agents
from src.init_state import init_state
from src.format_identifier_agent import identify_format, format_router
from src.extractor_agent import simple_text_extractor, document_extractor, image_extractor, html_extractor
from src.pdf_to_image_agent import convert_pdf_to_image
from src.extraction_validator_agent import validate_extraction, validate_extraction_router
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

    graph.add_node("plain_text_extractor", simple_text_extractor)
    graph.add_node("document_extractor", document_extractor)
    graph.add_node("image_extractor", image_extractor)
    graph.add_node("html_extractor", html_extractor)

    graph.add_node("pdf2image_converter", convert_pdf_to_image)

    graph.add_node("extraction_validator", validate_extraction)
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
        path_map={
            "plain_text": "plain_text_extractor",
            "text_from_document": "document_extractor",
            "text_from_image": "image_extractor",
            "web_text_extraction": "html_extractor"
        },
    )

    graph.add_edge("plain_text_extractor", "extraction_validator")
    graph.add_edge("document_extractor", "extraction_validator")
    graph.add_edge("image_extractor", "extraction_validator")
    graph.add_edge("html_extractor", "extraction_validator")

    graph.add_edge("pdf2image_converter", "format_identifier")

    graph.add_conditional_edges(
        source="extraction_validator",
        path=validate_extraction_router,
        path_map={
            "PDF-to-Image": "pdf2image_converter",
            "FAILED": END,
            "SUCCESSFUL": "classifier"
        }
    )

    graph.add_edge("classifier", "schema_generator")
    graph.add_edge("schema_generator", "parser")
    graph.add_edge("parser", "validator")

    graph.add_conditional_edges(
        source="validator",
        path=validation_router,
        path_map={
            "retry": "format_identifier",
            "approved": "redactor"
        },
    )

    graph.add_edge("redactor", END)

    ## compile
    workflow = graph.compile()

    return workflow

## ---- TEST ----
if __name__ == "__main__":
    workflow = build_graph()
    with open("./output/graph.png", "wb") as f:
        f.write(workflow.get_graph().draw_mermaid_png())
    