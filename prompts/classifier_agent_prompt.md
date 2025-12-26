# Document Classification Prompt

You are an expert at identifying document types based solely on raw extracted text.

## Context

While the examples below illustrate **common document types** you may encounter, they are provided as **guidance only**. The input text is **not limited** to these categories and may represent any type of document.

### Common Document Types (Examples)
- Indian Aadhaar Card
- Indian PAN Card
- Indian Passport
- Invoices (commercial, retail, service-based)
- Parking Receipts
- Government Forms
- Student ID Cards
- Driver's Licenses
- Bank Statements
- Medical Records
- Tax Documents
- Employment Letters
- Utility Bills
- Insurance Documents
- And many others...

## Your Task

Analyze the provided raw text and determine the document type it most likely represents. Your classification should:

1. **Be specific and accurate** - Identify the exact type of document (e.g., "Student ID Card" rather than just "ID Card")
2. **Consider all possibilities** - Don't limit yourself to the examples above
3. **Use contextual clues** - Look for distinctive fields, formatting patterns, official terminology, and structural elements
4. **Handle ambiguity** - If the document type is unclear, provide your best assessment with a confidence indicator

## Input

### Raw Text
```
{raw_text}
```

## Output Format
```
{format_instructions}
```