"""
Master Agent - Conversation Orchestrator.
Interprets queries, delegates to workers, and synthesizes responses.
"""
from typing import Dict, List, Any, Optional, Tuple
import re
import uuid
import logging
from datetime import datetime

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

from agents.base_agent import get_llm
from schemas.models import (
    AgentType, AgentTask, AgentResponse, TaskStatus, 
    OutputFormat, AGENT_CAPABILITIES
)
from data.synthetic_data import DRUG_NAMES, THERAPY_AREAS, COMPANIES

logger = logging.getLogger(__name__)


class MasterAgent:
    """
    Master Agent that orchestrates the multi-agent system.
    
    Responsibilities:
    1. Interpret user queries and extract intent
    2. Break down complex queries into modular tasks
    3. Delegate tasks to appropriate worker agents
    4. Synthesize responses from multiple agents
    5. Format final output (text, tables, charts, reports)
    """
    
    def __init__(
        self,
        model_name: str = "gemini-2.0-flash",
        temperature: float = 0.1
    ):
        self.model_name = model_name
        self.temperature = temperature
        
        # Use shared LLM getter (tries Gemini first, then OpenAI)
        try:
            self.llm = get_llm(model_name, temperature)
            if self.llm is None:
                logger.warning("No LLM API key found. Using synthetic data only.")
        except Exception as e:
            logger.warning(f"Could not initialize LLM: {e}")
            self.llm = None
        
        self.agent_capabilities = AGENT_CAPABILITIES
        
        # Intent patterns for routing
        self.intent_patterns = {
            "market_analysis": [
                r"market\s*(size|share|analysis|trend)",
                r"sales\s*(data|trend|volume)",
                r"iqvia",
                r"commercial\s*(opportunity|potential)"
            ],
            "trade_analysis": [
                r"export|import|exim|trade",
                r"sourcing|supply\s*chain",
                r"api\s*(source|supply)"
            ],
            "patent_analysis": [
                r"patent|ip\s*(analysis|landscape)",
                r"fto|freedom\s*to\s*operate",
                r"expir(y|ation)|generic\s*entry"
            ],
            "clinical_trials": [
                r"clinical\s*trial|study|phase\s*[1-4]",
                r"pipeline|development\s*stage",
                r"enrollment|endpoint"
            ],
            "internal_knowledge": [
                r"internal|strategy\s*(document|deck)",
                r"field\s*insight|kol\s*feedback",
                r"competitive\s*intelligence"
            ],
            "web_intelligence": [
                r"guideline|publication|news",
                r"regulatory|fda|ema",
                r"latest|recent\s*update"
            ],
            "report_generation": [
                r"generate\s*report|create\s*pdf",
                r"export|download|summary\s*report"
            ]
        }
        
        # Keyword extraction patterns
        self.drug_patterns = [re.compile(rf"\b{drug}\b", re.IGNORECASE) for drug in DRUG_NAMES]
        self.therapy_patterns = [re.compile(rf"\b{area}\b", re.IGNORECASE) for area in THERAPY_AREAS]
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """
        Analyze user query to extract intent, entities, and required agents.
        """
        query_lower = query.lower()
        
        # Extract entities
        drug_name = self._extract_drug_name(query)
        therapy_area = self._extract_therapy_area(query)
        
        # Identify intents
        intents = []
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    intents.append(intent)
                    break
        
        # If no specific intent found, use comprehensive analysis
        if not intents:
            intents = ["market_analysis", "clinical_trials", "patent_analysis"]
        
        # Map intents to agents
        intent_to_agent = {
            "market_analysis": AgentType.IQVIA,
            "trade_analysis": AgentType.EXIM,
            "patent_analysis": AgentType.PATENT,
            "clinical_trials": AgentType.CLINICAL_TRIALS,
            "internal_knowledge": AgentType.INTERNAL_KNOWLEDGE,
            "web_intelligence": AgentType.WEB_INTELLIGENCE,
            "report_generation": AgentType.REPORT_GENERATOR
        }
        
        required_agents = list(set(intent_to_agent.get(intent) for intent in intents if intent in intent_to_agent))
        
        # Determine if report is needed
        needs_report = "report_generation" in intents or any(
            word in query_lower for word in ["report", "pdf", "document", "summary"]
        )
        
        return {
            "original_query": query,
            "drug_name": drug_name,
            "therapy_area": therapy_area,
            "intents": intents,
            "required_agents": required_agents,
            "needs_report": needs_report,
            "parameters": {
                "drug_name": drug_name,
                "therapy_area": therapy_area,
                "query": query
            }
        }
    
    def _extract_drug_name(self, query: str) -> Optional[str]:
        """Extract drug name from query."""
        for pattern in self.drug_patterns:
            match = pattern.search(query)
            if match:
                return match.group()
        return None
    
    def _extract_therapy_area(self, query: str) -> Optional[str]:
        """Extract therapy area from query."""
        for pattern in self.therapy_patterns:
            match = pattern.search(query)
            if match:
                return match.group()
        return None
    
    def create_task_plan(self, analysis: Dict[str, Any]) -> List[AgentTask]:
        """
        Create a plan of tasks for worker agents.
        """
        tasks = []
        
        for agent_type in analysis["required_agents"]:
            task_id = f"task_{uuid.uuid4().hex[:8]}"
            
            # Create agent-specific query
            agent_query = self._create_agent_query(
                agent_type,
                analysis["original_query"],
                analysis["parameters"]
            )
            
            task = AgentTask(
                task_id=task_id,
                agent_type=agent_type,
                query=agent_query,
                parameters=analysis["parameters"],
                priority=self._get_task_priority(agent_type),
                status=TaskStatus.PENDING
            )
            tasks.append(task)
        
        # Add report generation task if needed
        if analysis["needs_report"]:
            report_task = AgentTask(
                task_id=f"task_{uuid.uuid4().hex[:8]}",
                agent_type=AgentType.REPORT_GENERATOR,
                query="Generate comprehensive research report",
                parameters={
                    **analysis["parameters"],
                    "title": f"Research Report: {analysis['drug_name'] or analysis['therapy_area'] or 'Drug Repurposing Analysis'}"
                },
                priority=5,  # Lowest priority - runs last
                status=TaskStatus.PENDING
            )
            tasks.append(report_task)
        
        # Sort by priority
        tasks.sort(key=lambda t: t.priority)
        
        return tasks
    
    def _create_agent_query(
        self,
        agent_type: AgentType,
        original_query: str,
        parameters: Dict[str, Any]
    ) -> str:
        """Create a specific query for each agent type."""
        
        drug = parameters.get("drug_name", "")
        therapy = parameters.get("therapy_area", "")
        
        query_templates = {
            AgentType.IQVIA: f"Analyze market data and sales trends{f' for {drug}' if drug else ''}{f' in {therapy}' if therapy else ''}. {original_query}",
            AgentType.EXIM: f"Analyze export-import trade data{f' for {drug}' if drug else ''}{f' in {therapy}' if therapy else ''}. {original_query}",
            AgentType.PATENT: f"Analyze patent landscape and IP status{f' for {drug}' if drug else ''}{f' in {therapy}' if therapy else ''}. {original_query}",
            AgentType.CLINICAL_TRIALS: f"Search clinical trials database{f' for {drug}' if drug else ''}{f' in {therapy}' if therapy else ''}. {original_query}",
            AgentType.INTERNAL_KNOWLEDGE: f"Search internal knowledge base{f' related to {drug}' if drug else ''}{f' in {therapy}' if therapy else ''}. {original_query}",
            AgentType.WEB_INTELLIGENCE: f"Search web for latest information{f' on {drug}' if drug else ''}{f' in {therapy}' if therapy else ''}. {original_query}",
            AgentType.REPORT_GENERATOR: "Generate comprehensive research report based on all gathered data."
        }
        
        return query_templates.get(agent_type, original_query)
    
    def _get_task_priority(self, agent_type: AgentType) -> int:
        """Get priority for agent type (1=highest)."""
        priorities = {
            AgentType.IQVIA: 1,
            AgentType.CLINICAL_TRIALS: 1,
            AgentType.PATENT: 2,
            AgentType.EXIM: 2,
            AgentType.WEB_INTELLIGENCE: 3,
            AgentType.INTERNAL_KNOWLEDGE: 3,
            AgentType.REPORT_GENERATOR: 5
        }
        return priorities.get(agent_type, 3)
    
    def synthesize_responses(
        self,
        query: str,
        responses: List[AgentResponse],
        output_format: OutputFormat = OutputFormat.TEXT
    ) -> Dict[str, Any]:
        """
        Synthesize responses from multiple agents into a coherent summary.
        """
        # Collect all data
        all_summaries = []
        all_tables = []
        all_charts = []
        all_references = []
        
        for response in responses:
            if response.status == TaskStatus.COMPLETED:
                all_summaries.append({
                    "agent": response.agent_type.value,
                    "content": response.summary
                })
                all_tables.extend(response.tables)
                all_charts.extend(response.charts)
                all_references.extend(response.references)
        
        # Build synthesized response
        sections = []
        for summary in all_summaries:
            sections.append({
                "title": summary["agent"].replace("_", " ").title(),
                "content": summary["content"]
            })
        
        # Create executive summary
        executive_summary = self._create_executive_summary(query, all_summaries)
        
        # Format final response
        if output_format == OutputFormat.JSON:
            final_response = {
                "query": query,
                "executive_summary": executive_summary,
                "sections": sections,
                "tables": all_tables,
                "charts": all_charts,
                "references": list(set(all_references)),
                "generated_at": datetime.now().isoformat()
            }
        else:
            # Text/Markdown format
            response_parts = [
                f"# Research Analysis\n\n**Query:** {query}\n",
                f"## Executive Summary\n\n{executive_summary}\n",
                "---\n"
            ]
            
            for section in sections:
                response_parts.append(f"## {section['title']}\n\n{section['content']}\n\n")
            
            if all_references:
                response_parts.append("## References\n\n")
                for ref in set(all_references):
                    response_parts.append(f"- {ref}\n")
            
            final_response = "\n".join(response_parts)
        
        return {
            "response": final_response,
            "sections": sections,
            "tables": all_tables,
            "charts": all_charts,
            "references": list(set(all_references))
        }
    
    def _create_executive_summary(
        self,
        query: str,
        summaries: List[Dict[str, str]]
    ) -> str:
        """Create an executive summary from agent responses."""
        
        if self.llm:
            try:
                prompt = f"""Based on the following analysis from multiple specialized agents, 
create a concise executive summary (3-5 bullet points) answering the query: "{query}"

Agent Analyses:
{chr(10).join(f"**{s['agent']}**: {s['content'][:500]}" for s in summaries)}

Provide key insights and actionable recommendations."""

                response = self.llm.invoke([HumanMessage(content=prompt)])
                return response.content
            except Exception:
                # Silent fallback to avoid cluttering output when rate limited
                pass
        
        # High-quality technical fallback for synthetic mode
        summary_points = []
        for s in summaries:
            # Extract first meaningful line/sentence
            lines = [l.strip() for l in s["content"].split("\n") if l.strip() and not l.strip().startswith("#")]
            if lines:
                agent_name = s['agent'].replace('_', ' ').title()
                summary_points.append(f"• **{agent_name}:** {lines[0]}")
        
        if not summary_points:
            return "Analysis complete. Specialized agents have gathered domain-specific data for your request. Please see the detailed sections below."
            
        return "Key Insights from Multi-Agent Analysis:\n\n" + "\n".join(summary_points[:5])
    
    def format_response(
        self,
        synthesis: Dict[str, Any],
        include_tables: bool = True,
        include_charts: bool = True
    ) -> str:
        """Format the final response for display."""
        
        response = synthesis.get("response", "")
        
        if isinstance(response, dict):
            # JSON format - convert to readable string
            import json
            return json.dumps(response, indent=2)
        
        # Add tables if requested
        if include_tables and synthesis.get("tables"):
            response += "\n\n## Data Tables\n"
            for table in synthesis["tables"][:5]:  # Limit tables
                response += f"\n### {table.get('title', 'Table')}\n"
                headers = table.get("headers", [])
                rows = table.get("rows", [])
                
                if headers and rows:
                    response += "| " + " | ".join(str(h) for h in headers) + " |\n"
                    response += "| " + " | ".join("---" for _ in headers) + " |\n"
                    for row in rows[:10]:  # Limit rows
                        response += "| " + " | ".join(str(cell) for cell in row) + " |\n"
        
        return response
