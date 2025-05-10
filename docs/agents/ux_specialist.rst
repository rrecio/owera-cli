UX Specialist
============

The UX Specialist agent is responsible for optimizing user experience and accessibility in the generated applications.

Responsibilities
--------------

1. **User Flow Analysis**
   - Create user flow diagrams
   - Identify optimal user paths
   - Document user interactions

2. **Accessibility Compliance**
   - Check WCAG 2.1 compliance
   - Implement accessibility features
   - Generate accessibility reports

3. **Usability Testing**
   - Perform usability analysis
   - Identify improvement areas
   - Generate usability reports

4. **User Journey Mapping**
   - Create user journey maps
   - Document touchpoints
   - Track user emotions

Tools
-----

The UX Specialist has access to the following tools:

.. code-block:: python

    self.tools = {
        "user_flow": self.create_user_flow,
        "accessibility_check": self.check_accessibility,
        "usability_test": self.perform_usability_test,
        "user_journey": self.create_user_journey
    }

API Reference
------------

.. autoclass:: owera.agents.ux_specialist.UXSpecialist
   :members:
   :undoc-members:
   :show-inheritance:

Methods
-------

.. automethod:: owera.agents.ux_specialist.UXSpecialist.create_user_flow
.. automethod:: owera.agents.ux_specialist.UXSpecialist.check_accessibility
.. automethod:: owera.agents.ux_specialist.UXSpecialist.perform_usability_test
.. automethod:: owera.agents.ux_specialist.UXSpecialist.create_user_journey

Example Usage
------------

.. code-block:: python

    from owera.agents import UXSpecialist
    from owera.models import Feature, Project, Task

    # Create agent
    ux_specialist = UXSpecialist()

    # Create sample feature
    feature = Feature(
        name="User Authentication",
        description="Implement secure user authentication system"
    )

    # Create sample project
    project = Project(
        name="Test Project",
        type="Web Application",
        target_users="General users",
        requirements=["Security", "Usability", "Accessibility"]
    )

    # Create task
    task = Task(
        description="Analyze UX for authentication system",
        feature=feature
    )

    # Generate prompt
    prompt = ux_specialist.generate_prompt(task, project)

    # Process response
    response = """
    User Flow Analysis:
    - Login page
    - Registration page
    - Password reset
    
    Accessibility Recommendations:
    - Add ARIA labels
    - Ensure keyboard navigation
    
    Usability Improvements:
    - Simplify form layout
    - Add clear error messages
    """
    
    ux_specialist.process_response(response, task, project)

Output Format
------------

The UX Specialist generates structured output in the following format:

.. code-block:: json

    {
        "user_flow": {
            "nodes": [],
            "edges": [],
            "recommendations": []
        },
        "accessibility": [],
        "usability": {
            "issues": [],
            "recommendations": []
        },
        "user_journey": {
            "stages": [],
            "touchpoints": [],
            "emotions": []
        }
    }

Best Practices
-------------

1. **User Flow Design**
   - Keep flows simple and intuitive
   - Minimize steps in critical paths
   - Provide clear feedback

2. **Accessibility**
   - Follow WCAG 2.1 guidelines
   - Test with screen readers
   - Ensure keyboard navigation

3. **Usability**
   - Focus on user needs
   - Test with real users
   - Iterate based on feedback

4. **Documentation**
   - Document all decisions
   - Provide clear rationale
   - Include examples 