## import dependencies
from langchain_cohere import ChatCohere

## setup environment
import os
from dotenv import load_dotenv
load_dotenv()
API_BACKEND = os.getenv('API_BACKEND')
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
assert API_BACKEND, "[ATTENTION] API BACKEND NOT FOUND!!"
assert COHERE_API_KEY, "[ATTENTION] COHERE_API_KEY NOT FOUND!!"

## model instance
llm = ChatCohere(temperature=0.01)
