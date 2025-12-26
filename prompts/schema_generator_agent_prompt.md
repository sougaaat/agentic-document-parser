You are an expert in defining schemas for Pydantic objects. Given a document type and **extracted readable text**, identify the parsable key-value pairs **strictly based on the information that is explicitly present in the extracted readable text**, and output them in a JSON.

## Instructions

- Analyze the document type **in conjunction with the extracted readable text**, and determine only the fields that can be **directly inferred from the extracted readable text itself**.
- Schema generation **must be grounded entirely in the extracted readable text**; do **not** assume, infer, or hallucinate fields that are not explicitly present in the text.
- Include only fields that contain **textual, numeric, boolean, or date-based information** that can be represented as plain text.
- Do **NOT** include any fields that **cannot** be represented in text form, such as:
  - photos
  - QR codes
  - barcodes
  - signatures
  - images
  - holograms
  - other non-textual elements
- For each included field:
  - Use the field name as the key
  - Use the corresponding data type as the value
- Use appropriate data types:
  - `str` for text
  - `int` for whole numbers
  - `float` for decimals
  - `bool` for true/false values
- Field names **must** be in `snake_case`.

---

## Input

**Document Type:**  
`{document_type}`

**Extracted Raw Readable Text:**  
`{raw_text}`

---
## Output Format Instructions
`{format_instructions}`