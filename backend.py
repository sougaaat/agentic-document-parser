## import dependencies
from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.orchestrator import build_graph
import uvicorn
from pydantic import BaseModel, Field, ValidationError
from typing import Dict, Any

app = FastAPI()

## enable CORS
origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## request schema
class GraphInput(BaseModel):
    file_path: str
    validation_score_threshold: float = Field(ge=0.3, le=1.0)
    max_iterations_allowed: int = Field(ge=2, le=10)

## health endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
def check_health():
    return {"status": "ok"}

## parse endpoint
@app.post("/parse", status_code=status.HTTP_201_CREATED)
def parse_doc(request: GraphInput):    
    ## request body validation
    try:
        initial_state = {
            "file_path": request.file_path,
            "validation_score_threshold": request.validation_score_threshold,
            "max_iterations_allowed": request.max_iterations_allowed
        }

        workflow = build_graph()
        result: Dict[str, Any] = workflow.invoke(initial_state)

        ## in case of invalid document
        if not result['successful_extraction'] or result.get('document_type', "Invalid Document") == "Invalid Document":
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid Document")

        else:
            """
            `result` includes the entire state of the LangGraph output. But the user should only be concerned
            with the final redacted output.
            """
            return {"parsed_output": result["redacted_output"]}
    
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


if __name__ == "__main__":
    uvicorn.run(app="backend:app", host="0.0.0.0", port=8000, reload=True)