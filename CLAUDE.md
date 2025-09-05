# TWS Trading App Context Engineering 
This file provides guidance for working with code in this repository.  
It contains rules for python development and deployment 

## Context File Structure
- All context files are located directly in the `ctx-ai` folder at the project root
- Key context files and folders include:
  - `CLAUDE.md` - This file with project guidelines
  - `project-plan/` - Project architecture and constraints
  - `tasks.md` - Task tracking and status
  - `requirements.md` - Project requirements
  - `logs/` - Phase completion summaries
  - `tests/` - Unit tests and integration tests
  - `scripts/` - Bash scripts used to support context and development (NOT
  for direct implementaion as part of the application code base)

## Project Awareness & Context
- At the start of a new conversation, read files in `project-plan/` to review project's architecture, style, and constraints.
- At the start of a new conversation, read task.md to review project's architecture, style, and constraints.
- At the start of a new conversation, read `requirements.md`to review project's architecture, style, and constraints.
- At the start of a new conversation, review sessions log files in folder `logs` to understand project status and issues.

## Testing 
- **IMPORTANT: Always use the python-phase-tester agent (Task tool with subagent_type: "general-purpose") for implementing all phase tests.**
- Create a python virtual environment for testing using uv.
- Please perform all tests within this virtural environment.
- Create a folder call `tests` in submodule ctx-ai.
- All test codes should reside in the test folder.
- Do not write test results or update README.md after testing.
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.

## Logs
- Create a folder called `/logs` in the ctx-ai folder.
- When each phase is completed successfully, create a high level of the summary. 
- Log summary should be no more than 16 lines. 
- Summary should be concise and hight level overview.
- Each summary should have 1 heading only and several bullet points.
- Do not use icons in the log files.
- Do not mention next phase or previous phase in the summary.
- Save the summary file in this folder.
- A log summary should be created for each phase.
- The format of the log file should look like this phase_xx_yyyymmdd.md.
- The summary should also be datestamped and timestamped.
- If a phase has been reimplemented or updated, summarized the changes and
append the summary to the existing log file with datestamp and timestamp.

## Scripts 
- All shell cripts should be save to the ctx-ai git submodule in the folder call`scripts`.
- Do not save scripts in the root directory in the parent repository.  

## Documents 
- All documents should be save to the ctx-ai git submodule in the folder call`docs`.
- Documents such as installation guide and other instructions should be saved as
  markdown file within this folder.
- Do not save documents in the root directory in the parent repository.  

## General Principles:
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `task.md`.

## Implementation Guideline
- Focus exclusively on completing a single, well-defined feature before moving to the next.
* Definition of Done: A task or feature is completed is defined by the following:
- All tests are written and passing.
- The code is confirmed to work in the real target environment.
- Integration with the actual system is verified.
- Documentation has been updated
- **NO FEATURE CREEP**: Resist the urge to add "nice-to-have" functionalities until the current, core feature is 100% completed and verified.
- When you are adding a new feature such as a new method or function, stop to ask whether me permission to build feature.
- Please fully explain reason for the function as a comment

## 📦 Adding New Features - Standard Procedure
### Feature Development Pattern
* When adding any new feature to this project, follow this established pattern:

1. **Module Structure**
   - Create a new file in `src/` named after your feature (e.g., `email_lookup.py`, `data_validator.py`)
   - Define main struct and any result types needed
   - Implement core logic following existing patterns from `phone_lookup.py` 

2. **Independent Testing**
   - Create unit tests in `tests/test_your_feature_unit.py`

5. **Development Process**
   - Follow strict TDD: RED → GREEN → REFACTOR
   - Implement minimal code to pass test
   - Refactor only after tests pass
   - Each feature must be completely independent and self-contained
   - Ask for permission before adding new methods or functions to existing modules

## Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
- Never hardcode sensitive information - Always use .env files for API keys and configuration

### 📎 Modification Guideline
- When modifying code, always ... tbd 

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

