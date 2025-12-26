"""
Clinical Trials Agent - Fetches trial pipeline data from clinical trial registries.
"""
from typing import Dict, Any, List

from agents.base_agent import BaseAgent
from schemas.models import AgentType
from data.synthetic_data import ClinicalTrialsDataGenerator


class ClinicalTrialsAgent(BaseAgent):
    """Agent for clinical trials data and pipeline analysis."""
    
    def __init__(self, **kwargs):
        super().__init__(agent_type=AgentType.CLINICAL_TRIALS, **kwargs)
        self.data_generator = ClinicalTrialsDataGenerator()
    
    def _get_system_prompt(self) -> str:
        return """You are a Clinical Trials Agent specialized in pharmaceutical R&D pipeline analysis.
        
Your expertise includes:
- Clinical trial registry searches (ClinicalTrials.gov, WHO ICTRP)
- Trial pipeline analysis by phase and indication
- Sponsor and competitive trial analysis
- Enrollment trends and geographic distribution
- Endpoint and study design assessment

You provide insights on active trials, competitor pipelines, and development trends.
Format outputs with trial tables, phase distributions, and sponsor profiles."""
    
    def _process_query(self, query: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process clinical trials-related queries."""
        query_lower = query.lower()
        
        drug_name = parameters.get("drug_name")
        indication = parameters.get("indication") or parameters.get("therapy_area")
        
        tables = []
        charts = []
        data = {}
        summary = ""
        references = ["ClinicalTrials.gov", "WHO ICTRP", "EU Clinical Trials Register"]
        
        if any(term in query_lower for term in ["trial", "clinical", "study", "phase"]):
            trials_data = self.data_generator.generate_trials_data(drug_name, indication)
            data["trials_data"] = trials_data
            
            # Trials table
            tables.append(self._format_table(
                title=f"Clinical Trials - {trials_data['drug_name']}",
                headers=["NCT ID", "Phase", "Status", "Sponsor", "Enrollment", "Start Date"],
                rows=[[t["nct_id"], t["phase"], t["status"], t["sponsor"], 
                       t["enrollment"], t["start_date"]] 
                      for t in trials_data["trials"][:10]]  # Top 10
            ))
            
            # Phase distribution chart
            charts.append(self._format_chart(
                chart_type="bar",
                title=f"Phase Distribution - {trials_data['drug_name']}",
                data={
                    "x": list(trials_data["phase_distribution"].keys()),
                    "y": list(trials_data["phase_distribution"].values())
                },
                x_label="Phase",
                y_label="Number of Trials"
            ))
            
            # Status distribution
            status_counts = {}
            for t in trials_data["trials"]:
                status_counts[t["status"]] = status_counts.get(t["status"], 0) + 1
            
            charts.append(self._format_chart(
                chart_type="pie",
                title=f"Trial Status Distribution - {trials_data['drug_name']}",
                data={
                    "labels": list(status_counts.keys()),
                    "values": list(status_counts.values())
                }
            ))
            
            summary = f"""**Clinical Trials Analysis: {trials_data['drug_name']}**

📊 **Total Trials:** {trials_data['total_trials']}
✅ **Active Trials:** {trials_data['active_trials']}
👥 **Total Enrollment:** {trials_data['total_enrollment']:,} patients
🎯 **Indication:** {trials_data['indication']}

**Phase Distribution:**
{chr(10).join(f"• {phase}: {count} trials" for phase, count in trials_data['phase_distribution'].items())}

**Top Sponsors:**
{chr(10).join('• ' + sponsor for sponsor in trials_data['top_sponsors'][:3])}

**Development Status:**
• {'Strong late-stage pipeline' if trials_data['phase_distribution'].get('Phase 3', 0) > 2 else 'Early development stage'}
• {'Multiple sponsors active' if len(trials_data['top_sponsors']) > 3 else 'Limited sponsor activity'}"""
        
        elif any(term in query_lower for term in ["pipeline", "competitor", "landscape"]):
            pipeline_data = self.data_generator.generate_competitor_pipeline(indication)
            data["pipeline_data"] = pipeline_data
            
            # Aggregate by company
            company_totals = {}
            for p in pipeline_data["pipeline_data"]:
                company_totals[p["company"]] = company_totals.get(p["company"], 0) + p["drug_candidates"]
            
            tables.append(self._format_table(
                title=f"Competitor Pipeline - {pipeline_data['therapy_area']}",
                headers=["Company", "Phase", "Drug Candidates", "Lead Indication"],
                rows=[[p["company"], p["phase"], p["drug_candidates"], p["lead_indication"]] 
                      for p in pipeline_data["pipeline_data"][:15]]
            ))
            
            charts.append(self._format_chart(
                chart_type="bar",
                title=f"Pipeline by Company - {pipeline_data['therapy_area']}",
                data={
                    "x": list(company_totals.keys()),
                    "y": list(company_totals.values())
                },
                x_label="Company",
                y_label="Drug Candidates"
            ))
            
            summary = f"""**Competitor Pipeline Analysis: {pipeline_data['therapy_area']}**

🔬 **Total Candidates:** {pipeline_data['total_candidates']}
🏆 **Most Active Company:** {pipeline_data['most_active_company']}
🎯 **Phase 3 Leaders:** {', '.join(pipeline_data['phase_3_leaders']) if pipeline_data['phase_3_leaders'] else 'None identified'}

**Competitive Landscape:**
• High R&D activity indicates {'competitive' if pipeline_data['total_candidates'] > 30 else 'moderate'} market
• {pipeline_data['most_active_company']} is leading development efforts
• {'Multiple Phase 3 programs suggest near-term competition' if pipeline_data['phase_3_leaders'] else 'Limited late-stage competition'}"""
        
        else:
            # Comprehensive analysis
            trials_data = self.data_generator.generate_trials_data(drug_name, indication)
            pipeline_data = self.data_generator.generate_competitor_pipeline(indication)
            
            data = {"trials_data": trials_data, "pipeline_data": pipeline_data}
            
            summary = f"""**Comprehensive Clinical Development Analysis**

**Drug Trials ({trials_data['drug_name']}):**
• Total Trials: {trials_data['total_trials']}
• Active: {trials_data['active_trials']}
• Enrollment: {trials_data['total_enrollment']:,}

**Competitor Pipeline ({pipeline_data['therapy_area']}):**
• Total Candidates: {pipeline_data['total_candidates']}
• Leading Developer: {pipeline_data['most_active_company']}"""
        
        return {
            "data": data,
            "summary": summary,
            "tables": tables,
            "charts": charts,
            "references": references
        }
