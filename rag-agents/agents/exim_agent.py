"""
EXIM Trends Agent - Extracts export-import data for APIs and formulations.
"""
from typing import Dict, Any, List

from agents.base_agent import BaseAgent
from schemas.models import AgentType
from data.synthetic_data import EXIMDataGenerator


class EXIMTrendsAgent(BaseAgent):
    """Agent for export-import trade data analysis."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.EXIM, **kwargs)
        self.data_generator = EXIMDataGenerator()
    
    def _get_system_prompt(self) -> str:
        return """You are an EXIM Trends Agent specialized in pharmaceutical trade analysis.
        
Your expertise includes:
- Export-import data analysis for APIs and formulations
- Trade volume and value trends
- Sourcing and supply chain analysis
- Import dependency assessment
- Trade balance calculations

You have access to UN Comtrade and national trade databases.
Provide insights on trade patterns, sourcing risks, and supply chain considerations.
Format outputs with clear trade tables, volume charts, and strategic insights."""
    
    def _process_query(self, query: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process EXIM-related queries."""
        query_lower = query.lower()
        
        product = parameters.get("product") or parameters.get("drug_name")
        country = parameters.get("country")
        api_name = parameters.get("api_name") or product
        
        tables = []
        charts = []
        data = {}
        summary = ""
        references = ["UN Comtrade Database", "National Trade Statistics"]
        
        if any(term in query_lower for term in ["trade", "export", "import", "volume"]):
            trade_data = self.data_generator.generate_trade_data(product, country)
            data["trade_data"] = trade_data
            
            tables.append(self._format_table(
                title=f"Trade Data - {trade_data['product']} ({trade_data['country']})",
                headers=["Year", "Exports (USD M)", "Imports (USD M)", "Trade Balance", "Volume (MT)"],
                rows=[[d["year"], d["exports_usd_millions"], d["imports_usd_millions"], 
                       d["trade_balance"], d["volume_mt"]] for d in trade_data["trade_data"]]
            ))
            
            charts.append(self._format_chart(
                chart_type="bar",
                title=f"Trade Volume Trend - {trade_data['product']}",
                data={
                    "x": [d["year"] for d in trade_data["trade_data"]],
                    "exports": [d["exports_usd_millions"] for d in trade_data["trade_data"]],
                    "imports": [d["imports_usd_millions"] for d in trade_data["trade_data"]]
                },
                x_label="Year",
                y_label="Value (USD Millions)"
            ))
            
            summary = f"""**Trade Analysis: {trade_data['product']} - {trade_data['country']}**

📦 **HS Code:** {trade_data['hs_code']}
📈 **YoY Export Growth:** {trade_data['yoy_export_growth']}

**Top Export Destinations:**
{chr(10).join('• ' + dest for dest in trade_data['top_export_destinations'][:3])}

**Top Import Sources:**
{chr(10).join('• ' + src for src in trade_data['top_import_sources'][:3])}"""
        
        elif any(term in query_lower for term in ["sourcing", "api", "supply", "dependency"]):
            sourcing_data = self.data_generator.generate_api_sourcing_data(api_name)
            data["sourcing_data"] = sourcing_data
            
            tables.append(self._format_table(
                title=f"API Sourcing Breakdown - {sourcing_data['api_name']}",
                headers=["Country", "Share (%)", "Key Manufacturers", "Avg Price (USD/kg)"],
                rows=[[s["country"], s["share_pct"], s["key_manufacturers"], s["avg_price_kg"]] 
                      for s in sourcing_data["sourcing_breakdown"]]
            ))
            
            charts.append(self._format_chart(
                chart_type="pie",
                title=f"API Sourcing Distribution - {sourcing_data['api_name']}",
                data={
                    "labels": [s["country"] for s in sourcing_data["sourcing_breakdown"]],
                    "values": [s["share_pct"] for s in sourcing_data["sourcing_breakdown"]]
                }
            ))
            
            risk_level = "🟢 Low" if sourcing_data["supply_risk_score"] <= 3 else (
                "🟡 Medium" if sourcing_data["supply_risk_score"] <= 6 else "🔴 High"
            )
            
            summary = f"""**API Sourcing Analysis: {sourcing_data['api_name']}**

🏭 **Global Production:** {sourcing_data['global_production_mt']:,} MT
⚠️ **Supply Risk Score:** {sourcing_data['supply_risk_score']}/10 ({risk_level})
📊 **Price Trend:** {sourcing_data['price_trend']}
🔄 **Alternative Sources:** {'Available' if sourcing_data['alternative_sources_available'] else 'Limited'}

**Quality Certifications Required:**
{chr(10).join('• ' + cert for cert in sourcing_data['quality_certifications_required'])}

**Sourcing Recommendations:**
• {'Diversify sourcing to reduce dependency' if sourcing_data['supply_risk_score'] > 5 else 'Current sourcing strategy is acceptable'}
• Consider {sourcing_data['sourcing_breakdown'][1]['country'] if len(sourcing_data['sourcing_breakdown']) > 1 else 'alternative'} as secondary source"""
        
        else:
            # Comprehensive trade analysis
            trade_data = self.data_generator.generate_trade_data(product, country)
            sourcing_data = self.data_generator.generate_api_sourcing_data(api_name)
            
            data = {"trade_data": trade_data, "sourcing_data": sourcing_data}
            
            summary = f"""**Comprehensive EXIM Analysis**

**Trade Overview - {trade_data['product']}:**
• Latest Trade Balance: ${trade_data['trade_data'][-1]['trade_balance']:.2f}M
• YoY Growth: {trade_data['yoy_export_growth']}

**Sourcing Assessment:**
• Global Production: {sourcing_data['global_production_mt']:,} MT
• Supply Risk: {sourcing_data['supply_risk_score']}/10"""
        
        return {
            "data": data,
            "summary": summary,
            "tables": tables,
            "charts": charts,
            "references": references
        }
