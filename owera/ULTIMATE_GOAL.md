Develop a command-line interface (CLI) tool named "owera" that automates custom software development by orchestrating a team of AI agents. The tool takes a J file containing detailed application specifications as input and generates a complete, production-ready software product. Owera parses the specs, delegates tasks to specialized AI agents, and manages an iterative Agile-based process to deliver source code, documentation, and supporting artifacts in a specified output directory. The process concludes when the product fully meets the specifications, passes rigorous validation, and is approved by relevant agents.

The AI agents and their roles, actions, and tools are:
- UI Specialist: Creates responsive, visually appealing interface designs using Figma (for mockups) and CSS frameworks (e.g., Tailwind CSS). Outputs design files and style guides.
- UX Specialist: Optimizes usability and accessibility using UX research tools (e.g., user flow diagrams, accessibility checkers like WAVE). Produces user journey maps and accessibility reports.
- QA Specialist: Conducts automated and manual tests using pytest (unit tests), Selenium (integration tests), and Lighthouse (performance). Generates test reports and bug tickets.
- Project Manager: Coordinates tasks, tracks progress, and manages timelines using a task graph and Trello-like prioritization logic. Outputs sprint plans and progress logs.
- Product Owner: Aligns the product with specs, prioritizes features, and validates deliverables using specification checklists. Provides feature approval or revision requests.
- Stakeholder: Evaluates business alignment using ROI analysis and market fit criteria. Submits strategic feedback or approval.
- Developers: Write clean, modular code in the specified language (e.g., Python, JavaScript) using Git for version control and VS Code for editing. Generate source code and commit logs.

The iterative development process follows Agile principles with clear steps:
1. Initialization: Owera parses the JSON specs (e.g., features, tech stack, constraints) and initializes agents, creating a task backlog.
2. Planning: Project Manager assigns tasks based on dependencies and priorities; Product Owner refines feature scope.
3. Design: UI and UX Specialists produce designs and usability plans, validated by Product Owner.
4. Implementation: Developers code features, integrating designs and committing changes to a Git repository.
5. Testing: QA Specialist runs tests, logs bugs, and assigns fixes to Developers.
6. Review: Product Owner verifies spec compliance; Stakeholder confirms business goals; feedback triggers adjustments.
7. Adjustment: Agents resolve issues (e.g., bugs, missing features) and prepare for the next iteration.

The cycle repeats until all features are implemented, tests pass, and Product Owner/Stakeholder approve.

Final output includes:
- Source code (organized by module, e.g., `src/`, with Git repository)
- Documentation (README.md, API docs via Sphinx, user guide)
- Artifacts (design files, test reports, configuration files)
- Logs (detailed agent actions, timestamps, and decisions in `logs/development.log`)

Key requirements:
- Simplicity: CLI command is `owera --spec specs.json --output my_app`.
- Tools: Agents use industry-standard tools (e.g., Git, pytest, Tailwind CSS) simulated via APIs or libraries.
- Interactions: Realistic agent collaboration (e.g., QA submits bug tickets to Developers, Product Owner clarifies specs with Developers).
- Validation: Product Owner ensures 100% spec compliance; QA guarantees zero critical bugs.
- Extensibility: Supports multiple languages/tech stacks (e.g., Python/Django, JavaScript/React) based on specs.

The goal is a fully automated, transparent, and efficient development process that mirrors a professional software lifecycle, delivering a high-quality product with minimal user input.