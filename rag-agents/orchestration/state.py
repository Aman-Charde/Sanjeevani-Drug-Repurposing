"""
LangGraph State Definitions for Multi-Agent Orchestration.
"""
from typing import Dict, List, Any, Optional, Annotated, TypedDict, Sequence
from datetime import datetime
import operator

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from schemas.models import AgentType, TaskStatus, AgentTask, AgentResponse, OutputFormat


class AgentState(TypedDict):
    """State maintained throughout the multi-agent workflow."""
    
    # Conversation
    messages: Annotated[Sequence[BaseMessage], operator.add]
    
    # User query
    user_query: str
    query_intent: Optional[str]
    
    # Extracted parameters
    drug_name: Optional[str]
    therapy_area: Optional[str]
    parameters: Dict[str, Any]
    
    # Task management
    tasks: List[AgentTask]
    current_task_index: int
    
    # Agent responses
    agent_responses: Annotated[List[AgentResponse], operator.add]
    
    # Output configuration
    output_format: OutputFormat
    include_charts: bool
    include_tables: bool
    generate_report: bool
    
    # Final output
    final_response: Optional[str]
    report_path: Optional[str]
    
    # Metadata
    iteration_count: int
    max_iterations: int
    status: str
    error: Optional[str]


def create_initial_state(
    user_query: str,
    output_format: OutputFormat = OutputFormat.TEXT,
    include_charts: bool = True,
    include_tables: bool = True,
    generate_report: bool = False
) -> AgentState:
    """Create initial state for the workflow."""
    return AgentState(
        messages=[HumanMessage(content=user_query)],
        user_query=user_query,
        query_intent=None,
        drug_name=None,
        therapy_area=None,
        parameters={},
        tasks=[],
        current_task_index=0,
        agent_responses=[],
        output_format=output_format,
        include_charts=include_charts,
        include_tables=include_tables,
        generate_report=generate_report,
        final_response=None,
        report_path=None,
        iteration_count=0,
        max_iterations=10,
        status="initialized",
        error=None
    )


class TaskPlan(TypedDict):
    """Plan of tasks to execute."""
    tasks: List[Dict[str, Any]]
    execution_order: List[str]
    parallel_groups: List[List[str]]


class SynthesisResult(TypedDict):
    """Result of response synthesis."""
    summary: str
    sections: List[Dict[str, Any]]
    tables: List[Dict[str, Any]]
    charts: List[Dict[str, Any]]
    references: List[str]
