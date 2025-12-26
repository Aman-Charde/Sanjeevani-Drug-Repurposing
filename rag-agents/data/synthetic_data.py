"""
Synthetic Data Generators for Multi-Agent System.
Provides realistic synthetic data for drug repurposing research.
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any


# Common drug and therapy area data
THERAPY_AREAS = [
    "Oncology", "Cardiology", "Neurology", "Immunology", "Infectious Diseases",
    "Metabolic Disorders", "Respiratory", "Dermatology", "Ophthalmology", "Rare Diseases"
]

DRUG_NAMES = [
    "Remdesivir", "Metformin", "Aspirin", "Lisinopril", "Atorvastatin",
    "Omeprazole", "Amlodipine", "Gabapentin", "Sertraline", "Losartan",
    "Sildenafil", "Tadalafil", "Duloxetine", "Pregabalin", "Celecoxib",
    "Rituximab", "Pembrolizumab", "Nivolumab", "Adalimumab", "Infliximab"
]

COMPANIES = [
    "Pfizer", "Johnson & Johnson", "Roche", "Novartis", "Merck",
    "AbbVie", "Bristol-Myers Squibb", "AstraZeneca", "GSK", "Sanofi",
    "Eli Lilly", "Gilead Sciences", "Amgen", "Novo Nordisk", "Bayer"
]

COUNTRIES = [
    "USA", "Germany", "China", "India", "Japan", "UK", "France",
    "Switzerland", "Canada", "South Korea", "Brazil", "Australia"
]

FORMULATION_TYPES = [
    "Tablets", "Capsules", "Injectables", "API", "Topical",
    "Oral Solution", "Patches", "Inhalers", "Suppositories"
]


class IQVIADataGenerator:
    """Generate synthetic IQVIA-style market data."""
    
    @staticmethod
    def generate_market_size_data(drug_name: str = None, therapy_area: str = None) -> Dict[str, Any]:
        """Generate market size and sales data."""
        drug = drug_name or random.choice(DRUG_NAMES)
        therapy = therapy_area or random.choice(THERAPY_AREAS)
        
        base_market_size = random.uniform(500, 15000)  # millions USD
        years = list(range(2019, 2025))
        
        market_data = []
        current_size = base_market_size * 0.7
        
        for year in years:
            growth = random.uniform(0.03, 0.15)
            current_size *= (1 + growth)
            market_data.append({
                "year": year,
                "market_size_usd_millions": round(current_size, 2),
                "growth_rate": round(growth * 100, 1)
            })
        
        cagr = ((market_data[-1]["market_size_usd_millions"] / market_data[0]["market_size_usd_millions"]) ** (1/5) - 1) * 100
        
        return {
            "drug_name": drug,
            "therapy_area": therapy,
            "market_data": market_data,
            "cagr_5yr": round(cagr, 2),
            "current_market_size": round(current_size, 2),
            "forecast_2028": round(current_size * (1 + cagr/100) ** 4, 2),
            "top_markets": random.sample(COUNTRIES[:6], 3),
            "market_share_leader": random.choice(COMPANIES),
            "data_source": "IQVIA MIDAS",
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
    
    @staticmethod
    def generate_therapy_dynamics(therapy_area: str = None) -> Dict[str, Any]:
        """Generate therapy area market dynamics."""
        therapy = therapy_area or random.choice(THERAPY_AREAS)
        
        competitors = random.sample(COMPANIES, random.randint(4, 8))
        market_shares = []
        remaining = 100
        
        for i, company in enumerate(competitors[:-1]):
            share = random.uniform(5, min(35, remaining - 5 * (len(competitors) - i - 1)))
            market_shares.append({"company": company, "market_share": round(share, 1)})
            remaining -= share
        market_shares.append({"company": competitors[-1], "market_share": round(remaining, 1)})
        market_shares.sort(key=lambda x: x["market_share"], reverse=True)
        
        return {
            "therapy_area": therapy,
            "total_market_size_bn": round(random.uniform(20, 180), 1),
            "competitor_landscape": market_shares,
            "key_trends": [
                f"Shift towards {random.choice(['biologics', 'gene therapy', 'personalized medicine'])}",
                f"Increasing focus on {random.choice(['combination therapies', 'first-line treatments', 'adjuvant therapy'])}",
                f"Growing {random.choice(['biosimilar', 'generic', 'novel mechanism'])} competition"
            ],
            "growth_drivers": [
                "Aging population demographics",
                "Increased disease awareness",
                "New diagnostic capabilities"
            ],
            "projected_growth": f"{random.uniform(5, 12):.1f}% CAGR through 2028"
        }
    
    @staticmethod
    def generate_volume_trends(drug_name: str = None) -> Dict[str, Any]:
        """Generate prescription volume trends."""
        drug = drug_name or random.choice(DRUG_NAMES)
        
        quarters = ["Q1'23", "Q2'23", "Q3'23", "Q4'23", "Q1'24", "Q2'24", "Q3'24", "Q4'24"]
        base_volume = random.randint(1000000, 50000000)
        
        volume_data = []
        current_vol = base_volume
        
        for quarter in quarters:
            change = random.uniform(-0.05, 0.10)
            current_vol = int(current_vol * (1 + change))
            volume_data.append({
                "quarter": quarter,
                "prescriptions": current_vol,
                "change_pct": round(change * 100, 1)
            })
        
        return {
            "drug_name": drug,
            "volume_trend": volume_data,
            "total_prescriptions_ytd": sum(d["prescriptions"] for d in volume_data[-4:]),
            "avg_quarterly_growth": round(sum(d["change_pct"] for d in volume_data) / len(volume_data), 2),
            "market_trend": random.choice(["Growing", "Stable", "Declining"]),
            "geographic_distribution": {
                "North America": random.randint(30, 50),
                "Europe": random.randint(20, 35),
                "Asia-Pacific": random.randint(15, 25),
                "Rest of World": random.randint(5, 15)
            }
        }


class EXIMDataGenerator:
    """Generate synthetic export-import trade data."""
    
    @staticmethod
    def generate_trade_data(product: str = None, country: str = None) -> Dict[str, Any]:
        """Generate export-import trade data."""
        product_name = product or random.choice(DRUG_NAMES + FORMULATION_TYPES)
        target_country = country or random.choice(COUNTRIES)
        
        trade_data = []
        for year in range(2020, 2025):
            exports = random.uniform(50, 500)  # millions USD
            imports = random.uniform(30, 400)
            trade_data.append({
                "year": year,
                "exports_usd_millions": round(exports, 2),
                "imports_usd_millions": round(imports, 2),
                "trade_balance": round(exports - imports, 2),
                "volume_mt": random.randint(1000, 50000)
            })
        
        return {
            "product": product_name,
            "country": target_country,
            "trade_data": trade_data,
            "top_export_destinations": random.sample(COUNTRIES, 5),
            "top_import_sources": random.sample(COUNTRIES, 5),
            "yoy_export_growth": f"{random.uniform(-5, 25):.1f}%",
            "hs_code": f"30{random.randint(10, 49):02d}.{random.randint(10, 99)}",
            "data_source": "UN Comtrade"
        }
    
    @staticmethod
    def generate_api_sourcing_data(api_name: str = None) -> Dict[str, Any]:
        """Generate API sourcing and dependency data."""
        api = api_name or random.choice(DRUG_NAMES)
        
        sourcing_countries = random.sample(COUNTRIES, random.randint(3, 6))
        sourcing_data = []
        remaining = 100
        
        for i, country in enumerate(sourcing_countries[:-1]):
            share = random.uniform(10, min(50, remaining - 5 * (len(sourcing_countries) - i - 1)))
            sourcing_data.append({
                "country": country,
                "share_pct": round(share, 1),
                "key_manufacturers": random.randint(2, 8),
                "avg_price_kg": round(random.uniform(50, 5000), 2)
            })
            remaining -= share
        sourcing_data.append({
            "country": sourcing_countries[-1],
            "share_pct": round(remaining, 1),
            "key_manufacturers": random.randint(1, 5),
            "avg_price_kg": round(random.uniform(50, 5000), 2)
        })
        
        return {
            "api_name": api,
            "global_production_mt": random.randint(100, 10000),
            "sourcing_breakdown": sourcing_data,
            "supply_risk_score": random.randint(1, 10),
            "price_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "alternative_sources_available": random.choice([True, False]),
            "quality_certifications_required": ["WHO-GMP", "FDA", "EU-GMP"][:random.randint(1, 3)]
        }


class PatentDataGenerator:
    """Generate synthetic patent landscape data."""
    
    @staticmethod
    def generate_patent_data(drug_name: str = None) -> Dict[str, Any]:
        """Generate patent information for a drug."""
        drug = drug_name or random.choice(DRUG_NAMES)
        
        patents = []
        for i in range(random.randint(3, 8)):
            filing_date = datetime.now() - timedelta(days=random.randint(365, 7300))
            expiry_date = filing_date + timedelta(days=20*365)
            
            patents.append({
                "patent_number": f"US{random.randint(7000000, 11999999)}",
                "title": f"{random.choice(['Composition', 'Method', 'Formulation', 'Process'])} for {drug} {random.choice(['Treatment', 'Delivery', 'Synthesis', 'Administration'])}",
                "assignee": random.choice(COMPANIES),
                "filing_date": filing_date.strftime("%Y-%m-%d"),
                "expiry_date": expiry_date.strftime("%Y-%m-%d"),
                "status": random.choice(["Active", "Active", "Active", "Expired", "Pending"]),
                "patent_type": random.choice(["Compound", "Formulation", "Process", "Use"]),
                "claims_count": random.randint(10, 50)
            })
        
        return {
            "drug_name": drug,
            "patents": patents,
            "total_patents": len(patents),
            "active_patents": sum(1 for p in patents if p["status"] == "Active"),
            "earliest_expiry": min(p["expiry_date"] for p in patents if p["status"] == "Active"),
            "fto_status": random.choice(["Clear", "Potential Issues", "Blocked"]),
            "key_patent_holders": list(set(p["assignee"] for p in patents))[:3],
            "litigation_history": random.choice([True, False]),
            "data_sources": ["USPTO", "EPO", "WIPO"]
        }
    
    @staticmethod
    def generate_patent_heatmap(therapy_area: str = None) -> Dict[str, Any]:
        """Generate patent filing heatmap by company and year."""
        therapy = therapy_area or random.choice(THERAPY_AREAS)
        companies = random.sample(COMPANIES, 6)
        years = list(range(2019, 2025))
        
        heatmap_data = []
        for company in companies:
            for year in years:
                heatmap_data.append({
                    "company": company,
                    "year": year,
                    "filings": random.randint(5, 150)
                })
        
        return {
            "therapy_area": therapy,
            "heatmap_data": heatmap_data,
            "top_filer": max(companies, key=lambda c: sum(
                d["filings"] for d in heatmap_data if d["company"] == c
            )),
            "total_filings_2024": sum(d["filings"] for d in heatmap_data if d["year"] == 2024),
            "trend": "Increasing IP activity in " + therapy
        }


class ClinicalTrialsDataGenerator:
    """Generate synthetic clinical trials data."""
    
    TRIAL_PHASES = ["Phase 1", "Phase 1/2", "Phase 2", "Phase 2/3", "Phase 3", "Phase 4"]
    TRIAL_STATUS = ["Recruiting", "Active, not recruiting", "Completed", "Enrolling by invitation", "Not yet recruiting"]
    
    @staticmethod
    def generate_trials_data(drug_name: str = None, indication: str = None) -> Dict[str, Any]:
        """Generate clinical trials pipeline data."""
        drug = drug_name or random.choice(DRUG_NAMES)
        condition = indication or random.choice(THERAPY_AREAS) + " " + random.choice(["Cancer", "Disease", "Disorder", "Syndrome", "Condition"])
        
        trials = []
        for i in range(random.randint(5, 15)):
            start_date = datetime.now() - timedelta(days=random.randint(30, 1825))
            
            trials.append({
                "nct_id": f"NCT{random.randint(10000000, 99999999)}",
                "title": f"Study of {drug} in {condition}",
                "phase": random.choice(ClinicalTrialsDataGenerator.TRIAL_PHASES),
                "status": random.choice(ClinicalTrialsDataGenerator.TRIAL_STATUS),
                "sponsor": random.choice(COMPANIES),
                "start_date": start_date.strftime("%Y-%m-%d"),
                "enrollment": random.randint(20, 2000),
                "study_type": random.choice(["Interventional", "Observational"]),
                "primary_endpoint": random.choice([
                    "Overall Survival", "Progression-Free Survival",
                    "Objective Response Rate", "Safety and Tolerability",
                    "Pharmacokinetics", "Disease-Free Survival"
                ]),
                "locations": random.sample(COUNTRIES, random.randint(1, 8))
            })
        
        phase_distribution = {}
        for phase in ClinicalTrialsDataGenerator.TRIAL_PHASES:
            count = sum(1 for t in trials if t["phase"] == phase)
            if count > 0:
                phase_distribution[phase] = count
        
        return {
            "drug_name": drug,
            "indication": condition,
            "trials": trials,
            "total_trials": len(trials),
            "phase_distribution": phase_distribution,
            "active_trials": sum(1 for t in trials if t["status"] in ["Recruiting", "Active, not recruiting"]),
            "top_sponsors": list(set(t["sponsor"] for t in trials))[:5],
            "total_enrollment": sum(t["enrollment"] for t in trials),
            "data_source": "ClinicalTrials.gov"
        }
    
    @staticmethod
    def generate_competitor_pipeline(therapy_area: str = None) -> Dict[str, Any]:
        """Generate competitor pipeline analysis."""
        therapy = therapy_area or random.choice(THERAPY_AREAS)
        
        pipeline = []
        for company in random.sample(COMPANIES, 8):
            for phase in ClinicalTrialsDataGenerator.TRIAL_PHASES[:5]:
                if random.random() > 0.3:
                    pipeline.append({
                        "company": company,
                        "phase": phase,
                        "drug_candidates": random.randint(1, 5),
                        "lead_indication": f"{therapy} {random.choice(['Cancer', 'Disease', 'Disorder'])}"
                    })
        
        return {
            "therapy_area": therapy,
            "pipeline_data": pipeline,
            "total_candidates": sum(p["drug_candidates"] for p in pipeline),
            "most_active_company": max(COMPANIES[:8], key=lambda c: sum(
                p["drug_candidates"] for p in pipeline if p["company"] == c
            )),
            "phase_3_leaders": [p["company"] for p in pipeline if p["phase"] == "Phase 3"][:3]
        }


class InternalKnowledgeGenerator:
    """Generate synthetic internal document summaries."""
    
    @staticmethod
    def generate_internal_document(topic: str = None) -> Dict[str, Any]:
        """Generate internal document summary."""
        doc_topic = topic or random.choice([
            "Market Entry Strategy", "Competitive Analysis",
            "Product Development Roadmap", "Regulatory Strategy",
            "Commercial Launch Plan", "Portfolio Review"
        ])
        
        return {
            "document_title": f"{doc_topic} - {random.choice(THERAPY_AREAS)}",
            "document_type": random.choice(["Strategy Deck", "MINS Document", "Field Insight", "Research Brief"]),
            "created_date": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            "author": f"Strategy Team - {random.choice(['Global', 'Regional', 'Local'])}",
            "key_takeaways": [
                f"Market opportunity estimated at ${random.uniform(1, 20):.1f}B by 2028",
                f"Key competitor {random.choice(COMPANIES)} holds {random.randint(20, 40)}% market share",
                f"Recommended entry strategy: {random.choice(['Organic growth', 'Partnership', 'Acquisition', 'Licensing'])}",
                f"Critical success factor: {random.choice(['Speed to market', 'Pricing strategy', 'KOL engagement', 'Real-world evidence'])}"
            ],
            "recommendations": [
                f"Prioritize {random.choice(['Phase 3 trials', 'regulatory submission', 'commercial preparation'])}",
                f"Consider {random.choice(['co-development', 'out-licensing', 'in-licensing'])} opportunities",
                f"Strengthen {random.choice(['medical affairs', 'market access', 'commercial'])} capabilities"
            ],
            "related_documents": [f"DOC-{random.randint(1000, 9999)}" for _ in range(3)],
            "confidentiality": random.choice(["Internal Only", "Confidential", "Restricted"])
        }
    
    @staticmethod
    def generate_field_insights(therapy_area: str = None) -> Dict[str, Any]:
        """Generate field intelligence summary."""
        therapy = therapy_area or random.choice(THERAPY_AREAS)
        
        return {
            "therapy_area": therapy,
            "collection_period": f"{(datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
            "kol_sentiment": {
                "positive": random.randint(40, 70),
                "neutral": random.randint(20, 40),
                "negative": random.randint(5, 20)
            },
            "key_themes": [
                f"Increasing interest in {random.choice(['combination therapy', 'early intervention', 'personalized treatment'])}",
                f"Concerns about {random.choice(['pricing', 'access', 'efficacy data', 'safety profile'])}",
                f"Demand for {random.choice(['real-world evidence', 'head-to-head trials', 'long-term outcomes data'])}"
            ],
            "competitive_intelligence": [
                f"{random.choice(COMPANIES)} expected to launch new product Q{random.randint(1, 4)} 2025",
                f"{random.choice(COMPANIES)} facing supply chain challenges",
                f"New clinical data from {random.choice(COMPANIES)} creating buzz"
            ],
            "opportunities": [
                f"Unmet need in {random.choice(['resistant', 'refractory', 'early-stage', 'maintenance'])} patients",
                f"Opportunity for {random.choice(['differentiated', 'improved', 'convenient'])} formulation"
            ]
        }


class WebIntelligenceGenerator:
    """Generate synthetic web intelligence data."""
    
    @staticmethod
    def generate_web_search_results(query: str = None) -> Dict[str, Any]:
        """Generate web search results."""
        search_query = query or f"{random.choice(DRUG_NAMES)} {random.choice(['clinical trial', 'market analysis', 'approval', 'guidelines'])}"
        
        results = []
        sources = [
            ("FDA.gov", "Regulatory"),
            ("PubMed Central", "Scientific"),
            ("Reuters Health", "News"),
            ("BioPharma Dive", "Industry"),
            ("Nature Medicine", "Scientific"),
            ("Fierce Pharma", "Industry"),
            ("WHO.int", "Guidelines"),
            ("ClinicalTrials.gov", "Clinical")
        ]
        
        for source, category in random.sample(sources, random.randint(4, 7)):
            results.append({
                "title": f"{search_query.title()} - {random.choice(['New Findings', 'Update', 'Analysis', 'Report', 'Guidelines'])}",
                "source": source,
                "category": category,
                "url": f"https://www.{source.lower().replace(' ', '')}/article/{random.randint(10000, 99999)}",
                "snippet": f"Recent developments in {search_query} show promising results with {random.choice(['improved efficacy', 'better safety profile', 'novel mechanisms', 'enhanced outcomes'])}...",
                "date": (datetime.now() - timedelta(days=random.randint(1, 90))).strftime("%Y-%m-%d"),
                "relevance_score": round(random.uniform(0.7, 0.99), 2)
            })
        
        return {
            "query": search_query,
            "results": results,
            "total_results": random.randint(50, 500),
            "search_time_ms": random.randint(100, 500),
            "top_sources": list(set(r["source"] for r in results)),
            "trending_topics": [
                f"{random.choice(DRUG_NAMES)} approval",
                f"{random.choice(THERAPY_AREAS)} breakthrough",
                f"{random.choice(COMPANIES)} acquisition"
            ]
        }
    
    @staticmethod
    def generate_guidelines_summary(therapy_area: str = None) -> Dict[str, Any]:
        """Generate clinical guidelines summary."""
        therapy = therapy_area or random.choice(THERAPY_AREAS)
        
        return {
            "therapy_area": therapy,
            "guidelines": [
                {
                    "organization": random.choice(["ASCO", "ESMO", "AHA", "ACC", "IDSA", "AAN"]),
                    "title": f"{therapy} Treatment Guidelines {2024}",
                    "publication_date": f"{random.choice(['January', 'March', 'June', 'September'])} 2024",
                    "key_recommendations": [
                        f"First-line: {random.choice(DRUG_NAMES)} recommended for {random.choice(['monotherapy', 'combination'])}",
                        f"Consider {random.choice(DRUG_NAMES)} for {random.choice(['refractory', 'intolerant', 'high-risk'])} patients",
                        f"Biomarker testing recommended before treatment with {random.choice(DRUG_NAMES)}"
                    ],
                    "evidence_level": random.choice(["1A", "1B", "2A", "2B"]),
                    "url": f"https://guidelines.org/{therapy.lower().replace(' ', '-')}-2024"
                }
                for _ in range(random.randint(2, 4))
            ],
            "recent_updates": [
                f"New recommendations for {random.choice(['elderly', 'pediatric', 'pregnant'])} populations",
                f"Updated {random.choice(['dosing', 'monitoring', 'switching'])} guidelines",
                f"Integration of {random.choice(['biomarkers', 'companion diagnostics', 'ctDNA testing'])}"
            ]
        }


# Export all generators
__all__ = [
    "IQVIADataGenerator",
    "EXIMDataGenerator",
    "PatentDataGenerator",
    "ClinicalTrialsDataGenerator",
    "InternalKnowledgeGenerator",
    "WebIntelligenceGenerator",
    "THERAPY_AREAS",
    "DRUG_NAMES",
    "COMPANIES",
    "COUNTRIES"
]
