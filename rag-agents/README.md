# Drug Repurposing Multi-Agent Intelligence Platform

## 🧬 Overview

An AI-driven multi-agent system for exploring potential drug innovation and repurposing cases using **LangChain** and **LangGraph**. This platform significantly reduces research time and increases throughput by coordinating specialized AI agents to analyze market data, patents, clinical trials, and more.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           User Interface                                │
│                    (CLI / REST API / Web Dashboard)                     │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────────────┐
│                         Master Agent                                     │
│              (Conversation Orchestrator / LangGraph)                     │
│  • Query interpretation    • Task delegation    • Response synthesis    │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼───────┐  ┌─────────────▼───────────┐  ┌────────▼────────┐
│ IQVIA Insights │  │   Patent Landscape     │  │ Clinical Trials │
│     Agent      │  │        Agent           │  │     Agent       │
└───────┬───────┘  └─────────────┬───────────┘  └────────┬────────┘
        │                        │                        │
┌───────▼───────┐  ┌─────────────▼───────────┐  ┌────────▼────────┐
│  EXIM Trends  │  │  Internal Knowledge    │  │Web Intelligence │
│     Agent     │  │        Agent           │  │     Agent       │
└───────┬───────┘  └─────────────┬───────────┘  └────────┬────────┘
        │                        │                        │
        └────────────────────────┼────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   Report Generator     │
                    │        Agent           │
                    └─────────────────────────┘
```

## 🤖 Agent Capabilities

### Master Agent (Orchestrator)
- Interprets user queries and breaks them into modular research tasks
- Delegates tasks to domain-specific Worker Agents
- Synthesizes responses into coherent summaries with references
- Outputs: Text, tables, charts, or PDF reports

### Worker Agents

| Agent | Description | Outputs |
|-------|-------------|---------|
| **IQVIA Insights** | Queries market datasets for sales trends, volume shifts, therapy area dynamics | Market size tables, CAGR trends, competition summaries |
| **EXIM Trends** | Extracts export-import data for APIs/formulations | Trade volume charts, sourcing insights, dependency tables |
| **Patent Landscape** | Searches USPTO and IP databases for patents, expiry timelines, FTO flags | Patent status tables, filing heatmaps, PDF extracts |
| **Clinical Trials** | Fetches trial pipeline data from ClinicalTrials.gov | Trial tables, sponsor profiles, phase distributions |
| **Internal Knowledge** | Retrieves and summarizes internal documents | Key takeaways, comparative tables, briefing PDFs |
| **Web Intelligence** | Real-time web search for guidelines, publications, news | Hyperlinked summaries, quotations, guideline extracts |
| **Report Generator** | Formats synthesized response into polished reports | PDF summaries, Excel exports, downloadable links |

## 📁 Project Structure

```
drug repurposing/
├── agents/                     # Worker agent implementations
│   ├── __init__.py
│   ├── base_agent.py          # Abstract base agent class
│   ├── iqvia_agent.py         # IQVIA market insights
│   ├── exim_agent.py          # Export-import trends
│   ├── patent_agent.py        # Patent landscape analysis
│   ├── clinical_trials_agent.py
│   ├── internal_knowledge_agent.py
│   ├── web_intelligence_agent.py
│   └── report_generator_agent.py
├── api/                        # FastAPI REST API
│   ├── __init__.py
│   └── main.py
├── config/                     # Configuration
│   ├── __init__.py
│   └── settings.py
├── data/                       # Synthetic data generators
│   ├── __init__.py
│   └── synthetic_data.py
├── orchestration/              # LangGraph orchestration
│   ├── __init__.py
│   ├── state.py               # State definitions
│   ├── master_agent.py        # Master agent logic
│   └── graph.py               # LangGraph workflow
├── schemas/                    # Pydantic models
│   ├── __init__.py
│   └── models.py
├── reports/                    # Generated reports directory
├── cli.py                      # Command-line interface
├── demo.py                     # Demonstration script
├── main.py                     # Main entry point
├── requirements.txt            # Dependencies
└── .env.example               # Environment template
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd "e:\Drug-Repurposing-main\drug repurposing"

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration (Free Google Gemini API)

```bash
# Copy environment template
copy .env.example .env

# Get your FREE Google Gemini API key at:
# https://aistudio.google.com/app/apikey
# Then edit .env and add your key:
# GOOGLE_API_KEY=your_api_key_here
```

### 3. Run the System

**Option A: Command Line Interface**
```bash
# Interactive mode
python cli.py --interactive

# Single query
python cli.py -q "Analyze market potential for Metformin in oncology"

# Generate report
python cli.py -q "Patent landscape for Pembrolizumab" --report
```

**Option B: REST API Server**
```bash
# Start the server
python -m uvicorn api.main:app --reload

# API will be available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

**Option C: Demo Script**
```bash
python demo.py
```

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/api/health` | Health check |
| GET | `/api/agents` | List available agents |
| POST | `/api/query` | Process research query |
| POST | `/api/stream` | Streaming query execution |
| GET | `/api/reports/{filename}` | Download generated report |
| GET | `/api/examples` | Example queries |

### Example API Request

```bash
curl -X POST "http://localhost:8000/api/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze drug repurposing potential for Metformin in oncology",
    "output_format": "text",
    "include_charts": true,
    "include_tables": true,
    "generate_report": false
  }'
```

## 🔄 LangGraph Workflow

The system uses LangGraph for orchestrating the multi-agent workflow:

```
┌───────────────┐     ┌────────────┐     ┌───────────────┐
│ analyze_query │ ──▶ │ plan_tasks │ ──▶ │ execute_tasks │
└───────────────┘     └────────────┘     └───────┬───────┘
                                                 │
                                                 ▼
                      ┌────────────────────────────────────────┐
                      │                                        │
                      ▼                                        │
              ┌────────────┐                                   │
              │ synthesize │ ──────────────────────────────────┤
              └────────────┘                                   │
                      │                                        │
          ┌───────────┴───────────┐                           │
          ▼                       ▼                           │
┌──────────────────┐    ┌───────────────┐                    │
│ generate_report  │    │ format_output │ ◀──────────────────┘
└────────┬─────────┘    └───────┬───────┘
         │                      │
         └──────────┬───────────┘
                    ▼
                  [END]
```

## 📊 Example Queries

```
# Market Analysis
"What is the market size for oncology biologics?"
"Show sales trends for Metformin over the last 5 years"

# Patent Landscape
"Patent expiry timeline for Pembrolizumab"
"FTO analysis for biosimilar development in immunology"

# Clinical Trials
"Active Phase 3 trials for Nivolumab"
"Competitor pipeline analysis in cardiology"

# Comprehensive Analysis
"Comprehensive drug repurposing analysis for Metformin in cancer"
"Generate research report on Rituximab market opportunities"
```

## 🧪 Synthetic Data

The system includes synthetic data generators for demonstration:

- **IQVIA Data**: Market size, CAGR, therapy dynamics
- **EXIM Data**: Trade volumes, sourcing breakdown
- **Patent Data**: Patent portfolios, expiry timelines
- **Clinical Trials**: Trial pipelines, sponsor profiles
- **Internal Knowledge**: Strategy documents, field insights
- **Web Intelligence**: Search results, clinical guidelines

## 🔧 Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | **Google Gemini API key (FREE)** | Primary LLM provider |
| `OPENAI_API_KEY` | OpenAI API key (fallback) | Optional alternative |
| `DEBUG` | Enable debug mode | `true` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `HOST` | API server host | `0.0.0.0` |
| `PORT` | API server port | `8000` |

### 🆓 Getting Your Free Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and add it to your `.env` file

## 📈 Future Enhancements

- [ ] Real IQVIA API integration
- [ ] USPTO/EPO patent API integration
- [ ] ClinicalTrials.gov live API
- [ ] Vector store for document retrieval
- [ ] Web dashboard with visualizations
- [ ] Advanced report templates
- [ ] Multi-language support
- [ ] User authentication

## 📄 License

MIT License - See LICENSE file for details.

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

---

Built with ❤️ using **LangChain** and **LangGraph**
