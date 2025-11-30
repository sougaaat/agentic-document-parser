## import dependencies
import torch
from transformers import AutoProcessor, Qwen2_5_VLForConditionalGeneration
from olmocr.prompts import build_no_anchoring_v4_yaml_prompt
from PIL import Image
from typing import List, Dict

## setup environment
import os
from dotenv import load_dotenv
load_dotenv()

model_path = os.getenv('MODEL_PATH')

## load the models and processor
def load_model(model_path: str) -> Dict:
    final_output = {"models": None, "processor": None, "device": None, "message": ""}
    # Check if paths exist
    if not os.path.exists(model_path):
        final_output["message"] = f"Model doesn't exist at {model_path}"
        return final_output
    
    ## set the device type CPU/GPU
    if not torch.cuda.is_available():
        device = torch.device("cpu")
        device_map_config = "cpu"
        final_output["device"] = "cpu"
    else:
        device = torch.device("cuda")
        device_map_config = "auto"
        final_output["device"] = f"{torch.cuda.get_device_name(0)}"

    ## load the models
    processor = AutoProcessor.from_pretrained("Qwen/Qwen2-VL-7B-Instruct")
    final_output["processor"] = processor
    try:
        model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            model_path,
            device_map = "cuda",
            torch_dtype=torch.bfloat16
        )
        final_output["models"] = model
    except Exception as e:
       final_output["message"] = f"[ALERT] Model couldn't get loaded.\n\n\nDetails: {e}"
    
    return final_output


## serialize final output from the OCR to JSON compatible output
def serialize_output(model_response: str):

    raw_meta = model_response.split("---")[1].strip()
    ## metadata extraction
    metadata_final = dict()
    all_items = [item.strip() for item in raw_meta.split('\n')]
    for item in all_items:
        key, value = [item.strip() for item in item.split(":")]
        metadata_final[key] = value
    
    ## extraction of text from the image file
    extracted_raw_text = model_response.split("---")[-1].strip()

    ## final output
    return {"metadata": metadata_final, "extracted_raw_text": extracted_raw_text}

## validate input filepath (IMAGE)
def validate_input(image_path: str) -> Dict:
    ## handle -> no such file exists
    if not os.path.exists(image_path):
        return {"file": None, "message": f"[ALERT] No such file exists at {image_path}"}

    ## handle -> unsupported format
    if not image_path.endswith(('.jpg', '.png','.tiff')):
        return {"file": None, "message": "[ALERT] Unsupported file type. This application only supports .png, .jpg and .tiff."}
    
    ## handle -> loading fails
    try:
        input_image = Image.open(image_path).convert("RGB")
    except Exception as e:
        return {"file": None, "message": f"Error while loading the image file.\n\nDetails: {e}"}
    
    ## everything goes right
    return {"file": input_image, "message": "[INFO] Valid file path and file."}

## make inference
def make_inference(image_path: str, model_path = model_path) -> Dict:
    model, processor, device, load_message = load_model(model_path).values()
    file, message = validate_input(image_path).values()
    
    ## in case of any of the previously handled error
    if not file:
        return {"output": None, "message": message}

    ## prompt generation
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": build_no_anchoring_v4_yaml_prompt()},
                {"type": "image"},
            ],
        }
    ]

    ## set up input
    text_prompt = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(
        text=[text_prompt],
        images=[file], ## pass the PIL image object here
        padding=True,
        return_tensors="pt",
    ).to(model.device)

    ## make inference
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=2048)
    
    ## decode output
    # --- 7. Decode and Print ---
    prompt_length = inputs["input_ids"].shape[1]
    generated_tokens = output[:, prompt_length:]
    generated_text = processor.tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]

    ## post-processing on output
    final_output = serialize_output(generated_text)

    return final_output

##----------------------------------------------------------
if __name__=="__main__":
    user_input = input("> Enter the path of the image: ")
    metadata, rawtext = make_inference(image_path=user_input).values()
    print(f"> OCR Output:\n\nMetadata: {metadata}\n\nRaw Text: {rawtext}")