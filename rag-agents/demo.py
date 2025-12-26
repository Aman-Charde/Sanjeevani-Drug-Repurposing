"""
Demonstration script showcasing the Multi-Agent System capabilities.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestration import create_orchestrator
from schemas.models import OutputFormat
from datetime import datetime


def print_section(title: str):
    """Print section header."""
    print("\n" + "=" * 80)
    print(f"🔹 {title}")
    print("=" * 80 + "\n")


def demo_individual_agents():
    """Demonstrate individual agent capabilities."""
    from agents import (
        IQVIAInsightsAgent,
        EXIMTrendsAgent,
        PatentLandscapeAgent,
        ClinicalTrialsAgent,
        InternalKnowledgeAgent,
        WebIntelligenceAgent
    )
    from schemas.models import AgentTask
    import uuid
    
    print_section("Individual Agent Demonstrations")
    
    agents_demo = [
        (IQVIAInsightsAgent(), "What is the market size for oncology drugs?", 
         {"drug_name": "Pembrolizumab", "therapy_area": "Oncology"}),
        
        (EXIMTrendsAgent(), "Show API sourcing data for Metformin",
         {"api_name": "Metformin", "country": "India"}),
        
        (PatentLandscapeAgent(), "Patent landscape analysis",
         {"drug_name": "Adalimumab", "therapy_area": "Immunology"}),
        
        (ClinicalTrialsAgent(), "Active clinical trials",
         {"drug_name": "Nivolumab", "therapy_area": "Oncology"}),
        
        (InternalKnowledgeAgent(), "Field insights summary",
         {"therapy_area": "Cardiology"}),
        
        (WebIntelligenceAgent(), "Latest guidelines",
         {"therapy_area": "Neurology"})
    ]
    
    for agent, query, params in agents_demo:
        print(f"\n{'─' * 60}")
        print(f"🤖 Agent: {agent.agent_type.value.replace('_', ' ').title()}")
        print(f"📝 Query: {query}")
        print(f"{'─' * 60}")
        
        task = AgentTask(
            task_id=f"demo_{uuid.uuid4().hex[:8]}",
            agent_type=agent.agent_type,
            query=query,
            parameters=params
        )
        
        response = agent.execute(task)
        
        print(f"\n📊 Status: {response.status.value}")
        print(f"⏱️  Time: {response.execution_time_ms}ms")
        print(f"\n{response.summary[:500]}...")
        
        if response.tables:
            print(f"\n📈 Tables generated: {len(response.tables)}")
        if response.charts:
            print(f"📉 Charts generated: {len(response.charts)}")


def demo_multi_agent_queries():
    """Demonstrate multi-agent query processing."""
    print_section("Multi-Agent Orchestration Demonstrations")
    
    orchestrator = create_orchestrator()
    
    queries = [
        "Analyze the drug repurposing potential for Metformin in oncology indications",
        "What is the competitive landscape for biologics in immunology?",
        "Comprehensive analysis of Pembrolizumab including market, patents, and trials"
    ]
    
    for query in queries:
        print(f"\n{'─' * 60}")
        print(f"📝 Query: {query}")
        print(f"{'─' * 60}")
        
        start = datetime.now()
        result = orchestrator.run(
            query=query,
            output_format=OutputFormat.TEXT,
            include_charts=True,
            include_tables=True,
            generate_report=False
        )
        elapsed = (datetime.now() - start).total_seconds()
        
        if result.get("success"):
            response = result.get("response", "")
            # Truncate for demo
            if len(response) > 1500:
                response = response[:1500] + "\n\n... [truncated for demo]"
            print(response)
        else:
            print(f"❌ Error: {result.get('error')}")
        
        print(f"\n⏱️  Total time: {elapsed:.2f}s")
        print(f"🤖 Agents used: {len(result.get('agent_responses', []))}")


def demo_report_generation():
    """Demonstrate report generation."""
    print_section("Report Generation Demonstration")
    
    orchestrator = create_orchestrator()
    
    query = "Generate a comprehensive research report on Rituximab drug repurposing opportunities"
    
    print(f"📝 Query: {query}\n")
    
    result = orchestrator.run(
        query=query,
        output_format=OutputFormat.PDF,
        include_charts=True,
        include_tables=True,
        generate_report=True
    )
    
    if result.get("success"):
        print(result.get("response", ""))
        if result.get("report_path"):
            print(f"\n📄 Report saved to: {result['report_path']}")
    else:
        print(f"❌ Error: {result.get('error')}")


def demo_streaming():
    """Demonstrate streaming execution."""
    print_section("Streaming Execution Demonstration")
    
    orchestrator = create_orchestrator()
    
    query = "Analyze patent landscape for Adalimumab"
    
    print(f"📝 Query: {query}")
    print("\n📊 Streaming execution progress:")
    
    for event in orchestrator.run_stream(
        query=query,
        output_format=OutputFormat.TEXT,
        include_charts=False,
        include_tables=True,
        generate_report=False
    ):
        for node_name, state_update in event.items():
            status = state_update.get("status", "processing")
            print(f"  ✓ {node_name}: {status}")
    
    print("\n✅ Streaming completed!")


def main():
    """Run all demonstrations."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║       🧬 Drug Repurposing Multi-Agent System - Demonstration Suite 🧬        ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    print("""
This demonstration showcases:
1. Individual agent capabilities with synthetic data
2. Multi-agent orchestration and query processing
3. Report generation with formatted outputs
4. Streaming execution for real-time updates
    """)
    
    input("Press Enter to start the demonstrations...")
    
    # Run demonstrations
    demo_individual_agents()
    
    input("\nPress Enter to continue to multi-agent queries...")
    demo_multi_agent_queries()
    
    input("\nPress Enter to continue to report generation...")
    demo_report_generation()
    
    input("\nPress Enter to continue to streaming demo...")
    demo_streaming()
    
    print_section("Demonstration Complete!")
    print("""
Next steps:
1. Start the API server: python -m uvicorn api.main:app --reload
2. Run interactive CLI: python cli.py --interactive
3. Access API docs at: http://localhost:8000/docs
    """)


if __name__ == "__main__":
    main()
