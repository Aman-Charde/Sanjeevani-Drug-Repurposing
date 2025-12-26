"""
LangGraph Workflow for Multi-Agent Orchestration.
Implements the graph-based workflow for coordinating multiple agents.
"""
from typing import Dict, Any, List, Optional, Literal
import logging
from datetime import datetime

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage

from orchestration.state import AgentState, create_initial_state
from orchestration.master_agent import MasterAgent
from agents import (
    IQVIAInsightsAgent,
    EXIMTrendsAgent,
    PatentLandscapeAgent,
    ClinicalTrialsAgent,
    InternalKnowledgeAgent,
    WebIntelligenceAgent,
    ReportGeneratorAgent
)
from schemas.models import AgentType, TaskStatus, AgentResponse, OutputFormat

logger = logging.getLogger(__name__)


class MultiAgentOrchestrator:
    """
    LangGraph-based multi-agent orchestrator for drug repurposing research.
    
    Workflow:
    1. analyze_query: Master agent analyzes user query
    2. plan_tasks: Create task plan for worker agents
    3. execute_tasks: Execute tasks via worker agents
    4. synthesize: Combine responses into coherent output
    5. generate_report: (Optional) Generate formatted report
    """
    
    def __init__(self):
        """Initialize the orchestrator with all agents."""
        
        # Initialize master agent
        self.master_agent = MasterAgent()
        
        # Initialize worker agents
        self.worker_agents = {
            AgentType.IQVIA: IQVIAInsightsAgent(),
            AgentType.EXIM: EXIMTrendsAgent(),
            AgentType.PATENT: PatentLandscapeAgent(),
            AgentType.CLINICAL_TRIALS: ClinicalTrialsAgent(),
            AgentType.INTERNAL_KNOWLEDGE: InternalKnowledgeAgent(),
            AgentType.WEB_INTELLIGENCE: WebIntelligenceAgent(),
            AgentType.REPORT_GENERATOR: ReportGeneratorAgent()
        }
        
        # Build the graph
        self.graph = self._build_graph()
        self.compiled_graph = self.graph.compile()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        # Create the graph with state schema
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_query", self._analyze_query_node)
        workflow.add_node("plan_tasks", self._plan_tasks_node)
        workflow.add_node("execute_tasks", self._execute_tasks_node)
        workflow.add_node("synthesize", self._synthesize_node)
        workflow.add_node("generate_report", self._generate_report_node)
        workflow.add_node("format_output", self._format_output_node)
        
        # Add entry point
        workflow.set_entry_point("analyze_query")
        
        # Add edges
        workflow.add_edge("analyze_query", "plan_tasks")
        workflow.add_edge("plan_tasks", "execute_tasks")
        workflow.add_edge("execute_tasks", "synthesize")
        
        # Conditional edge for report generation
        workflow.add_conditional_edges(
            "synthesize",
            self._should_generate_report,
            {
                "generate_report": "generate_report",
                "format_output": "format_output"
            }
        )
        
        workflow.add_edge("generate_report", "format_output")
        workflow.add_edge("format_output", END)
        
        return workflow
    
    def _analyze_query_node(self, state: AgentState) -> Dict[str, Any]:
        """Analyze the user query to extract intent and entities."""
        
        logger.info(f"Analyzing query: {state['user_query']}")
        
        analysis = self.master_agent.analyze_query(state["user_query"])
        
        return {
            "query_intent": ", ".join(analysis["intents"]),
            "drug_name": analysis["drug_name"],
            "therapy_area": analysis["therapy_area"],
            "parameters": analysis["parameters"],
            "generate_report": analysis["needs_report"] or state.get("generate_report", False),
            "status": "analyzed",
            "messages": [AIMessage(content=f"Query analyzed. Identified intents: {', '.join(analysis['intents'])}")]
        }
    
    def _plan_tasks_node(self, state: AgentState) -> Dict[str, Any]:
        """Create task plan for worker agents."""
        
        logger.info("Planning tasks...")
        
        analysis = {
            "original_query": state["user_query"],
            "drug_name": state.get("drug_name"),
            "therapy_area": state.get("therapy_area"),
            "intents": state.get("query_intent", "").split(", "),
            "required_agents": self._determine_required_agents(state),
            "needs_report": state.get("generate_report", False),
            "parameters": state.get("parameters", {})
        }
        
        tasks = self.master_agent.create_task_plan(analysis)
        
        return {
            "tasks": tasks,
            "current_task_index": 0,
            "status": "planned",
            "messages": [AIMessage(content=f"Created {len(tasks)} tasks for execution.")]
        }
    
    def _determine_required_agents(self, state: AgentState) -> List[AgentType]:
        """Determine which agents are needed based on query analysis."""
        
        intents = state.get("query_intent", "").split(", ")
        agents = []
        
        intent_mapping = {
            "market_analysis": AgentType.IQVIA,
            "trade_analysis": AgentType.EXIM,
            "patent_analysis": AgentType.PATENT,
            "clinical_trials": AgentType.CLINICAL_TRIALS,
            "internal_knowledge": AgentType.INTERNAL_KNOWLEDGE,
            "web_intelligence": AgentType.WEB_INTELLIGENCE
        }
        
        for intent in intents:
            intent = intent.strip()
            if intent in intent_mapping:
                agents.append(intent_mapping[intent])
        
        # Default agents if none determined
        if not agents:
            agents = [AgentType.IQVIA, AgentType.CLINICAL_TRIALS, AgentType.PATENT]
        
        return agents
    
    def _execute_tasks_node(self, state: AgentState) -> Dict[str, Any]:
        """Execute tasks using worker agents."""
        
        logger.info("Executing tasks...")
        
        responses = []
        
        for task in state["tasks"]:
            if task.agent_type == AgentType.REPORT_GENERATOR:
                # Skip report generation here - handled separately
                continue
            
            agent = self.worker_agents.get(task.agent_type)
            if agent:
                logger.info(f"Executing task {task.task_id} with {task.agent_type.value}")
                
                try:
                    response = agent.execute(task)
                    responses.append(response)
                except Exception as e:
                    logger.error(f"Task {task.task_id} failed: {e}")
                    responses.append(AgentResponse(
                        agent_type=task.agent_type,
                        task_id=task.task_id,
                        status=TaskStatus.FAILED,
                        error=str(e)
                    ))
        
        return {
            "agent_responses": responses,
            "status": "executed",
            "messages": [AIMessage(content=f"Executed {len(responses)} tasks successfully.")]
        }
    
    def _synthesize_node(self, state: AgentState) -> Dict[str, Any]:
        """Synthesize responses from all agents."""
        
        logger.info("Synthesizing responses...")
        
        synthesis = self.master_agent.synthesize_responses(
            state["user_query"],
            state.get("agent_responses", []),
            state.get("output_format", OutputFormat.TEXT)
        )
        
        formatted_response = self.master_agent.format_response(
            synthesis,
            include_tables=state.get("include_tables", True),
            include_charts=state.get("include_charts", True)
        )
        
        return {
            "final_response": formatted_response,
            "status": "synthesized",
            "messages": [AIMessage(content="Responses synthesized successfully.")]
        }
    
    def _should_generate_report(self, state: AgentState) -> Literal["generate_report", "format_output"]:
        """Decide whether to generate a report."""
        
        if state.get("generate_report", False):
            return "generate_report"
        return "format_output"
    
    def _generate_report_node(self, state: AgentState) -> Dict[str, Any]:
        """Generate a formatted report."""
        
        logger.info("Generating report...")
        
        report_agent = self.worker_agents[AgentType.REPORT_GENERATOR]
        
        # Create report task
        from schemas.models import AgentTask
        import uuid
        
        report_task = AgentTask(
            task_id=f"report_{uuid.uuid4().hex[:8]}",
            agent_type=AgentType.REPORT_GENERATOR,
            query="Generate comprehensive research report",
            parameters={
                "agent_responses": [r.model_dump() if hasattr(r, 'model_dump') else r.__dict__ 
                                   for r in state.get("agent_responses", [])],
                "title": f"Research Report: {state.get('drug_name') or state.get('therapy_area') or 'Drug Repurposing Analysis'}",
                "output_format": state.get("output_format", OutputFormat.PDF)
            }
        )
        
        response = report_agent.execute(report_task)
        
        return {
            "report_path": response.data.get("report_path"),
            "agent_responses": [response],
            "status": "report_generated",
            "messages": [AIMessage(content=f"Report generated: {response.data.get('report_path')}")]
        }
    
    def _format_output_node(self, state: AgentState) -> Dict[str, Any]:
        """Format the final output."""
        
        logger.info("Formatting final output...")
        
        # Build final message
        final_parts = [state.get("final_response", "")]
        
        if state.get("report_path"):
            final_parts.append(f"\n\n📄 **Report Generated:** `{state['report_path']}`")
        
        return {
            "final_response": "\n".join(final_parts),
            "status": "completed",
            "messages": [AIMessage(content="\n".join(final_parts))]
        }
    
    def run(
        self,
        query: str,
        output_format: OutputFormat = OutputFormat.TEXT,
        include_charts: bool = True,
        include_tables: bool = True,
        generate_report: bool = False
    ) -> Dict[str, Any]:
        """
        Run the multi-agent workflow.
        
        Args:
            query: User research query
            output_format: Desired output format
            include_charts: Whether to include chart data
            include_tables: Whether to include table data
            generate_report: Whether to generate a report file
            
        Returns:
            Dict with final response, tables, charts, and report path
        """
        
        # Create initial state
        initial_state = create_initial_state(
            user_query=query,
            output_format=output_format,
            include_charts=include_charts,
            include_tables=include_tables,
            generate_report=generate_report
        )
        
        # Run the graph
        logger.info(f"Starting workflow for query: {query}")
        
        try:
            final_state = self.compiled_graph.invoke(initial_state)
            
            return {
                "success": True,
                "query": query,
                "response": final_state.get("final_response", ""),
                "agent_responses": final_state.get("agent_responses", []),
                "report_path": final_state.get("report_path"),
                "status": final_state.get("status", "completed")
            }
            
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "status": "failed"
            }
    
    def run_stream(
        self,
        query: str,
        output_format: OutputFormat = OutputFormat.TEXT,
        include_charts: bool = True,
        include_tables: bool = True,
        generate_report: bool = False
    ):
        """
        Run the workflow with streaming updates.
        
        Yields:
            Dict with node name and state updates
        """
        
        initial_state = create_initial_state(
            user_query=query,
            output_format=output_format,
            include_charts=include_charts,
            include_tables=include_tables,
            generate_report=generate_report
        )
        
        logger.info(f"Starting streaming workflow for query: {query}")
        
        try:
            for event in self.compiled_graph.stream(initial_state):
                yield event
                
        except Exception as e:
            logger.error(f"Streaming workflow failed: {e}")
            yield {"error": str(e), "status": "failed"}


# Convenience function to create orchestrator
def create_orchestrator() -> MultiAgentOrchestrator:
    """Create and return a new MultiAgentOrchestrator instance."""
    return MultiAgentOrchestrator()
