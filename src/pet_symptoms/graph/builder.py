import asyncio
import logging
from langgraph.graph import END, START, StateGraph
from src.llms.llm import get_llm_by_type

from src.pet_symptoms.graph.collect_pet_info_node import collect_pet_info_node
from src.pet_symptoms.graph.symptoms_node import symptoms_node
from src.pet_symptoms.graph.report_node import report_node
from src.pet_symptoms.graph.state import PetSymptomsState

# def should_continue(state: PetSymptomsState) -> str:
#     """Determine which node to go to next based on the current state."""
#     logging.debug(f"Current state: {state}")
    
#     if state.get("is_complete"):
#         return "report"
#     elif not state.get("pet_type") or not state.get("pet_name"):
#         return "collect_pet_info"
#     elif not state.get("symptoms") or not state.get("severity") or not state.get("duration"):
#         return "collect_symptom_details"
#     else:
#         return "report"

def build_graph():
    """Build and return the pet symptoms workflow graph."""
    # Initialize LLM
    llm = get_llm_by_type("basic")
    
    # build state graph
    builder = StateGraph(PetSymptomsState)
    builder.add_edge(START, "collect_pet_info")
    
    builder.add_node("collect_pet_info", collect_pet_info_node)
    # builder.add_node("collect_symptom_details", symptoms_node)
    builder.add_node("report", report_node)
    
    # Add edges
    # builder.add_conditional_edges(
    #     START,
    #     should_continue,
    #     {
    #         "collect_pet_info": "collect_pet_info",
    #         "collect_symptom_details": "collect_symptom_details",
    #         "report": "report"
    #     },
    # )
    
    # builder.add_conditional_edges(
    #     "collect_pet_info",
    #     should_continue,
    #     {
    #         "collect_pet_info": "collect_pet_info",
    #         "collect_symptom_details": "collect_symptom_details",
    #         "report": "report"
    #     },
    # )
    
    # builder.add_conditional_edges(
    #     "collect_symptom_details",
    #     should_continue,
    #     {
    #         "collect_symptom_details": "collect_symptom_details",
    #         "report": "report"
    #     },
    # )
    
    # builder.add_edge("report", END)
    
    return builder.compile()

async def _test_workflow():
    workflow = build_graph()
    events = workflow.astream(
        {
            "pet_type": "",
            "pet_name": "",
            "symptoms": [],
            "severity": "",
            "duration": "",
            "additional_info": None,
            "current_question": None,
            "conversation_history": [],
            "current_input": "",
        },
        stream_mode="messages",
        subgraphs=True,
        config={"recursion_limit": 100},  # Increase recursion limit
    )
    async for node, event in events:
        e = event[0]
        print({"id": e.id, "object": "chat.completion.chunk", "content": e.content})

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    from src.pet_symptoms.graph.builder import build_graph
    graph = build_graph()
    print(graph.get_graph(xray=True).draw_mermaid()) 