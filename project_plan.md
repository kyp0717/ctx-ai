# Project Plan

## AI Directive
1. Create comprehensive project plan (if not already exisit)
2. If project plan already exist, modify and update as work progress.
3. Modify and update tasks.md as needed as project progess.
4. Utilize sub agents for specific tasks
5. Run all tests in virtual environment using uv.
6. Summarized at a high level the work completed as a log file in the format specified.
7. When executing the test during the conversation: 
    - Display the heading with "FEATURE TEST: Phase xx - new_feature"
    - Display test input and test output 
    - If test fail, display failure in red in the console.
    - If test is successful, display success in green in the console.

## Goal
- Build a web scraper in python.
- Scraper will scrape a CT Judiciary civil inquiry site to get a list of court cases by town.
- Use the docket number to scrape the for the defendant name and address 
- Using the address, perform and http post request for phone numbers using the batchdata api.


## Phase 1 - Requirements
- Create a file in folder /prps/ call requirements.md
- In the requirements, explain what are the technical requirements that are needed for development of a scraper using python.
- For example, if selenium is required for this development, explain its purposes.
- In another section, list the python packages that are needed and why this is required.
- In another section, list the api and url that are used for scraping. In this section, include the tags that are used.
- Please feel free to add additional sections to explain anything else.
- When this phase is completed, log a summary of what has been done in phase and save with format phase_log_yyyymmdd.md
- Save the log file in `/log`.  If folder does not exist, create one.

## Phase 2 - Setup
- Setup configuration files such as `requirement.txt` and others as needed.

## Phase 3a - Open URL and extract HTML 
- Do not implement testing. Only write or modify code in this phase.
- Open the URL Connecticut Judicial site using the url provided in requirement.md.

## Phase 3b - Build Test and Run Test
- Build the test for Phase 3a.  Do not build another test except for phase 3a.
- Run the test in a virtual environment us uv.  Do not run any other test.  

## Phase 4 - Web Scraping  
### Feature Implementation
- CT Jucial URL: https://civilinquiry.jud.ct.gov/PropertyAddressSearch.aspx
- Scrape for cases by first performing a search by town on the search page which is the CT Jucial URL.
- Use the id tag "ctl00_ContentPlaceHolder1_txtCityTown" to input the town name.
- Use the Id tax "ctl00_ContentPlaceHolder1_btnSubmit" to submit the form after inputting town name.
- Return a list of court cases that include name of case, defendant name, address, docket number, and docket number url 
- Some cases may have multiple defendants.  Extract all defendants.
### Test Feature
- Test this implemenation by searching with 'Middletonw' as an example.
### Integration Implementation
- Integrate the feature created in this phase by creating a main.py file and using the classes and related code. 
### Test Integration
- Test the integration implemenation by searching with 'Middletonw' as an example.
## Phase 5 - Post Request to Sandbox Batch API
### Implementation
- Implement http post request to the following url:
- sandbox url - 'https://stoplight.io/mocks/batchdata/batchdata/20349728/property/skip-trace'
- Tokens for api access is provided in the file `../batchapi.csv`.  Please incorporate
- If the request is successful, return all phone numbers associated with this addresses.
### Test
- Buid test that can connect to sandbox api
- Use the test cases provided in the file `tests/batchapi_test_cases.json`.
- Run the test.  
### Integration Implementation
- Integrate the feature created in this phase by integrating with the main.py file and using the classes and related code. 
### Test Integration
- Test the main.py after integration.
- Use the test cases provided in the file `tests/batchapi_test_cases.json`.
- Run the test. 
## Phase 6 - Post Request to Prod Batch API
### Implementation
- Implement http post request to the following url:
- prod url - https://api.batchdata.com/api/v1/property/skip-trace
- Tokens for api access is provided in the file batchapi.csv.  Please incorporate
- If the request is successful, return all phone numbers associated with this addresses.
### Test
- Buid test that can connect to prod api
- Use the addresses from the first two items in the list derived from web scraping.
- Run the test.  
- When executing the test, display the input to the test and the output of test.
- Reminder.  Please use only 2 addresses for testing.  Do not use more than 2 addresses.
### Integration Implementation
- Integrate the feature created in this phase by integrating with the main.py file and using the classes and related code. 
### Test Integration
- Test the main.py after integration.
- When executing the test, display the input to the test and the output of test.
