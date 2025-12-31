# ## import dependencies
from src.orchestrator import build_graph
import streamlit as st
import tempfile
import os
from json import dump

st.title("Agentic Document Parser")

if "button_status" not in st.session_state:
    st.session_state["button_disable"] = True

## input from the user's side
uploaded_file = st.file_uploader(
    label="Choose a file to extract",
    type=[".pdf", ".docx", ".png", ".jpeg", ".txt", ".md", ".html"]
)

validation_threshold = st.number_input("Pick a Validation Thresold", min_value=0.0, max_value=1.0, value=0.5, step=0.05)

max_iterations_allowed = st.number_input("Retries allowed", min_value=0, max_value=10, value=1, step=1)


## have to write the uploaded file into a temp file since Streamlit can't directly access the file path
if all([uploaded_file, validation_threshold, max_iterations_allowed]):
    suffix = os.path.splitext(uploaded_file.name)[1]

    temp_file_path = None
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.getbuffer())
        temp_file_path = tmp.name
    
    st.session_state["button_disable"] = False

submit = st.button("Submit", disabled=st.session_state["button_disable"])

if submit:
    initial_state = {
        "file_path": temp_file_path,
        "validation_score_threshold": validation_threshold,
        "max_iterations_allowed": max_iterations_allowed
    }

    workflow = build_graph()
    result = workflow.invoke(initial_state)

    if result['successful_extraction']:
        st.json(result)
    else:
        st.warning("Invalid Document!")

    ## clean up after execution
    if temp_file_path and os.path.exists(temp_file_path):
        os.remove(temp_file_path)