"""
Command Line Interface for Multi-Agent Drug Repurposing System.
"""
import argparse
import sys
import json
from datetime import datetime
from typing import Optional

from orchestration import create_orchestrator
from schemas.models import OutputFormat, AGENT_CAPABILITIES


def print_header():
    """Print application header."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║          🧬 Drug Repurposing Multi-Agent Intelligence Platform 🧬            ║
║                                                                              ║
║   AI-driven tool for exploring potential drug innovation cases              ║
║   Using LangChain + LangGraph Multi-Agent Orchestration                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)


def print_agents():
    """Print available agents."""
    print("\n📋 Available Agents:")
    print("=" * 60)
    for agent_type, caps in AGENT_CAPABILITIES.items():
        print(f"\n🤖 {agent_type.value.replace('_', ' ').title()}")
        print(f"   {caps.description}")
        print(f"   Example: {caps.example_queries[0]}")
    print()


def run_query(
    query: str,
    output_format: str = "text",
    generate_report: bool = False,
    verbose: bool = False
) -> None:
    """Run a query through the multi-agent system."""
    
    print(f"\n🔍 Processing Query: {query}")
    print("-" * 60)
    
    # Create orchestrator
    print("⏳ Initializing multi-agent system...")
    orchestrator = create_orchestrator()
    
    # Map output format
    format_map = {
        "text": OutputFormat.TEXT,
        "json": OutputFormat.JSON,
        "pdf": OutputFormat.PDF,
        "excel": OutputFormat.EXCEL
    }
    fmt = format_map.get(output_format.lower(), OutputFormat.TEXT)
    
    # Run query
    start_time = datetime.now()
    
    if verbose:
        print("\n📊 Streaming execution:")
        for event in orchestrator.run_stream(
            query=query,
            output_format=fmt,
            include_charts=True,
            include_tables=True,
            generate_report=generate_report
        ):
            for node_name, state_update in event.items():
                print(f"  ✓ {node_name}: {state_update.get('status', 'processing')}")
    else:
        result = orchestrator.run(
            query=query,
            output_format=fmt,
            include_charts=True,
            include_tables=True,
            generate_report=generate_report
        )
    
    execution_time = (datetime.now() - start_time).total_seconds()
    
    print("\n" + "=" * 60)
    print("📝 RESPONSE:")
    print("=" * 60)
    
    if verbose:
        print("\n[Streaming completed - final state shown above]")
    else:
        if result.get("success"):
            print(result.get("response", "No response generated"))
            
            if result.get("report_path"):
                print(f"\n📄 Report generated: {result['report_path']}")
        else:
            print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    print("\n" + "-" * 60)
    print(f"⏱️  Execution time: {execution_time:.2f}s")
    print("-" * 60)


def interactive_mode():
    """Run in interactive mode."""
    print_header()
    print_agents()
    
    print("📝 Enter your research queries (type 'exit' to quit, 'help' for options)")
    print("-" * 60)
    
    orchestrator = create_orchestrator()
    
    while True:
        try:
            query = input("\n🔹 Query: ").strip()
            
            if not query:
                continue
            
            if query.lower() == 'exit':
                print("👋 Goodbye!")
                break
            
            if query.lower() == 'help':
                print("\nCommands:")
                print("  exit     - Exit the program")
                print("  help     - Show this help")
                print("  agents   - List available agents")
                print("  report   - Add 'report' to your query to generate PDF")
                print("\nExample queries:")
                for caps in list(AGENT_CAPABILITIES.values())[:3]:
                    print(f"  - {caps.example_queries[0]}")
                continue
            
            if query.lower() == 'agents':
                print_agents()
                continue
            
            # Check if report generation requested
            generate_report = 'report' in query.lower()
            
            # Run query
            print("\n⏳ Processing...")
            result = orchestrator.run(
                query=query,
                output_format=OutputFormat.TEXT,
                include_charts=True,
                include_tables=True,
                generate_report=generate_report
            )
            
            print("\n" + "=" * 60)
            if result.get("success"):
                print(result.get("response", "No response"))
                if result.get("report_path"):
                    print(f"\n📄 Report: {result['report_path']}")
            else:
                print(f"❌ Error: {result.get('error')}")
            print("=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Drug Repurposing Multi-Agent System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py -q "Analyze market for Metformin in oncology"
  python cli.py -q "Patent landscape for Pembrolizumab" --report
  python cli.py --interactive
  python cli.py --agents
        """
    )
    
    parser.add_argument(
        "-q", "--query",
        type=str,
        help="Research query to process"
    )
    
    parser.add_argument(
        "-f", "--format",
        type=str,
        choices=["text", "json", "pdf", "excel"],
        default="text",
        help="Output format (default: text)"
    )
    
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate a downloadable report"
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    
    parser.add_argument(
        "--agents",
        action="store_true",
        help="List available agents"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output with streaming updates"
    )
    
    args = parser.parse_args()
    
    if args.agents:
        print_header()
        print_agents()
        return
    
    if args.interactive:
        interactive_mode()
        return
    
    if args.query:
        print_header()
        run_query(
            query=args.query,
            output_format=args.format,
            generate_report=args.report,
            verbose=args.verbose
        )
        return
    
    # No arguments - show help
    parser.print_help()


if __name__ == "__main__":
    main()
