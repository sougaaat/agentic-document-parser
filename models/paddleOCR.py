from paddleocr import PaddleOCR

ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)

def invoke_paddleocr(file_path, confidence_threshold=0.8):
    result = ocr.predict(file_path)
    scores = {k:v for k,v in zip(result[0]['rec_texts'], result[0]['rec_scores'])}

    ## filter content that does not meet the confidence threshold
    high_scores = {k:v for k,v in scores.items() if v > confidence_threshold}
    raw_text = "\n".join(high_scores.keys())
    confidence_score = sum(scores.values())/len(scores) ## overall confidence score
    return raw_text, confidence_score, result

## ---- TEST APP ---
if __name__ == "__main__":
    input_one = "./data/handwritten.jpg"
    text, score, _ = invoke_paddleocr(input_one)

    print(f"Extracted text: {text}\n\nScore: {score}")