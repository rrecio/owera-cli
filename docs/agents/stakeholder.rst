Stakeholder
==========

The Stakeholder agent is responsible for business alignment and strategic validation of the generated applications.

Responsibilities
--------------

1. **ROI Analysis**
   - Calculate investment costs
   - Estimate returns
   - Determine payback period

2. **Market Fit Assessment**
   - Analyze market size
   - Evaluate competition
   - Identify differentiators

3. **Business Value Evaluation**
   - Assess strategic alignment
   - Identify value drivers
   - Measure impact areas

4. **Risk Assessment**
   - Identify business risks
   - Evaluate technical risks
   - Propose mitigation strategies

Tools
-----

The Stakeholder has access to the following tools:

.. code-block:: python

    self.tools = {
        "roi_analysis": self.perform_roi_analysis,
        "market_fit": self.analyze_market_fit,
        "business_value": self.assess_business_value,
        "risk_assessment": self.assess_risks
    }

API Reference
------------

.. autoclass:: owera.agents.stakeholder.Stakeholder
   :members:
   :undoc-members:
   :show-inheritance:

Methods
-------

.. automethod:: owera.agents.stakeholder.Stakeholder.perform_roi_analysis
.. automethod:: owera.agents.stakeholder.Stakeholder.analyze_market_fit
.. automethod:: owera.agents.stakeholder.Stakeholder.assess_business_value
.. automethod:: owera.agents.stakeholder.Stakeholder.assess_risks

Example Usage
------------

.. code-block:: python

    from owera.agents import Stakeholder
    from owera.models import Feature, Project, Task

    # Create agent
    stakeholder = Stakeholder()

    # Create sample feature
    feature = Feature(
        name="E-commerce Integration",
        description="Implement e-commerce functionality with payment processing"
    )

    # Create sample project
    project = Project(
        name="Online Store",
        type="E-commerce Platform",
        target_market="Retail consumers",
        business_goals=["Increase sales", "Reduce operational costs"],
        budget=100000,
        timeline="6 months"
    )

    # Create task
    task = Task(
        description="Evaluate business value of e-commerce integration",
        feature=feature
    )

    # Generate prompt
    prompt = stakeholder.generate_prompt(task, project)

    # Process response
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
    
    stakeholder.process_response(response, task, project)

Output Format
------------

The Stakeholder generates structured output in the following format:

.. code-block:: json

    {
        "roi": {
            "investment": 0.0,
            "returns": 0.0,
            "roi": 0.0,
            "payback_period": 0
        },
        "market_fit": {
            "market_size": 0,
            "competition": [],
            "differentiators": [],
            "opportunity": 0.0
        },
        "business_value": {
            "strategic_alignment": 0.0,
            "value_drivers": [],
            "impact_areas": []
        },
        "risks": []
    }

Best Practices
-------------

1. **ROI Analysis**
   - Use realistic cost estimates
   - Consider all revenue streams
   - Account for time value of money

2. **Market Analysis**
   - Research market thoroughly
   - Identify key competitors
   - Highlight unique advantages

3. **Value Assessment**
   - Align with business goals
   - Quantify benefits
   - Consider long-term impact

4. **Risk Management**
   - Identify all potential risks
   - Prioritize by impact
   - Propose mitigation strategies

5. **Documentation**
   - Document assumptions
   - Provide data sources
   - Include confidence levels 