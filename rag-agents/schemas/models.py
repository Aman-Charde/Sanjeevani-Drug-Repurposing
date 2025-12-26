"""
Pydantic models and schemas for the multi-agent system.
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Literal
from datetime import datetime
from enum import Enum


class AgentType(str, Enum):
    """Types of agents in the system."""
    MASTER = "master"
    IQVIA = "iqvia_insights"
    EXIM = "exim_trends"
    PATENT = "patent_landscape"
    CLINICAL_TRIALS = "clinical_trials"
    INTERNAL_KNOWLEDGE = "internal_knowledge"
    WEB_INTELLIGENCE = "web_intelligence"
    REPORT_GENERATOR = "report_generator"


class TaskStatus(str, Enum):
    """Status of a task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class OutputFormat(str, Enum):
    """Output format types."""
    TEXT = "text"
    TABLE = "table"
    CHART = "chart"
    PDF = "pdf"
    EXCEL = "excel"
    JSON = "json"


class AgentTask(BaseModel):
    """A task assigned to an agent."""
    task_id: str = Field(..., description="Unique identifier for the task")
    agent_type: AgentType = Field(..., description="Type of agent to handle the task")
    query: str = Field(..., description="The query or instruction for the agent")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Additional parameters")
    priority: int = Field(default=1, ge=1, le=5, description="Task priority (1=highest)")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AgentResponse(BaseModel):
    """Response from an agent."""
    agent_type: AgentType
    task_id: str
    status: TaskStatus
    data: Dict[str, Any] = Field(default_factory=dict)
    summary: str = ""
    tables: List[Dict[str, Any]] = Field(default_factory=list)
    charts: List[Dict[str, Any]] = Field(default_factory=list)
    references: List[str] = Field(default_factory=list)
    execution_time_ms: int = 0
    error: Optional[str] = None


class UserQuery(BaseModel):
    """User query input."""
    query: str = Field(..., description="The user's research query")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")
    preferred_format: OutputFormat = Field(default=OutputFormat.TEXT)
    include_charts: bool = Field(default=True)
    include_tables: bool = Field(default=True)
    generate_report: bool = Field(default=False)


class ConversationMessage(BaseModel):
    """A message in the conversation."""
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None


class ResearchReport(BaseModel):
    """Generated research report."""
    report_id: str
    title: str
    executive_summary: str
    sections: List[Dict[str, Any]]
    tables: List[Dict[str, Any]]
    charts: List[Dict[str, Any]]
    references: List[str]
    generated_at: datetime = Field(default_factory=datetime.now)
    format: OutputFormat
    file_path: Optional[str] = None


class ChartData(BaseModel):
    """Data for chart generation."""
    chart_type: Literal["bar", "line", "pie", "scatter", "heatmap", "area"]
    title: str
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    data: Dict[str, Any]
    options: Dict[str, Any] = Field(default_factory=dict)


class TableData(BaseModel):
    """Data for table generation."""
    title: str
    headers: List[str]
    rows: List[List[Any]]
    footer: Optional[str] = None
    style: Dict[str, Any] = Field(default_factory=dict)


class AgentCapabilities(BaseModel):
    """Capabilities of an agent."""
    agent_type: AgentType
    description: str
    supported_queries: List[str]
    output_formats: List[OutputFormat]
    data_sources: List[str]
    example_queries: List[str]


# Define agent capabilities
AGENT_CAPABILITIES = {
    AgentType.IQVIA: AgentCapabilities(
        agent_type=AgentType.IQVIA,
        description="Queries IQVIA datasets for sales trends, volume shifts and therapy area dynamics",
        supported_queries=["market size", "sales trends", "therapy dynamics", "volume analysis", "market share"],
        output_formats=[OutputFormat.TABLE, OutputFormat.CHART, OutputFormat.TEXT],
        data_sources=["IQVIA MIDAS", "IQVIA National Sales Perspectives"],
        example_queries=[
            "What is the market size for oncology drugs?",
            "Show sales trends for Metformin",
            "Compare market share in cardiology segment"
        ]
    ),
    AgentType.EXIM: AgentCapabilities(
        agent_type=AgentType.EXIM,
        description="Extracts export-import data for APIs and formulations across countries",
        supported_queries=["trade data", "export trends", "import analysis", "API sourcing", "trade balance"],
        output_formats=[OutputFormat.TABLE, OutputFormat.CHART, OutputFormat.TEXT],
        data_sources=["UN Comtrade", "National Trade Databases"],
        example_queries=[
            "Show export trends for APIs to USA",
            "What are the import sources for Metformin API?",
            "Trade balance analysis for pharmaceuticals"
        ]
    ),
    AgentType.PATENT: AgentCapabilities(
        agent_type=AgentType.PATENT,
        description="Searches patent databases for active patents, expiry timelines and FTO analysis",
        supported_queries=["patent search", "expiry analysis", "FTO status", "patent landscape", "IP analysis"],
        output_formats=[OutputFormat.TABLE, OutputFormat.CHART, OutputFormat.PDF],
        data_sources=["USPTO", "EPO", "WIPO"],
        example_queries=[
            "Patent landscape for Pembrolizumab",
            "When do patents expire for Adalimumab?",
            "Show patent filing trends in immunology"
        ]
    ),
    AgentType.CLINICAL_TRIALS: AgentCapabilities(
        agent_type=AgentType.CLINICAL_TRIALS,
        description="Fetches trial pipeline data from clinical trial registries",
        supported_queries=["clinical trials", "trial pipeline", "phase distribution", "sponsor analysis", "enrollment data"],
        output_formats=[OutputFormat.TABLE, OutputFormat.CHART, OutputFormat.TEXT],
        data_sources=["ClinicalTrials.gov", "WHO ICTRP", "EU Clinical Trials Register"],
        example_queries=[
            "Active trials for Nivolumab",
            "Phase 3 trials in oncology",
            "Competitor pipeline in immunology"
        ]
    ),
    AgentType.INTERNAL_KNOWLEDGE: AgentCapabilities(
        agent_type=AgentType.INTERNAL_KNOWLEDGE,
        description="Retrieves and summarizes internal documents and knowledge base",
        supported_queries=["internal docs", "strategy documents", "field insights", "market intelligence", "competitive analysis"],
        output_formats=[OutputFormat.TEXT, OutputFormat.PDF, OutputFormat.TABLE],
        data_sources=["Internal Knowledge Base", "Strategy Documents", "Field Reports"],
        example_queries=[
            "Summarize our oncology strategy",
            "What are recent field insights?",
            "Find competitive analysis documents"
        ]
    ),
    AgentType.WEB_INTELLIGENCE: AgentCapabilities(
        agent_type=AgentType.WEB_INTELLIGENCE,
        description="Performs real-time web search for guidelines, publications, news and forums",
        supported_queries=["web search", "guidelines", "publications", "news", "scientific literature"],
        output_formats=[OutputFormat.TEXT, OutputFormat.TABLE],
        data_sources=["PubMed", "FDA", "WHO", "News Sources", "Scientific Journals"],
        example_queries=[
            "Latest FDA guidelines for oncology",
            "Recent publications on drug repurposing",
            "News about Pfizer acquisitions"
        ]
    ),
    AgentType.REPORT_GENERATOR: AgentCapabilities(
        agent_type=AgentType.REPORT_GENERATOR,
        description="Formats synthesized responses into polished PDF or Excel reports",
        supported_queries=["generate report", "create PDF", "export excel", "format summary"],
        output_formats=[OutputFormat.PDF, OutputFormat.EXCEL],
        data_sources=["Agent Responses", "Synthesized Data"],
        example_queries=[
            "Generate PDF report",
            "Export analysis to Excel",
            "Create executive summary document"
        ]
    )
}
