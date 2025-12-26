"""
Web Intelligence Agent - Performs real-time web search for guidelines and publications.
"""
from typing import Dict, Any, List

from agents.base_agent import BaseAgent
from schemas.models import AgentType
from data.synthetic_data import WebIntelligenceGenerator


class WebIntelligenceAgent(BaseAgent):
    """Agent for web search and guideline extraction."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.WEB_INTELLIGENCE, **kwargs)
        self.data_generator = WebIntelligenceGenerator()
    
    def _get_system_prompt(self) -> str:
        return """You are a Web Intelligence Agent specialized in real-time pharmaceutical intelligence.
        
Your expertise includes:
- Clinical guideline searches and summarization
- Scientific publication monitoring
- Industry news tracking
- Patient forum analysis
- Regulatory update monitoring

You provide hyperlinked summaries, credible quotations, and guideline extracts.
Format outputs with source attributions, relevance scores, and actionable insights."""
    
    def _process_query(self, query: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process web intelligence queries."""
        query_lower = query.lower()
        
        search_query = parameters.get("query") or query
        therapy_area = parameters.get("therapy_area")
        
        tables = []
        charts = []
        data = {}
        summary = ""
        references = []
        
        if any(term in query_lower for term in ["search", "news", "publication", "article"]):
            search_data = self.data_generator.generate_web_search_results(search_query)
            data["search_results"] = search_data
            
            tables.append(self._format_table(
                title=f"Search Results: {search_data['query']}",
                headers=["Title", "Source", "Category", "Date", "Relevance"],
                rows=[[r["title"][:50], r["source"], r["category"], r["date"], 
                       f"{r['relevance_score']:.0%}"] 
                      for r in search_data["results"]]
            ))
            
            # Add URLs as references
            references = [f"{r['source']}: {r['url']}" for r in search_data["results"]]
            
            results_text = []
            for r in search_data["results"][:5]:
                results_text.append(f"""
**[{r['title']}]({r['url']})**
*Source: {r['source']} | {r['date']} | Relevance: {r['relevance_score']:.0%}*
> {r['snippet']}""")
            
            summary = f"""**Web Search Results: {search_data['query']}**

🔍 **Total Results Found:** {search_data['total_results']}
⏱️ **Search Time:** {search_data['search_time_ms']}ms

**Top Results:**
{''.join(results_text)}

**Trending Topics:**
{chr(10).join('• ' + topic for topic in search_data['trending_topics'])}"""
        
        elif any(term in query_lower for term in ["guideline", "recommendation", "standard"]):
            guidelines_data = self.data_generator.generate_guidelines_summary(therapy_area)
            data["guidelines"] = guidelines_data
            
            for g in guidelines_data["guidelines"]:
                tables.append(self._format_table(
                    title=f"{g['organization']} Guidelines",
                    headers=["Recommendation", "Evidence Level"],
                    rows=[[rec, g["evidence_level"]] for rec in g["key_recommendations"]]
                ))
            
            references = [f"{g['organization']}: {g['url']}" for g in guidelines_data["guidelines"]]
            
            guidelines_text = []
            for g in guidelines_data["guidelines"]:
                guidelines_text.append(f"""
### {g['organization']} - {g['title']}
*Published: {g['publication_date']} | Evidence Level: {g['evidence_level']}*

**Key Recommendations:**
{chr(10).join('• ' + rec for rec in g['key_recommendations'])}

🔗 [Full Guidelines]({g['url']})""")
            
            summary = f"""**Clinical Guidelines Summary: {guidelines_data['therapy_area']}**
{''.join(guidelines_text)}

**Recent Updates:**
{chr(10).join('• ' + update for update in guidelines_data['recent_updates'])}"""
        
        else:
            # Comprehensive web intelligence
            search_data = self.data_generator.generate_web_search_results(search_query)
            guidelines_data = self.data_generator.generate_guidelines_summary(therapy_area)
            
            data = {"search_results": search_data, "guidelines": guidelines_data}
            references = [r["url"] for r in search_data["results"][:5]]
            
            summary = f"""**Web Intelligence Summary**

**Search Results ({search_data['query']}):**
• Found: {search_data['total_results']} results
• Top Sources: {', '.join(search_data['top_sources'][:3])}

**Active Guidelines ({guidelines_data['therapy_area']}):**
• {len(guidelines_data['guidelines'])} relevant guidelines found
• Recent focus: {guidelines_data['recent_updates'][0] if guidelines_data['recent_updates'] else 'N/A'}"""
        
        return {
            "data": data,
            "summary": summary,
            "tables": tables,
            "charts": charts,
            "references": references
        }
