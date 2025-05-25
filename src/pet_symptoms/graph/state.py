from typing import List, Optional
from langgraph.graph import MessagesState

class PetSymptomsState(MessagesState):
    """State for pet symptoms collection workflow."""
    pet_type: Optional[str]  # Type of pet (e.g., dog, cat)
    pet_name: Optional[str]  # Name of the pet
    symptoms: List[str]  # List of reported symptoms
    severity: Optional[str]  # Severity of symptoms (mild, moderate, severe)
    duration: Optional[str]  # How long the symptoms have been present
    additional_info: Optional[str]  # Any additional information provided
    current_question: Optional[str]  # Current question being asked
    conversation_history: List[dict]  # History of the conversation
    current_input: str  # Current user input
    is_complete: bool  # Whether the workflow is complete
    extracted_info: dict  # Information extracted by LLM from user input 