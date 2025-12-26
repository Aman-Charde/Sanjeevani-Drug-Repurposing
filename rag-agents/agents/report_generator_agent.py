"""
Report Generator Agent - Formats synthesized responses into polished reports.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
import uuid
import json
import logging

from agents.base_agent import BaseAgent
from schemas.models import AgentType, AgentResponse, OutputFormat

logger = logging.getLogger(__name__)


class ReportGeneratorAgent(BaseAgent):
    """Agent for generating formatted PDF and Excel reports."""
    
    def __init__(self, reports_dir: str = "./reports", **kwargs):
        super().__init__(agent_type=AgentType.REPORT_GENERATOR, **kwargs)
        self.reports_dir = reports_dir
        os.makedirs(reports_dir, exist_ok=True)
    
    def _get_system_prompt(self) -> str:
        return """You are a Report Generator Agent specialized in creating professional pharmaceutical reports.
        
Your expertise includes:
- Executive summary generation
- Data visualization and formatting
- Professional document structuring
- PDF and Excel report creation
- Chart and table integration

You create polished, professional reports suitable for executive review.
Ensure reports are well-organized with clear sections, visualizations, and actionable insights."""
    
    def _process_query(self, query: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process report generation queries."""
        
        # Get agent responses to compile
        agent_responses: List[AgentResponse] = parameters.get("agent_responses", [])
        title = parameters.get("title", "Drug Repurposing Research Report")
        output_format = parameters.get("output_format", OutputFormat.PDF)
        
        # Compile report data
        report_data = self._compile_report_data(agent_responses, title)
        
        # Generate report based on format
        if output_format == OutputFormat.PDF:
            report_path = self._generate_pdf_report(report_data)
        elif output_format == OutputFormat.EXCEL:
            report_path = self._generate_excel_report(report_data)
        else:
            report_path = self._generate_text_report(report_data)
        
        summary = f"""**Report Generated Successfully**

📄 **Title:** {report_data['title']}
📁 **Format:** {output_format.value.upper()}
📅 **Generated:** {report_data['generated_at']}
📊 **Sections:** {len(report_data['sections'])}
📈 **Tables:** {report_data['table_count']}
📉 **Charts:** {report_data['chart_count']}

**Report Location:** `{report_path}`

**Contents:**
{chr(10).join(f"• {section['title']}" for section in report_data['sections'])}"""
        
        return {
            "data": {
                "report_data": report_data,
                "report_path": report_path
            },
            "summary": summary,
            "tables": [],
            "charts": [],
            "references": [f"Report: {report_path}"]
        }
    
    def _compile_report_data(
        self, 
        agent_responses: List[AgentResponse], 
        title: str
    ) -> Dict[str, Any]:
        """Compile data from agent responses into report structure."""
        
        sections = []
        all_tables = []
        all_charts = []
        all_references = []
        
        # If we have actual agent responses
        if agent_responses:
            for response in agent_responses:
                if isinstance(response, dict):
                    sections.append({
                        "title": response.get("agent_type", "Analysis"),
                        "content": response.get("summary", ""),
                        "data": response.get("data", {})
                    })
                    all_tables.extend(response.get("tables", []))
                    all_charts.extend(response.get("charts", []))
                    all_references.extend(response.get("references", []))
                elif hasattr(response, 'agent_type'):
                    sections.append({
                        "title": f"{response.agent_type.value.replace('_', ' ').title()} Analysis",
                        "content": response.summary,
                        "data": response.data
                    })
                    all_tables.extend(response.tables)
                    all_charts.extend(response.charts)
                    all_references.extend(response.references)
        else:
            # Generate sample sections for demonstration
            sections = [
                {
                    "title": "Executive Summary",
                    "content": "This report provides a comprehensive analysis of drug repurposing opportunities.",
                    "data": {}
                },
                {
                    "title": "Market Analysis",
                    "content": "Market analysis indicates significant opportunities in the selected therapy areas.",
                    "data": {}
                },
                {
                    "title": "Patent Landscape",
                    "content": "Patent analysis reveals favorable FTO status for potential development.",
                    "data": {}
                },
                {
                    "title": "Clinical Development",
                    "content": "Clinical trial landscape shows active development with multiple sponsors.",
                    "data": {}
                },
                {
                    "title": "Recommendations",
                    "content": "Based on the analysis, we recommend proceeding with further evaluation.",
                    "data": {}
                }
            ]
        
        return {
            "report_id": str(uuid.uuid4()),
            "title": title,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sections": sections,
            "tables": all_tables,
            "charts": all_charts,
            "references": list(set(all_references)),
            "table_count": len(all_tables),
            "chart_count": len(all_charts)
        }
    
    def _generate_pdf_report(self, report_data: Dict[str, Any]) -> str:
        """Generate a PDF report."""
        try:
            from fpdf import FPDF
            
            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            
            # Title page
            pdf.add_page()
            pdf.set_font("Arial", "B", 24)
            pdf.cell(0, 60, "", ln=True)  # Spacing
            pdf.multi_cell(0, 15, report_data["title"], align="C")
            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 20, "", ln=True)
            pdf.cell(0, 10, f"Generated: {report_data['generated_at']}", align="C", ln=True)
            pdf.cell(0, 10, "Drug Repurposing Intelligence Platform", align="C", ln=True)
            
            # Table of Contents
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "Table of Contents", ln=True)
            pdf.set_font("Arial", "", 12)
            for i, section in enumerate(report_data["sections"], 1):
                pdf.cell(0, 8, f"{i}. {section['title']}", ln=True)
            
            # Sections
            for section in report_data["sections"]:
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, section["title"], ln=True)
                pdf.set_font("Arial", "", 11)
                
                # Clean content for PDF (remove markdown)
                content = section["content"]
                content = content.replace("**", "").replace("*", "")
                content = content.replace("###", "").replace("##", "").replace("#", "")
                
                pdf.multi_cell(0, 6, content)
            
            # Tables
            if report_data["tables"]:
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "Data Tables", ln=True)
                
                for table in report_data["tables"][:5]:  # Limit tables
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(0, 8, table.get("title", "Table"), ln=True)
                    pdf.set_font("Arial", "", 10)
                    
                    # Simple table representation
                    headers = table.get("headers", [])
                    if headers:
                        pdf.cell(0, 6, " | ".join(str(h) for h in headers), ln=True)
                        for row in table.get("rows", [])[:10]:
                            pdf.cell(0, 5, " | ".join(str(cell) for cell in row), ln=True)
                    pdf.cell(0, 5, "", ln=True)
            
            # References
            if report_data["references"]:
                pdf.add_page()
                pdf.set_font("Arial", "B", 16)
                pdf.cell(0, 10, "References", ln=True)
                pdf.set_font("Arial", "", 10)
                for ref in report_data["references"]:
                    pdf.cell(0, 6, f"- {ref}", ln=True)
            
            # Save PDF
            filename = f"report_{report_data['report_id'][:8]}.pdf"
            filepath = os.path.join(self.reports_dir, filename)
            pdf.output(filepath)
            
            return filepath
            
        except ImportError:
            logger.warning("FPDF not available, generating text report instead")
            return self._generate_text_report(report_data)
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return self._generate_text_report(report_data)
    
    def _generate_excel_report(self, report_data: Dict[str, Any]) -> str:
        """Generate an Excel report."""
        try:
            import pandas as pd
            
            filename = f"report_{report_data['report_id'][:8]}.xlsx"
            filepath = os.path.join(self.reports_dir, filename)
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Summary sheet
                summary_data = {
                    "Field": ["Report ID", "Title", "Generated At", "Sections", "Tables", "Charts"],
                    "Value": [
                        report_data["report_id"],
                        report_data["title"],
                        report_data["generated_at"],
                        len(report_data["sections"]),
                        report_data["table_count"],
                        report_data["chart_count"]
                    ]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name="Summary", index=False)
                
                # Sections sheet
                sections_data = []
                for section in report_data["sections"]:
                    sections_data.append({
                        "Section": section["title"],
                        "Content": section["content"][:500]  # Truncate for Excel
                    })
                pd.DataFrame(sections_data).to_excel(writer, sheet_name="Sections", index=False)
                
                # Tables sheets
                for i, table in enumerate(report_data["tables"][:10]):  # Limit tables
                    headers = table.get("headers", [f"Col{j}" for j in range(5)])
                    rows = table.get("rows", [])
                    if rows:
                        df = pd.DataFrame(rows, columns=headers[:len(rows[0])] if rows else headers)
                        sheet_name = f"Table_{i+1}"[:31]  # Excel sheet name limit
                        df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # References sheet
                if report_data["references"]:
                    pd.DataFrame({"References": report_data["references"]}).to_excel(
                        writer, sheet_name="References", index=False
                    )
            
            return filepath
            
        except ImportError:
            logger.warning("Pandas/openpyxl not available, generating text report instead")
            return self._generate_text_report(report_data)
        except Exception as e:
            logger.error(f"Excel generation failed: {e}")
            return self._generate_text_report(report_data)
    
    def _generate_text_report(self, report_data: Dict[str, Any]) -> str:
        """Generate a text/markdown report."""
        
        filename = f"report_{report_data['report_id'][:8]}.md"
        filepath = os.path.join(self.reports_dir, filename)
        
        content = f"""# {report_data['title']}

**Generated:** {report_data['generated_at']}
**Report ID:** {report_data['report_id']}

---

## Table of Contents

"""
        for i, section in enumerate(report_data["sections"], 1):
            content += f"{i}. {section['title']}\n"
        
        content += "\n---\n\n"
        
        for section in report_data["sections"]:
            content += f"## {section['title']}\n\n{section['content']}\n\n---\n\n"
        
        if report_data["tables"]:
            content += "## Data Tables\n\n"
            for table in report_data["tables"]:
                content += f"### {table.get('title', 'Table')}\n\n"
                headers = table.get("headers", [])
                rows = table.get("rows", [])
                if headers and rows:
                    content += "| " + " | ".join(str(h) for h in headers) + " |\n"
                    content += "| " + " | ".join("---" for _ in headers) + " |\n"
                    for row in rows[:20]:
                        content += "| " + " | ".join(str(cell) for cell in row) + " |\n"
                content += "\n"
        
        if report_data["references"]:
            content += "## References\n\n"
            for ref in report_data["references"]:
                content += f"- {ref}\n"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return filepath
