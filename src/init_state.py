from src.agent_schema import DocumentState

## set the default iteration value as 0
def init_state(state: DocumentState):
    return {
        **state,
        "iterations": 0
    }