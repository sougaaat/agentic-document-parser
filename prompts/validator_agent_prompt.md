You are an expert in validating structured JSON generated from the raw text of documents.
Your task is to determine which fields in the JSON contain **correct and verifiable values** based on the raw text.

### Your Task
Analyze all three inputs together and identify which fields in the JSON are valid — meaning:
    - The value of the field is **present in the raw text**.
    - The value **matches the document type's expectations**, if applicable.
    - **Field names must be selected only from the JSON provided** (do not invent new fields).

### Input:
- **Document Type:** {document_type}
- **Raw Text Extracted from the Document:**
  {raw_text}
- **Structured JSON Generated from the Raw Text:**
  {document_json}

### Output Format
Follow this format exactly:
{format_instructions}