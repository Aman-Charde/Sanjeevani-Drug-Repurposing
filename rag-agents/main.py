"""
Drug Repurposing Multi-Agent Intelligence Platform

Main entry point for the application.
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestration import create_orchestrator, MultiAgentOrchestrator
from schemas.models import OutputFormat


def main():
    """Main entry point."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║          🧬 Drug Repurposing Multi-Agent Intelligence Platform 🧬            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Starting the multi-agent system...
    """)
    
    # Initialize orchestrator
    orchestrator = create_orchestrator()
    
    # Example query
    query = "Analyze the market potential and patent landscape for Metformin in oncology"
    
    print(f"📝 Sample Query: {query}\n")
    print("=" * 80)
    
    # Run the query
    result = orchestrator.run(
        query=query,
        output_format=OutputFormat.TEXT,
        include_charts=True,
        include_tables=True,
        generate_report=False
    )
    
    if result.get("success"):
        print(result.get("response", "No response"))
    else:
        print(f"Error: {result.get('error')}")
    
    print("\n" + "=" * 80)
    print("\nTo run the API server: python -m uvicorn api.main:app --reload")
    print("To run interactive CLI: python cli.py --interactive")


if __name__ == "__main__":
    main()
