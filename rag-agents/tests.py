"""
Test suite for the Multi-Agent Drug Repurposing System.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestSyntheticDataGenerators:
    """Test synthetic data generation."""
    
    def test_iqvia_market_data(self):
        from data.synthetic_data import IQVIADataGenerator
        
        generator = IQVIADataGenerator()
        data = generator.generate_market_size_data("Metformin", "Oncology")
        
        assert "drug_name" in data
        assert "market_data" in data
        assert "cagr_5yr" in data
        assert len(data["market_data"]) > 0
    
    def test_iqvia_therapy_dynamics(self):
        from data.synthetic_data import IQVIADataGenerator
        
        generator = IQVIADataGenerator()
        data = generator.generate_therapy_dynamics("Cardiology")
        
        assert "therapy_area" in data
        assert "competitor_landscape" in data
        assert len(data["competitor_landscape"]) > 0
    
    def test_exim_trade_data(self):
        from data.synthetic_data import EXIMDataGenerator
        
        generator = EXIMDataGenerator()
        data = generator.generate_trade_data("API", "India")
        
        assert "trade_data" in data
        assert "top_export_destinations" in data
    
    def test_patent_data(self):
        from data.synthetic_data import PatentDataGenerator
        
        generator = PatentDataGenerator()
        data = generator.generate_patent_data("Adalimumab")
        
        assert "patents" in data
        assert "fto_status" in data
        assert len(data["patents"]) > 0
    
    def test_clinical_trials_data(self):
        from data.synthetic_data import ClinicalTrialsDataGenerator
        
        generator = ClinicalTrialsDataGenerator()
        data = generator.generate_trials_data("Pembrolizumab", "Cancer")
        
        assert "trials" in data
        assert "phase_distribution" in data
        assert len(data["trials"]) > 0


class TestAgents:
    """Test individual agents."""
    
    def test_iqvia_agent_execution(self):
        from agents import IQVIAInsightsAgent
        from schemas.models import AgentTask, AgentType, TaskStatus
        
        agent = IQVIAInsightsAgent()
        task = AgentTask(
            task_id="test_001",
            agent_type=AgentType.IQVIA,
            query="Market size for oncology",
            parameters={"therapy_area": "Oncology"}
        )
        
        response = agent.execute(task)
        
        assert response.status == TaskStatus.COMPLETED
        assert response.summary != ""
        assert response.execution_time_ms >= 0
    
    def test_patent_agent_execution(self):
        from agents import PatentLandscapeAgent
        from schemas.models import AgentTask, AgentType, TaskStatus
        
        agent = PatentLandscapeAgent()
        task = AgentTask(
            task_id="test_002",
            agent_type=AgentType.PATENT,
            query="Patent landscape analysis",
            parameters={"drug_name": "Adalimumab"}
        )
        
        response = agent.execute(task)
        
        assert response.status == TaskStatus.COMPLETED
        assert len(response.tables) > 0
    
    def test_clinical_trials_agent_execution(self):
        from agents import ClinicalTrialsAgent
        from schemas.models import AgentTask, AgentType, TaskStatus
        
        agent = ClinicalTrialsAgent()
        task = AgentTask(
            task_id="test_003",
            agent_type=AgentType.CLINICAL_TRIALS,
            query="Active clinical trials",
            parameters={"drug_name": "Nivolumab"}
        )
        
        response = agent.execute(task)
        
        assert response.status == TaskStatus.COMPLETED
        assert "trials" in response.data or response.data.get("trials_data")


class TestMasterAgent:
    """Test master agent functionality."""
    
    def test_query_analysis(self):
        from orchestration.master_agent import MasterAgent
        
        agent = MasterAgent()
        analysis = agent.analyze_query("Analyze market potential for Metformin in oncology")
        
        assert "original_query" in analysis
        assert "intents" in analysis
        assert "required_agents" in analysis
        assert "drug_name" in analysis
    
    def test_drug_extraction(self):
        from orchestration.master_agent import MasterAgent
        
        agent = MasterAgent()
        analysis = agent.analyze_query("What is the patent status for Adalimumab?")
        
        assert analysis["drug_name"] == "Adalimumab"
    
    def test_therapy_extraction(self):
        from orchestration.master_agent import MasterAgent
        
        agent = MasterAgent()
        analysis = agent.analyze_query("Show me the market for Cardiology drugs")
        
        assert analysis["therapy_area"] == "Cardiology"
    
    def test_task_planning(self):
        from orchestration.master_agent import MasterAgent
        from schemas.models import AgentType
        
        agent = MasterAgent()
        analysis = {
            "original_query": "Analyze Metformin",
            "drug_name": "Metformin",
            "therapy_area": None,
            "intents": ["market_analysis", "patent_analysis"],
            "required_agents": [AgentType.IQVIA, AgentType.PATENT],
            "needs_report": False,
            "parameters": {"drug_name": "Metformin"}
        }
        
        tasks = agent.create_task_plan(analysis)
        
        assert len(tasks) >= 2
        assert all(hasattr(t, "task_id") for t in tasks)


class TestOrchestrator:
    """Test the multi-agent orchestrator."""
    
    def test_orchestrator_initialization(self):
        from orchestration import create_orchestrator
        
        orchestrator = create_orchestrator()
        
        assert orchestrator is not None
        assert orchestrator.master_agent is not None
        assert len(orchestrator.worker_agents) == 7
    
    def test_simple_query(self):
        from orchestration import create_orchestrator
        from schemas.models import OutputFormat
        
        orchestrator = create_orchestrator()
        result = orchestrator.run(
            query="What is the market size for oncology?",
            output_format=OutputFormat.TEXT,
            include_charts=False,
            include_tables=False,
            generate_report=False
        )
        
        assert result["success"] == True
        assert "response" in result
        assert result["response"] != ""
    
    def test_multi_agent_query(self):
        from orchestration import create_orchestrator
        from schemas.models import OutputFormat
        
        orchestrator = create_orchestrator()
        result = orchestrator.run(
            query="Analyze Metformin including market size, patents, and clinical trials",
            output_format=OutputFormat.TEXT,
            include_charts=True,
            include_tables=True,
            generate_report=False
        )
        
        assert result["success"] == True
        assert len(result.get("agent_responses", [])) >= 2


class TestState:
    """Test state management."""
    
    def test_initial_state_creation(self):
        from orchestration.state import create_initial_state
        from schemas.models import OutputFormat
        
        state = create_initial_state(
            user_query="Test query",
            output_format=OutputFormat.TEXT
        )
        
        assert state["user_query"] == "Test query"
        assert state["status"] == "initialized"
        assert len(state["tasks"]) == 0


class TestSchemas:
    """Test Pydantic schemas."""
    
    def test_agent_task_creation(self):
        from schemas.models import AgentTask, AgentType, TaskStatus
        
        task = AgentTask(
            task_id="test_task",
            agent_type=AgentType.IQVIA,
            query="Test query",
            parameters={"key": "value"}
        )
        
        assert task.task_id == "test_task"
        assert task.status == TaskStatus.PENDING
    
    def test_agent_response_creation(self):
        from schemas.models import AgentResponse, AgentType, TaskStatus
        
        response = AgentResponse(
            agent_type=AgentType.PATENT,
            task_id="test_task",
            status=TaskStatus.COMPLETED,
            summary="Test summary"
        )
        
        assert response.summary == "Test summary"
        assert response.status == TaskStatus.COMPLETED


def run_tests():
    """Run all tests."""
    print("Running Multi-Agent System Tests...")
    print("=" * 60)
    
    # Test synthetic data
    print("\n1. Testing Synthetic Data Generators...")
    test_data = TestSyntheticDataGenerators()
    test_data.test_iqvia_market_data()
    test_data.test_iqvia_therapy_dynamics()
    test_data.test_exim_trade_data()
    test_data.test_patent_data()
    test_data.test_clinical_trials_data()
    print("   ✓ All synthetic data tests passed")
    
    # Test agents
    print("\n2. Testing Individual Agents...")
    test_agents = TestAgents()
    test_agents.test_iqvia_agent_execution()
    test_agents.test_patent_agent_execution()
    test_agents.test_clinical_trials_agent_execution()
    print("   ✓ All agent tests passed")
    
    # Test master agent
    print("\n3. Testing Master Agent...")
    test_master = TestMasterAgent()
    test_master.test_query_analysis()
    test_master.test_drug_extraction()
    test_master.test_therapy_extraction()
    test_master.test_task_planning()
    print("   ✓ All master agent tests passed")
    
    # Test schemas
    print("\n4. Testing Schemas...")
    test_schemas = TestSchemas()
    test_schemas.test_agent_task_creation()
    test_schemas.test_agent_response_creation()
    print("   ✓ All schema tests passed")
    
    # Test state
    print("\n5. Testing State Management...")
    test_state = TestState()
    test_state.test_initial_state_creation()
    print("   ✓ All state tests passed")
    
    # Test orchestrator
    print("\n6. Testing Orchestrator...")
    test_orch = TestOrchestrator()
    test_orch.test_orchestrator_initialization()
    test_orch.test_simple_query()
    test_orch.test_multi_agent_query()
    print("   ✓ All orchestrator tests passed")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed successfully!")


if __name__ == "__main__":
    run_tests()
