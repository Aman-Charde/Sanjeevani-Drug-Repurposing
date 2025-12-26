"""
Internal Knowledge Agent - Retrieves and summarizes internal documents.
"""
from typing import Dict, Any, List

from agents.base_agent import BaseAgent
from schemas.models import AgentType
from data.synthetic_data import InternalKnowledgeGenerator


class InternalKnowledgeAgent(BaseAgent):
    """Agent for internal document retrieval and summarization."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.INTERNAL_KNOWLEDGE, **kwargs)
        self.data_generator = InternalKnowledgeGenerator()
    
    def _get_system_prompt(self) -> str:
        return """You are an Internal Knowledge Agent specialized in retrieving and summarizing internal documents.
        
Your expertise includes:
- Strategy document analysis and summarization
- Field intelligence synthesis
- Competitive analysis reports
- Market intelligence documents
- Internal meeting notes (MINS)

You provide key takeaways, strategic insights, and comparative analyses from internal sources.
Format outputs with clear summaries, key points, and actionable recommendations."""
    
    def _process_query(self, query: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process internal knowledge queries."""
        query_lower = query.lower()
        
        topic = parameters.get("topic") or parameters.get("therapy_area")
        
        tables = []
        charts = []
        data = {}
        summary = ""
        references = ["Internal Knowledge Base", "Strategy Documents", "Field Reports"]
        
        if any(term in query_lower for term in ["document", "strategy", "internal", "mins"]):
            doc_data = self.data_generator.generate_internal_document(topic)
            data["document"] = doc_data
            
            tables.append(self._format_table(
                title="Document Summary",
                headers=["Field", "Value"],
                rows=[
                    ["Title", doc_data["document_title"]],
                    ["Type", doc_data["document_type"]],
                    ["Created", doc_data["created_date"]],
                    ["Author", doc_data["author"]],
                    ["Confidentiality", doc_data["confidentiality"]]
                ]
            ))
            
            summary = f"""**Internal Document Summary**

📄 **{doc_data['document_title']}**
📁 Type: {doc_data['document_type']}
📅 Date: {doc_data['created_date']}
👤 Author: {doc_data['author']}

**Key Takeaways:**
{chr(10).join('• ' + takeaway for takeaway in doc_data['key_takeaways'])}

**Strategic Recommendations:**
{chr(10).join('• ' + rec for rec in doc_data['recommendations'])}

**Related Documents:** {', '.join(doc_data['related_documents'])}

⚠️ *Confidentiality: {doc_data['confidentiality']}*"""
        
        elif any(term in query_lower for term in ["field", "insight", "intelligence", "kol"]):
            field_data = self.data_generator.generate_field_insights(topic)
            data["field_insights"] = field_data
            
            # KOL sentiment chart
            charts.append(self._format_chart(
                chart_type="pie",
                title=f"KOL Sentiment - {field_data['therapy_area']}",
                data={
                    "labels": ["Positive", "Neutral", "Negative"],
                    "values": [
                        field_data["kol_sentiment"]["positive"],
                        field_data["kol_sentiment"]["neutral"],
                        field_data["kol_sentiment"]["negative"]
                    ]
                }
            ))
            
            summary = f"""**Field Intelligence Summary: {field_data['therapy_area']}**

📅 **Collection Period:** {field_data['collection_period']}

**KOL Sentiment Analysis:**
🟢 Positive: {field_data['kol_sentiment']['positive']}%
🟡 Neutral: {field_data['kol_sentiment']['neutral']}%
🔴 Negative: {field_data['kol_sentiment']['negative']}%

**Key Themes:**
{chr(10).join('• ' + theme for theme in field_data['key_themes'])}

**Competitive Intelligence:**
{chr(10).join('• ' + intel for intel in field_data['competitive_intelligence'])}

**Opportunities Identified:**
{chr(10).join('• ' + opp for opp in field_data['opportunities'])}"""
        
        else:
            # Comprehensive internal knowledge
            doc_data = self.data_generator.generate_internal_document(topic)
            field_data = self.data_generator.generate_field_insights(topic)
            
            data = {"document": doc_data, "field_insights": field_data}
            
            summary = f"""**Internal Knowledge Summary**

**Latest Strategy Document:**
• {doc_data['document_title']}
• Key Focus: {doc_data['key_takeaways'][0] if doc_data['key_takeaways'] else 'N/A'}

**Field Insights ({field_data['therapy_area']}):**
• KOL Sentiment: {field_data['kol_sentiment']['positive']}% positive
• Key Theme: {field_data['key_themes'][0] if field_data['key_themes'] else 'N/A'}
• Top Opportunity: {field_data['opportunities'][0] if field_data['opportunities'] else 'N/A'}"""
        
        return {
            "data": data,
            "summary": summary,
            "tables": tables,
            "charts": charts,
            "references": references
        }
