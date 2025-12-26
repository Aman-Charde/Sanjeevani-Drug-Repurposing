"""
Patent Landscape Agent - Searches patent databases for IP analysis.
"""
from typing import Dict, Any, List

from agents.base_agent import BaseAgent
from schemas.models import AgentType
from data.synthetic_data import PatentDataGenerator


class PatentLandscapeAgent(BaseAgent):
    """Agent for patent landscape and IP analysis."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.PATENT, **kwargs)
        self.data_generator = PatentDataGenerator()
    
    def _get_system_prompt(self) -> str:
        return """You are a Patent Landscape Agent specialized in pharmaceutical IP analysis.
        
Your expertise includes:
- Patent search and analysis (USPTO, EPO, WIPO)
- Patent expiry timeline assessment
- Freedom to Operate (FTO) analysis
- Patent filing trends and competitive intelligence
- IP strategy recommendations

You provide insights on patent status, expiry dates, and competitive IP positioning.
Format outputs with patent tables, expiry timelines, and filing heatmaps."""
    
    def _process_query(self, query: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process patent-related queries."""
        query_lower = query.lower()
        
        drug_name = parameters.get("drug_name")
        therapy_area = parameters.get("therapy_area")
        
        tables = []
        charts = []
        data = {}
        summary = ""
        references = ["USPTO Patent Database", "European Patent Office", "WIPO"]
        
        if any(term in query_lower for term in ["patent", "ip", "expiry", "fto"]):
            patent_data = self.data_generator.generate_patent_data(drug_name)
            data["patent_data"] = patent_data
            
            # Patent status table
            tables.append(self._format_table(
                title=f"Patent Portfolio - {patent_data['drug_name']}",
                headers=["Patent Number", "Type", "Assignee", "Filing Date", "Expiry Date", "Status"],
                rows=[[p["patent_number"], p["patent_type"], p["assignee"], 
                       p["filing_date"], p["expiry_date"], p["status"]] 
                      for p in patent_data["patents"]]
            ))
            
            # Patent type distribution chart
            type_counts = {}
            for p in patent_data["patents"]:
                type_counts[p["patent_type"]] = type_counts.get(p["patent_type"], 0) + 1
            
            charts.append(self._format_chart(
                chart_type="pie",
                title=f"Patent Type Distribution - {patent_data['drug_name']}",
                data={
                    "labels": list(type_counts.keys()),
                    "values": list(type_counts.values())
                }
            ))
            
            fto_indicator = "🟢 Clear" if patent_data["fto_status"] == "Clear" else (
                "🟡 Potential Issues" if patent_data["fto_status"] == "Potential Issues" else "🔴 Blocked"
            )
            
            summary = f"""**Patent Landscape Analysis: {patent_data['drug_name']}**

📋 **Total Patents:** {patent_data['total_patents']}
✅ **Active Patents:** {patent_data['active_patents']}
📅 **Earliest Expiry:** {patent_data['earliest_expiry']}
⚖️ **FTO Status:** {patent_data['fto_status']} {fto_indicator}
🔄 **Litigation History:** {'Yes' if patent_data['litigation_history'] else 'No'}

**Key Patent Holders:**
{chr(10).join('• ' + holder for holder in patent_data['key_patent_holders'])}

**Strategic Implications:**
• {'Patent cliff approaching - generic entry expected' if patent_data['earliest_expiry'] < '2026-01-01' else 'Strong IP protection continues'}
• {'Consider licensing discussions' if patent_data['fto_status'] != 'Clear' else 'FTO pathway available'}"""
        
        elif any(term in query_lower for term in ["heatmap", "filing", "trend", "competitive"]):
            heatmap_data = self.data_generator.generate_patent_heatmap(therapy_area)
            data["heatmap_data"] = heatmap_data
            
            # Pivot data for table
            companies = list(set(d["company"] for d in heatmap_data["heatmap_data"]))
            years = sorted(set(d["year"] for d in heatmap_data["heatmap_data"]))
            
            rows = []
            for company in companies:
                row = [company]
                for year in years:
                    filings = next((d["filings"] for d in heatmap_data["heatmap_data"] 
                                   if d["company"] == company and d["year"] == year), 0)
                    row.append(filings)
                rows.append(row)
            
            tables.append(self._format_table(
                title=f"Patent Filing Heatmap - {heatmap_data['therapy_area']}",
                headers=["Company"] + [str(y) for y in years],
                rows=rows
            ))
            
            charts.append(self._format_chart(
                chart_type="heatmap",
                title=f"Patent Filing Activity - {heatmap_data['therapy_area']}",
                data={
                    "companies": companies,
                    "years": years,
                    "values": [[next((d["filings"] for d in heatmap_data["heatmap_data"] 
                                     if d["company"] == c and d["year"] == y), 0) 
                               for y in years] for c in companies]
                }
            ))
            
            summary = f"""**Patent Filing Trends: {heatmap_data['therapy_area']}**

🏆 **Top Filer:** {heatmap_data['top_filer']}
📊 **2024 Total Filings:** {heatmap_data['total_filings_2024']}
📈 **Trend:** {heatmap_data['trend']}

**Competitive Intelligence:**
• Patent activity indicates {'increasing' if heatmap_data['total_filings_2024'] > 300 else 'stable'} R&D investment
• {heatmap_data['top_filer']} is leading IP development
• Multiple players competing for IP position"""
        
        else:
            # Comprehensive patent analysis
            patent_data = self.data_generator.generate_patent_data(drug_name)
            heatmap_data = self.data_generator.generate_patent_heatmap(therapy_area)
            
            data = {"patent_data": patent_data, "heatmap_data": heatmap_data}
            
            summary = f"""**Comprehensive Patent Analysis**

**Drug-Specific IP ({patent_data['drug_name']}):**
• Active Patents: {patent_data['active_patents']}/{patent_data['total_patents']}
• FTO Status: {patent_data['fto_status']}
• Earliest Expiry: {patent_data['earliest_expiry']}

**Therapy Area Filings ({heatmap_data['therapy_area']}):**
• Top Filer: {heatmap_data['top_filer']}
• 2024 Activity: {heatmap_data['total_filings_2024']} filings"""
        
        return {
            "data": data,
            "summary": summary,
            "tables": tables,
            "charts": charts,
            "references": references
        }
