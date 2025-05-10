import pytest
from owera.agents.stakeholder import Stakeholder
from owera.models.base import Task, Project, Feature

@pytest.fixture
def stakeholder():
    """Create a Stakeholder agent instance."""
    return Stakeholder()

@pytest.fixture
def sample_feature():
    """Create a sample feature for testing."""
    return Feature(
        name="E-commerce Integration",
        description="Implement e-commerce functionality with payment processing"
    )

@pytest.fixture
def sample_project():
    """Create a sample project for testing."""
    return Project(
        name="Online Store",
        type="E-commerce Platform",
        target_market="Retail consumers",
        business_goals=["Increase sales", "Reduce operational costs"],
        budget=100000,
        timeline="6 months"
    )

@pytest.fixture
def sample_task(sample_feature):
    """Create a sample task for testing."""
    return Task(
        description="Evaluate business value of e-commerce integration",
        feature=sample_feature
    )

def test_stakeholder_initialization(stakeholder):
    """Test Stakeholder initialization."""
    assert stakeholder.role == "Stakeholder"
    assert "roi_analysis" in stakeholder.tools
    assert "market_fit" in stakeholder.tools
    assert "business_value" in stakeholder.tools
    assert "risk_assessment" in stakeholder.tools

def test_generate_prompt(stakeholder, sample_task, sample_project):
    """Test prompt generation."""
    prompt = stakeholder.generate_prompt(sample_task, sample_project)
    assert "E-commerce Integration" in prompt
    assert "E-commerce Platform" in prompt
    assert "Retail consumers" in prompt
    assert "Increase sales" in prompt
    assert "100000" in prompt
    assert "6 months" in prompt

def test_perform_roi_analysis(stakeholder, sample_feature):
    """Test ROI analysis."""
    analysis = stakeholder.perform_roi_analysis(sample_feature)
    assert isinstance(analysis, dict)
    assert "investment" in analysis
    assert "returns" in analysis
    assert "roi" in analysis
    assert "payback_period" in analysis

def test_analyze_market_fit(stakeholder, sample_feature):
    """Test market fit analysis."""
    analysis = stakeholder.analyze_market_fit(sample_feature)
    assert isinstance(analysis, dict)
    assert "market_size" in analysis
    assert "competition" in analysis
    assert "differentiators" in analysis
    assert "opportunity" in analysis

def test_assess_business_value(stakeholder, sample_feature):
    """Test business value assessment."""
    assessment = stakeholder.assess_business_value(sample_feature)
    assert isinstance(assessment, dict)
    assert "strategic_alignment" in assessment
    assert "value_drivers" in assessment
    assert "impact_areas" in assessment

def test_assess_risks(stakeholder, sample_feature):
    """Test risk assessment."""
    risks = stakeholder.assess_risks(sample_feature)
    assert isinstance(risks, list)

def test_process_response(stakeholder, sample_task, sample_project):
    """Test response processing."""
    response = """
    ROI Analysis:
    - Investment: $50,000
    - Expected Returns: $150,000
    - ROI: 200%
    - Payback Period: 4 months
    
    Market Fit:
    - Market Size: $1B
    - Competition: Moderate
    - Differentiators: Advanced features
    
    Business Value:
    - Strategic Alignment: High
    - Value Drivers: Revenue growth
    
    Risk Assessment:
    - Technical risks
    - Market risks
    """
    
    stakeholder.process_response(response, sample_task, sample_project)
    assert hasattr(sample_task.feature, "business_validation")
    assert isinstance(sample_task.feature.business_validation, dict)

def test_extract_code(stakeholder):
    """Test code extraction."""
    response = "Some business analysis without code"
    code = stakeholder.extract_code(response)
    assert code == "" 