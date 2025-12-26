## import dependencies
from langchain_openai import ChatOpenAI
from langchain_cohere import ChatCohere

## setup environment
import os
from dotenv import load_dotenv
load_dotenv()

COHERE_API_KEY = os.getenv('COHERE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
assert COHERE_API_KEY, "[ATTENTION] COHERE API NOT FOUND!!"
assert OPENAI_API_KEY, "[ATTENTION] OPENAI API NOT FOUND!!"
os.environ['COHERE_API_KEY'] = COHERE_API_KEY
os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY

## model instance
llm = ChatCohere(temperature=0.01)

## for OCR
ocr_llm = ChatOpenAI(temperature=0.01, model="gpt-4.1-nano")