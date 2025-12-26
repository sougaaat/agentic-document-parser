# Agentic Document Parser

An end-to-end agentic document understanding system capable of extracting text from documents, classifying document types, generating schemas, parsing raw text into structured JSON, validating extracted fields, and redacting PII. The system is composed of multiple specialized agents working together to produce reliable and privacy-safe document outputs.

**Important Note:**  
The first run will take **at least 15 minutes** because `olmOCR` is a heavy model and relies on the Qwen Vision-Language Model (VLM) internally. After the initial model download and setup, subsequent runs are much faster.

# Flow of the application:
1. Extractor Agent
   - Input: File Path (for now only images)
   - Output: Extracted Raw Text, Confidence Score based on the extraction
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

---

## Graph Flow
                                 +-----------+                        
                                 | __start__ |                        
                                 +-----------+                        
                                        *                             
                                        *                             
                                        *                             
                                 +------------+                       
                                 | init_state |                       
                                 +------------+                       
                                        *                             
                                        *                             
                                        *                             
                             +-------------------+                    
                             | format_identifier |                    
                            .+-------------------+..                  
                        ....            .           .....             
                   .....                 .               ....         
                ...                      .                   .....    
+--------------------+          +-----------------+               ... 
| document_extractor |          | image_extractor |                 . 
+--------------------+          +-----------------+                 . 
                  ***            ***                                . 
                     **        **                                   . 
                       **    **                                     . 
                   +------------+                                   . 
                   | classifier |                                   . 
                   +------------+                                   . 
                          *                                         . 
                          *                                         . 
                          *                                         . 
                +------------------+                                . 
                | schema_generator |                                . 
                +------------------+                                . 
                          *                                         . 
                          *                                         . 
                          *                                         . 
                     +--------+                                   ... 
                     | parser |                              .....    
                     +--------+*                         ....         
                                ***                 .....             
                                   **          .....                  
                                     **     ...                       
                                 +-----------+                        
                                 | validator |                        
                                 +-----------+                        
                                        .                             
                                        .                             
                                        .                             
                                  +----------+                        
                                  | redactor |                        
                                  +----------+                        
                                        *                             
                                        *                             
                                        *                             
                                  +---------+                         
                                  | __end__ |                         
                                  +---------+   
---

## Quick Start

### Prerequisites
- Python 3.10+
- `uv` package manager
- Internet connection for the initial olmOCR model download
- GPU recommended for improved performance (not required)

### Run Instructions

1. Start the OCR API backend:
   ```bash
   uv run serve_OCRs.py
   ```

2. Start the main application:
   ```bash
   uv run orchestrator.py
   ```

---

## Project Structure

```
agentic-document-parser/
│
├── data/                 # Sample input files and datasets
├── demo/                 # Demonstrations and examples
├── exclaidraw/           # Future scope of the project (workflows/UI expansion)
├── legacy-builds/        # Deprecated or older builds
├── models/               # Model configs and related assets
├── notebooks/            # Experiments, exploration, and prototyping
├── output/               # Parsed results, JSON output, logs
├── prompts/              # Prompt templates for all agents
├── src/                  # Function definition scripts for different agents
│
├── utils/                # Utility modules
│   ├── download_olmocr.py
│   ├── gpu_availability.py
│   └── path_generator.py
│
├── app.py                # Main application entrypoint
├── serve_OCRs.py         # Local OCR backend powered by olmOCR
├── requirements.txt       # Package dependencies
├── pyproject.toml         # Project configuration and metadata
└── README.md              # Project documentation
```

### Special Directories

#### `exclaidraw/`
Reserved for future extensions, including visual workflows, UI components, and interaction diagrams.

#### `src/`
Contains all core agent logic. This includes:
- Extractor agent
- Classifier agent
- Schema generator agent
- Parser agent
- Validator agent
- Redactor agent

---

## System Overview

The system consists of six coordinated agents:

1. **Extractor Agent**  
   Extracts textual content from documents using olmOCR (powered by Qwen VLM).

2. **Classifier Agent**  
   Determines the likely document type using the extracted text.

3. **Schema Generator Agent**  
   Produces a generalized schema that documents of the detected type should follow.

4. **Parser Agent**  
   Converts the extracted raw text into a structured JSON format, using:
   - Extracted text  
   - Predicted document type  
   - Generated schema

5. **Validator Agent**  
   Checks whether all required schema fields have been successfully extracted and computes a validation score.

6. **Redactor Agent**  
   Detects and redacts PII fields, producing a clean and privacy-safe output.

---

## Installation (Optional)

To install dependencies manually:

```bash
uv pip install -r requirements.txt
```

---

## Notes

- The OCR workload is heavy on first run; allow at least 15 minutes for model download and initialization.
- GPU support significantly speeds up parsing, but CPU-only execution is fully supported.