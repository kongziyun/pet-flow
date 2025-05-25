import logging
from pprint import pprint
from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional, List
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph
from langchain.schema import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)

class ExtractedInfo(BaseModel):
    """Information extracted from user input."""
    pet_type: Optional[str] = Field(None, description="Type of pet (e.g., dog, cat)")
    pet_name: Optional[str] = Field(None, description="Name of the pet")
    symptoms: List[str] = Field(default_factory=list, description="List of reported symptoms")
    severity: Optional[str] = Field(None, description="Severity of symptoms (mild, moderate, severe)")
    duration: Optional[str] = Field(None, description="How long the symptoms have been present")
    additional_info: Optional[str] = Field(None, description="Any additional information provided")

def get_conversation_prompt():
    """Get the prompt for natural conversation."""
    return ChatPromptTemplate.from_messages([
        ("system", """You are a helpful veterinary assistant collecting information about a pet's symptoms.
        Have a natural conversation with the user to gather information about their pet's condition.
        Be empathetic and professional. Ask follow-up questions when needed. Focus on asking for the following information:
        - Pet type (e.g., dog, cat)
        - Pet name
        - Symptoms
        - Severity of symptoms (mild, moderate, severe)
        - Duration of symptoms
        - Any additional relevant information
        
        Current conversation history:
        {conversation_history}
        
        Current state of information, do NOT ask for the information that we already knew:
        {current_state}
        
        Based on this, what would be a natural next question or response?"""),
        ("human", "{user_input}")
    ])

def get_extraction_prompt():
    """Get the prompt for information extraction."""
    return ChatPromptTemplate.from_messages([
        ("system", """Extract structured information about the pet's condition from the user's input.
        Focus on identifying:
        - Pet type (e.g., dog, cat)
        - Pet name
        - Symptoms
        - Severity of symptoms (mild, moderate, severe)
        - Duration of symptoms
        - Any additional relevant information
        
        Extract and return the information in the following format:
        {format_instructions}"""),
        ("human", """Current state of information:
        {current_state}
        
        User input:
        {user_input}""")
    ])

def get_next_question(state: Dict, user_input: str, llm: ChatOpenAI) -> str:
    """Get the next question based on conversation history and current state."""
    prompt = get_conversation_prompt()
    
    # Format conversation history
    conversation_history = "\n".join([
        f"{'Assistant' if msg['role'] == 'assistant' else 'User'}: {msg['content']}"
        for msg in state.get("conversation_history", [])
    ])
    
    # Format current state
    current_state = {
        "pet_type": state.get("pet_type"),
        "pet_name": state.get("pet_name"),
        "symptoms": state.get("symptoms", []),
        "severity": state.get("severity"),
        "duration": state.get("duration"),
        "additional_info": state.get("additional_info")
    }

    # print("?!?!?!!!!!!!")
    # pprint(current_state)
    
    # Get response from LLM
    messages = prompt.format_messages(
        conversation_history=conversation_history,
        current_state=current_state,
        user_input=user_input
    )
    
    # Convert to the format expected by LangChain
    contents = [{"role": msg.type, "content": msg.content} for msg in messages]
    
    response = llm.invoke(contents)
    return response.content

def extract_information(state: Dict, user_input: str, llm: ChatOpenAI) -> ExtractedInfo:
    """Extract structured information from user input."""
    parser = PydanticOutputParser(pydantic_object=ExtractedInfo)
    prompt = get_extraction_prompt()
    
    # Format current state
    current_state = {
        "pet_type": state.get("pet_type"),
        "pet_name": state.get("pet_name"),
        "symptoms": state.get("symptoms", []),
        "severity": state.get("severity"),
        "duration": state.get("duration"),
        "additional_info": state.get("additional_info")
    }
    # Get response from LLM
    messages = prompt.format_messages(
        current_state=current_state,
        user_input=user_input,
        format_instructions=parser.get_format_instructions()
    )
    
    # print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! {messages}")
    # Convert to the format expected by LangChain
    contents = [{"role": msg.type, "content": msg.content} for msg in messages]
    
    response = llm.invoke(contents)
    
    # Parse the response
    try:
        extracted_info = parser.parse(response.content)
        return extracted_info
    except Exception as e:
        logger.error(f"Error parsing LLM response: {e}")
        return ExtractedInfo() 