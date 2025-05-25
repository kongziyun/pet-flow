import asyncio
import logging
from src.pet_symptoms.graph.builder import build_graph
from src.pet_symptoms.graph.state import PetSymptomsState
from pprint import pprint

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default level is INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to run the pet symptoms collection workflow."""
    try:
        # Build the graph
        graph = build_graph()
        
        # Initialize the state
        initial_state: PetSymptomsState = {
            "current_question": "Hello! I'm here to help with your pet's symptoms. Please tell me about your pet and what's concerning you.",
            "current_input": "",
            "conversation_history": [],
            "symptoms": [],
            "is_complete": False,
            "extracted_info": {}
        }
                    # Display the current question
        # print(f"\n{initial_state['current_question']}\n")
        # user_input = input("\nYour response: ").strip()    
        # # Update state with user input
        # initial_state["current_input"] = user_input
        # print("\nInitial State:")
        # pprint(initial_state)
        # Run the workflow
        async for state in graph.astream(initial_state):
            True
            # logger.info(f"Current state: {state}\n\n")
            
            # # If we've reached the end, display the collected information
            # if state.get("is_complete"):
            #     print("\n=== Collected Pet Symptoms Information ===")
            #     print(f"Pet Type: {state.get('pet_type', 'Not provided')}")
            #     print(f"Pet Name: {state.get('pet_name', 'Not provided')}")
            #     print(f"Symptoms: {', '.join(state.get('symptoms', ['Not provided']))}")
            #     print(f"Severity: {state.get('severity', 'Not provided')}")
            #     print(f"Duration: {state.get('duration', 'Not provided')}")
            #     if state.get('additional_info'):
            #         print(f"Additional Information: {state['additional_info']}")
            #     print("========================================")
            #     break
            
            
            # print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ${state["current_input"]}")
            
    except Exception as e:
        logger.error(f"Error in main workflow: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 