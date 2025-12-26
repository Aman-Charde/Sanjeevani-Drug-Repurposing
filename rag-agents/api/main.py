"""
FastAPI Application for Multi-Agent Drug Repurposing System.
Provides REST API endpoints for interacting with the multi-agent system.
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging
import os
import json
import asyncio
from datetime import datetime

from orchestration import create_orchestrator, MultiAgentOrchestrator
from schemas.models import OutputFormat, AgentType, AGENT_CAPABILITIES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Drug Repurposing Multi-Agent System",
    description="AI-driven tool for exploring potential drug innovation cases using multi-agent orchestration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global orchestrator instance
orchestrator: Optional[MultiAgentOrchestrator] = None


class QueryRequest(BaseModel):
    """Request model for research queries."""
    query: str = Field(..., description="Research query to analyze")
    output_format: str = Field(default="text", description="Output format: text, json, pdf, excel")
    include_charts: bool = Field(default=True, description="Include chart data in response")
    include_tables: bool = Field(default=True, description="Include table data in response")
    generate_report: bool = Field(default=False, description="Generate downloadable report")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "Analyze market potential for Metformin in oncology",
                "output_format": "text",
                "include_charts": True,
                "include_tables": True,
                "generate_report": False
            }
        }


class QueryResponse(BaseModel):
    """Response model for research queries."""
    success: bool
    query: str
    response: str
    report_path: Optional[str] = None
    status: str
    execution_time_ms: int
    agent_count: int


class AgentInfo(BaseModel):
    """Information about an agent."""
    agent_type: str
    description: str
    supported_queries: List[str]
    output_formats: List[str]
    data_sources: List[str]
    example_queries: List[str]


@app.on_event("startup")
async def startup_event():
    """Initialize the orchestrator on startup."""
    global orchestrator
    logger.info("Initializing Multi-Agent Orchestrator...")
    orchestrator = create_orchestrator()
    logger.info("Orchestrator initialized successfully")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Drug Repurposing Multi-Agent System",
        "version": "1.0.0",
        "description": "AI-driven tool for drug innovation research",
        "endpoints": {
            "query": "/api/query",
            "stream": "/api/stream",
            "agents": "/api/agents",
            "health": "/api/health",
            "docs": "/docs"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "orchestrator_initialized": orchestrator is not None
    }


@app.get("/api/agents", response_model=List[AgentInfo])
async def list_agents():
    """List all available agents and their capabilities."""
    agents = []
    for agent_type, capabilities in AGENT_CAPABILITIES.items():
        agents.append(AgentInfo(
            agent_type=agent_type.value,
            description=capabilities.description,
            supported_queries=capabilities.supported_queries,
            output_formats=[f.value for f in capabilities.output_formats],
            data_sources=capabilities.data_sources,
            example_queries=capabilities.example_queries
        ))
    return agents


@app.post("/api/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a research query using the multi-agent system.
    
    This endpoint:
    1. Analyzes the query to determine intent
    2. Delegates to appropriate worker agents
    3. Synthesizes responses
    4. Optionally generates a report
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    start_time = datetime.now()
    
    try:
        # Map output format
        format_map = {
            "text": OutputFormat.TEXT,
            "json": OutputFormat.JSON,
            "pdf": OutputFormat.PDF,
            "excel": OutputFormat.EXCEL
        }
        output_format = format_map.get(request.output_format.lower(), OutputFormat.TEXT)
        
        # Run the orchestrator
        result = orchestrator.run(
            query=request.query,
            output_format=output_format,
            include_charts=request.include_charts,
            include_tables=request.include_tables,
            generate_report=request.generate_report
        )
        
        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        return QueryResponse(
            success=result.get("success", False),
            query=request.query,
            response=result.get("response", ""),
            report_path=result.get("report_path"),
            status=result.get("status", "unknown"),
            execution_time_ms=execution_time,
            agent_count=len(result.get("agent_responses", []))
        )
        
    except Exception as e:
        logger.error(f"Query processing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/stream")
async def stream_query(request: QueryRequest):
    """
    Process a research query with streaming updates.
    
    Returns Server-Sent Events (SSE) with progress updates.
    """
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    async def generate():
        try:
            format_map = {
                "text": OutputFormat.TEXT,
                "json": OutputFormat.JSON,
                "pdf": OutputFormat.PDF,
                "excel": OutputFormat.EXCEL
            }
            output_format = format_map.get(request.output_format.lower(), OutputFormat.TEXT)
            
            for event in orchestrator.run_stream(
                query=request.query,
                output_format=output_format,
                include_charts=request.include_charts,
                include_tables=request.include_tables,
                generate_report=request.generate_report
            ):
                # Convert event to SSE format
                event_data = json.dumps(event, default=str)
                yield f"data: {event_data}\n\n"
                await asyncio.sleep(0.1)  # Small delay for streaming
                
            yield "data: {\"status\": \"completed\"}\n\n"
            
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@app.get("/api/reports/{filename}")
async def download_report(filename: str):
    """Download a generated report."""
    reports_dir = "./reports"
    filepath = os.path.join(reports_dir, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        filepath,
        media_type="application/octet-stream",
        filename=filename
    )


@app.get("/api/examples")
async def get_example_queries():
    """Get example queries for demonstration."""
    return {
        "examples": [
            {
                "query": "Analyze the market potential for Metformin in oncology indications",
                "description": "Market analysis for drug repurposing"
            },
            {
                "query": "What is the patent landscape for Pembrolizumab?",
                "description": "Patent and IP analysis"
            },
            {
                "query": "Show me active clinical trials for Rituximab in autoimmune diseases",
                "description": "Clinical trials search"
            },
            {
                "query": "Comprehensive analysis of drug repurposing opportunities in neurology",
                "description": "Multi-agent comprehensive analysis"
            },
            {
                "query": "Generate a report on Atorvastatin market trends and patent expiry",
                "description": "Report generation with multiple data sources"
            }
        ]
    }


# Run with: uvicorn api.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
