# Project Plan

## AI Directive
1. Create comprehensive project plan (if not already exisit)
2. If project plan already exist, modify and update as work progress.
3. Modify and update tasks.md as needed as project progress.
5. Run all tests in virtual environment using uv.
6. After completing each phase, summarize at a high level the work completed.  Log the summary in the format specified within the log folder.
7. When executing the test during the conversation: 
    - Display the heading with "FEATURE TEST: Phase xx - new_feature"
    - Display test input and test output 
    - If test fail, display failure in red in the console.
    - If test is successful, display success in green in the console.
8. Do not build project structure unless it is explicitly directed in this project plan.

## Goal
- Build a python app to trade stock using interactive broker trader workstation
- Use the python package ibapi which is published interactive broker. 
- Do not use third party package such as ib_async, ib_insync or ibridepy.


## Phase 1  
- Create a file call requirements.md.
- Store the requirement.md file in the folder `ctx-ai/ibxpy`.
- In the requirements, explain what are the technical requirements that are needed for development of trading app.
- In another section, list the python packages that are needed and why this is required.
- Please feel free to add additional sections to explain anything else.
- When this phase is completed, log a summary of what has been done in phase and save with format phase_log_yyyymmdd.md

## Phase 2 - Established connection to TWS (Trader Workstation)
### Feature
- Do not implement testing. Only write or modify code in this phase.
- Implement the connection to TWS on port 7500 on localhost.
### Test
- Build the test.  Do not build another test except for this phase.
- Run the test in a virtual environment us uv.  Do not run any other test.  

