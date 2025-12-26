"""
Base Agent class for all worker agents.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import time
import uuid
import logging
import os

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from schemas.models import AgentType, AgentResponse, TaskStatus, AgentTask

logger = logging.getLogger(__name__)


def get_llm(model_name: str = "gemini-2.0-flash", temperature: float = 0.1, max_tokens: int = 4096):
    """Get LLM instance - tries Gemini first (free), then OpenAI as fallback."""
    
    # Try Google Gemini first (FREE)
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if google_api_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            # Use correct model name - gemini-2.0-flash is the current free model
            gemini_model = model_name if "gemini" in model_name else "gemini-2.0-flash"
            return ChatGoogleGenerativeAI(
                model=gemini_model,
                temperature=temperature,
                max_output_tokens=max_tokens,
                google_api_key=google_api_key,
                convert_system_message_to_human=True  # Gemini doesn't support system messages directly
            )
        except Exception as e:
            logger.warning(f"Could not initialize Gemini: {e}")
    
    # Try OpenAI as fallback
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if openai_api_key:
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model="gpt-4-turbo-preview" if "gemini" in model_name else model_name,
                temperature=temperature,
                max_tokens=max_tokens
            )
        except Exception as e:
            logger.warning(f"Could not initialize OpenAI: {e}")
    
    return None


class BaseAgent(ABC):
    """Base class for all worker agents."""
    
    def __init__(
        self,
        agent_type: AgentType,
        model_name: str = "gemini-2.0-flash",
        temperature: float = 0.1,
        max_tokens: int = 4096
    ):
        self.agent_type = agent_type
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Initialize LLM (will be None if no API key)
        try:
            self.llm = get_llm(model_name, temperature, max_tokens)
            if self.llm is None:
                logger.warning("No LLM API key found. Using synthetic data only.")
        except Exception as e:
            logger.warning(f"Could not initialize LLM: {e}. Using mock responses.")
            self.llm = None
        
        self.system_prompt = self._get_system_prompt()
    
    @abstractmethod
    def _get_system_prompt(self) -> str:
        """Get the system prompt for this agent."""
        pass
    
    @abstractmethod
    def _process_query(self, query: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process the query and return results."""
        pass
    
    def execute(self, task: AgentTask) -> AgentResponse:
        """Execute the task and return response."""
        start_time = time.time()
        
        try:
            # Process the query
            result = self._process_query(task.query, task.parameters)
            
            # Build response
            response = AgentResponse(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status=TaskStatus.COMPLETED,
                data=result.get("data", {}),
                summary=result.get("summary", ""),
                tables=result.get("tables", []),
                charts=result.get("charts", []),
                references=result.get("references", []),
                execution_time_ms=int((time.time() - start_time) * 1000)
            )
            
            logger.info(f"Agent {self.agent_type.value} completed task {task.task_id}")
            return response
            
        except Exception as e:
            logger.error(f"Agent {self.agent_type.value} failed task {task.task_id}: {e}")
            return AgentResponse(
                agent_type=self.agent_type,
                task_id=task.task_id,
                status=TaskStatus.FAILED,
                error=str(e),
                execution_time_ms=int((time.time() - start_time) * 1000)
            )
    
    def _generate_llm_response(self, prompt: str, context: str = "") -> str:
        """Generate a response using the LLM."""
        if self.llm is None:
            return "LLM not available. Using synthetic data."
        
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=f"Context: {context}\n\nQuery: {prompt}")
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return f"Error generating response: {e}"
    
    def _format_table(self, title: str, headers: List[str], rows: List[List[Any]]) -> Dict[str, Any]:
        """Format data as a table."""
        return {
            "title": title,
            "headers": headers,
            "rows": rows,
            "row_count": len(rows)
        }
    
    def _format_chart(
        self,
        chart_type: str,
        title: str,
        data: Dict[str, Any],
        x_label: str = "",
        y_label: str = ""
    ) -> Dict[str, Any]:
        """Format data for chart generation."""
        return {
            "chart_type": chart_type,
            "title": title,
            "x_label": x_label,
            "y_label": y_label,
            "data": data
        }
