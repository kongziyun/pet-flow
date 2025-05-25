from typing import Literal
import logging
from langgraph.types import Command
from src.pet_symptoms.graph.state import PetSymptomsState

logger = logging.getLogger(__name__)

def report_node(state: PetSymptomsState) -> Command[Literal["__end__"]]:
    """Node that reports the collected pet symptoms information."""
    print("\n=== Collected Pet Symptoms Information ===")
    print(f"Pet Type: {state.get('pet_type', 'Not provided')}")
    print(f"Pet Name: {state.get('pet_name', 'Not provided')}")
    print(f"Symptoms: {', '.join(state.get('symptoms', ['Not provided']))}")
    print(f"Severity: {state.get('severity', 'Not provided')}")
    print(f"Duration: {state.get('duration', 'Not provided')}")
    if state.get('additional_info'):
        print(f"Additional Information: {state['additional_info']}")
    print("========================================")
    
    return Command(
        update=state,
        goto="__end__"
    ) 