# Project Tasks

## Status Legend
- ✅ Completed
- 🔄 In Progress
- ⏳ Pending
- ❌ Blocked

## Re-implementation (2025-08-28)

### Updated Project Plan Implementation
- ✅ Phase 4 Feature Test: Updated `tests/test_case_scraper.py` with colored output (green/red) and proper test format
- ✅ Phase 4 Integration: Created `main.py` with case scraping integration
- ✅ Phase 4 Integration Test: Created `tests/test_phase4_integration.py` with proper test format
- ✅ Phase 5 Integration: Updated `main.py` to integrate sandbox batch API with --skip-trace flag
- ✅ Phase 5 Integration Test: Created `tests/test_phase5_integration.py`
- ✅ Phase 6 Implementation: Updated `main.py` to support production API with --prod flag
- ✅ Phase 6 Test: Created `tests/test_phase6_prod_api.py` for production API testing
- ✅ Phase 6 Integration Test: Created `tests/test_phase6_integration.py`

## Re-implementation (2025-08-27)

### Phase 1 - Requirements
- ✅ Reviewed `GEMINI.md` and `project_plan.md`.
- ✅ No changes needed for `requirements.md`.

### Phase 2 - Setup
- ✅ No changes needed for `requirements.txt`.

### Phase 3 - Site Connection
- ✅ **3a:** No changes needed for `src/site_connector.py`.
- ✅ **3b:** Created `tests/test_site_connector.py` and test passed.

### Phase 4 - Case Scraper
- ✅ **4a:** Modified `src/case_scraper.py` to extract docket number URL.
- ✅ **4b:** Created `tests/test_case_scraper.py` and test passed.

### Phase 5 - Batch API
- ✅ **5a:** Modified `src/batch_api_connector.py` to return phone numbers.
- ✅ **5b:** Modified `tests/test_batch_api_connector.py` to validate the phone numbers and test passed.


## Initial Implementation

## Phase 1 - Requirements
- ✅ Create `prps/requirements.md`.
- ✅ Create `/logs` directory.
- ✅ Create `logs/phase_log_20250826.md`.

## Phase 2 - Setup
- ✅ Build the `requirements.txt` for python development.
- ✅ Setup any other configuration file as needed.

## Phase 3a - Implement site connection
- ✅ Do not implement testing. Only write or modify code in this phase.


## Phase 3b - Testing
- ✅ Test site connection

## Phase 4a - Implement scraping for docket number by town
- ✅ Web scrape for case docket number from Connecticut Judicial Site

## Phase 5a - Post Request to Sandbox Batch API
- ✅ Implement http post request to the following url:
- sandbox url - 'https://stoplight.io/mocks/batchdata/batchdata/20349728/property/skip-trace'
- ✅ Tokens for api access is provided in the file batchapi.csv.  Please incorporate

## Phase 5b - Test Sandbox Batch API Http Request 
- ✅ Buid test that can connect to sandbox api
- ✅ Use the test cases provided in the file `tests/batchapi_test_cases.json`.
- ✅ Run the test.  
- ✅ When executing the test, display the input to the test and the output of test.