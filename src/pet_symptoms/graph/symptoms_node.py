from typing import Annotated, Sequence, TypedDict
import logging
from langgraph.graph import END, START, StateGraph
from src.pet_symptoms.graph.state import PetSymptomsState

logger = logging.getLogger(__name__)

def symptoms_node(state: PetSymptomsState) -> PetSymptomsState:
    """Node that collects detailed symptom information."""
    current_input = state.get("current_input", "")
    
    if not state.get("severity"):
        if current_input:
            logger.info(f"Received severity: {current_input}")
            return {
                **state,
                "severity": current_input,
                "current_question": "How long has your pet been experiencing these symptoms?",
            }
        logger.info("Asking for symptom severity")
        print("\nHow severe are these symptoms? (mild, moderate, or severe)")
        user_input = input("Enter severity (mild/moderate/severe): ").strip()
        return {
            **state,
            "severity": user_input,
            "current_question": "How long has your pet been experiencing these symptoms?",
        }
    elif not state.get("duration"):
        if current_input:
            logger.info(f"Received duration: {current_input}")
            return {
                **state,
                "duration": current_input,
                "current_question": "Is there any additional information you'd like to share about your pet's condition?",
            }
        logger.info("Asking for symptom duration")
        print("\nHow long has your pet been experiencing these symptoms?")
        user_input = input("Enter duration: ").strip()
        return {
            **state,
            "duration": user_input,
            "current_question": "Is there any additional information you'd like to share about your pet's condition?",
        }
    else:
        if current_input:
            logger.info(f"Received additional info: {current_input}")
            return {
                **state,
                "additional_info": current_input,
                "is_complete": True,
                "current_question": "Thank you for providing this information. A veterinarian will review these details shortly.",
            }
        logger.info("Asking for additional information")
        print("\nIs there any additional information you'd like to share about your pet's condition?")
        user_input = input("Enter additional information (or press Enter to skip): ").strip()
        return {
            **state,
            "additional_info": user_input,
            "is_complete": True,
            "current_question": "Thank you for providing this information. A veterinarian will review these details shortly.",
        } 