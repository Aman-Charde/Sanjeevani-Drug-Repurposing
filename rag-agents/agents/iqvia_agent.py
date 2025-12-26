"""
IQVIA Insights Agent - Queries market data for sales trends and therapy area dynamics.
"""
from typing import Dict, Any, List
import json

from agents.base_agent import BaseAgent
from schemas.models import AgentType
from data.synthetic_data import IQVIADataGenerator


class IQVIAInsightsAgent(BaseAgent):
    """Agent for IQVIA market insights and sales data."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.IQVIA, **kwargs)
        self.data_generator = IQVIADataGenerator()
    
    def _get_system_prompt(self) -> str:
        return """You are an IQVIA Insights Agent specialized in pharmaceutical market analysis.
        
Your expertise includes:
- Market size analysis and forecasting
- Sales trends and volume analysis
- Therapy area dynamics and competition
- Geographic market distribution
- CAGR calculations and growth projections

You have access to IQVIA MIDAS and National Sales Perspectives data.
Provide accurate, data-driven insights with specific numbers and trends.
Format outputs with clear tables, charts, and actionable summaries."""
    
    def _process_query(self, query: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process IQVIA-related queries."""
        query_lower = query.lower()
        
        # Extract relevant parameters
        drug_name = parameters.get("drug_name")
        therapy_area = parameters.get("therapy_area")
        
        # Determine query type and generate appropriate data
        tables = []
        charts = []
        data = {}
        summary = ""
        references = ["IQVIA MIDAS Database", "IQVIA National Sales Perspectives"]
        
        if any(term in query_lower for term in ["market size", "market analysis", "sales"]):
            market_data = self.data_generator.generate_market_size_data(drug_name, therapy_area)
            data["market_data"] = market_data
            
            # Create market size table
            tables.append(self._format_table(
                title=f"Market Size Analysis - {market_data['drug_name']}",
                headers=["Year", "Market Size (USD M)", "Growth Rate (%)"],
                rows=[[d["year"], d["market_size_usd_millions"], d["growth_rate"]] 
                      for d in market_data["market_data"]]
            ))
            
            # Create chart data
            charts.append(self._format_chart(
                chart_type="line",
                title=f"Market Size Trend - {market_data['drug_name']}",
                data={
                    "x": [d["year"] for d in market_data["market_data"]],
                    "y": [d["market_size_usd_millions"] for d in market_data["market_data"]]
                },
                x_label="Year",
                y_label="Market Size (USD Millions)"
            ))
            
            summary = f"""**Market Analysis for {market_data['drug_name']}**

📊 **Current Market Size:** ${market_data['current_market_size']:,.2f}M
📈 **5-Year CAGR:** {market_data['cagr_5yr']}%
🎯 **2028 Forecast:** ${market_data['forecast_2028']:,.2f}M

**Top Markets:** {', '.join(market_data['top_markets'])}
**Market Leader:** {market_data['market_share_leader']}

The {market_data['therapy_area']} segment shows {'strong' if market_data['cagr_5yr'] > 8 else 'moderate'} growth trajectory."""
        
        elif any(term in query_lower for term in ["therapy", "dynamics", "competition"]):
            therapy_data = self.data_generator.generate_therapy_dynamics(therapy_area)
            data["therapy_dynamics"] = therapy_data
            
            tables.append(self._format_table(
                title=f"Competitive Landscape - {therapy_data['therapy_area']}",
                headers=["Company", "Market Share (%)"],
                rows=[[c["company"], c["market_share"]] for c in therapy_data["competitor_landscape"]]
            ))
            
            charts.append(self._format_chart(
                chart_type="pie",
                title=f"Market Share Distribution - {therapy_data['therapy_area']}",
                data={
                    "labels": [c["company"] for c in therapy_data["competitor_landscape"]],
                    "values": [c["market_share"] for c in therapy_data["competitor_landscape"]]
                }
            ))
            
            summary = f"""**Therapy Area Dynamics: {therapy_data['therapy_area']}**

💰 **Total Market Size:** ${therapy_data['total_market_size_bn']}B
📊 **Projected Growth:** {therapy_data['projected_growth']}

**Key Trends:**
{chr(10).join('• ' + trend for trend in therapy_data['key_trends'])}

**Growth Drivers:**
{chr(10).join('• ' + driver for driver in therapy_data['growth_drivers'])}"""
        
        elif any(term in query_lower for term in ["volume", "prescription", "trend"]):
            volume_data = self.data_generator.generate_volume_trends(drug_name)
            data["volume_trends"] = volume_data
            
            tables.append(self._format_table(
                title=f"Prescription Volume Trends - {volume_data['drug_name']}",
                headers=["Quarter", "Prescriptions", "Change (%)"],
                rows=[[d["quarter"], f"{d['prescriptions']:,}", d["change_pct"]] 
                      for d in volume_data["volume_trend"]]
            ))
            
            charts.append(self._format_chart(
                chart_type="bar",
                title=f"Quarterly Prescription Volume - {volume_data['drug_name']}",
                data={
                    "x": [d["quarter"] for d in volume_data["volume_trend"]],
                    "y": [d["prescriptions"] for d in volume_data["volume_trend"]]
                },
                x_label="Quarter",
                y_label="Prescriptions"
            ))
            
            summary = f"""**Volume Analysis for {volume_data['drug_name']}**

📋 **YTD Total Prescriptions:** {volume_data['total_prescriptions_ytd']:,}
📈 **Avg Quarterly Growth:** {volume_data['avg_quarterly_growth']}%
📊 **Market Trend:** {volume_data['market_trend']}

**Geographic Distribution:**
{chr(10).join(f'• {region}: {share}%' for region, share in volume_data['geographic_distribution'].items())}"""
        
        else:
            # Default comprehensive analysis
            market_data = self.data_generator.generate_market_size_data(drug_name, therapy_area)
            therapy_data = self.data_generator.generate_therapy_dynamics(therapy_area)
            
            data = {"market_data": market_data, "therapy_dynamics": therapy_data}
            
            summary = f"""**Comprehensive IQVIA Market Analysis**

**Market Overview - {market_data['drug_name']}:**
• Current Market Size: ${market_data['current_market_size']:,.2f}M
• 5-Year CAGR: {market_data['cagr_5yr']}%

**{therapy_data['therapy_area']} Therapy Area:**
• Total Market: ${therapy_data['total_market_size_bn']}B
• Growth Outlook: {therapy_data['projected_growth']}"""
        
        return {
            "data": data,
            "summary": summary,
            "tables": tables,
            "charts": charts,
            "references": references
        }
