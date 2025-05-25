from pprint import pprint
from typing import Annotated, Sequence, TypedDict, Literal
import logging
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
from langchain_openai import ChatOpenAI
from src.pet_symptoms.graph.state import PetSymptomsState
from src.pet_symptoms.graph.llm_utils import get_next_question, extract_information
from src.llms.llm import get_llm_by_type

logger = logging.getLogger(__name__)

def collect_pet_info_node(state: PetSymptomsState) -> Command[Literal["collect_pet_info","report"]]:
    """Node that collects basic pet information through natural conversation."""
    llm = get_llm_by_type("basic")
    print("\nCurrent State:")
    pprint(state)
    # Update state with extracted information
    updated_state = state
    # Display the current question
    current_question=state.get('current_question')
            
    if current_question:
        print(f"\n{state['current_question']}")

    # Get user input
    user_input = input("\nYour response: ").strip()
            
    # Update state with user input
    updated_state["current_input"] = user_input
    # Extract information from user input
    extracted_info = extract_information(state, user_input, llm)
    
    if extracted_info.pet_type and not state.get("pet_type"):
        updated_state["pet_type"] = extracted_info.pet_type
    if extracted_info.pet_name and not state.get("pet_name"):
        updated_state["pet_name"] = extracted_info.pet_name
    if extracted_info.symptoms:
        updated_state["symptoms"] = state.get("symptoms", []) + extracted_info.symptoms
    if extracted_info.severity and not state.get("severity"):
        updated_state["severity"] = extracted_info.severity
    if extracted_info.duration and not state.get("duration"):
        updated_state["duration"] = extracted_info.duration
    if extracted_info.additional_info:
        updated_state["additional_info"] = extracted_info.additional_info
    
    # Get next question from LLM
    next_question = get_next_question(updated_state, user_input, llm)
    
    # Update conversation history
    conversation_history = state.get("conversation_history", [])
    if user_input:
        conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": next_question})
    updated_state["conversation_history"] = conversation_history
    updated_state["current_question"] = next_question
    # print("?!?!?!?!?!?!?")
    # pprint(updated_state)
    # Check if we have all required information
    has_required_info = (
        updated_state.get("pet_type") and
        updated_state.get("pet_name") and
        updated_state.get("symptoms") and
        updated_state.get("severity") and
        updated_state.get("duration")
    )
    print(f"is it completed? {has_required_info}")
    if has_required_info:
        return Command(
            update=updated_state,
            goto="report"
        )
    else:
        return Command(
            update=updated_state,
            goto="collect_pet_info"
        )