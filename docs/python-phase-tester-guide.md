# Python Phase Tester Agent - Quick Reference Guide

## What is the Python Phase Tester Agent?
A specialized testing agent designed specifically for your TWS Trading Application that follows your phase-based development approach with strict TDD principles.

## Quick Start

### Basic Usage
To test any phase, simply ask:
- "Test Phase 6" 
- "Run tests for Phase 7 order placement"
- "Check if Phase 8 tests pass"

The agent will automatically:
1. Read your project plan and requirements
2. Create/update test files in `ctx-ai/tests/`
3. Run tests in your uv environment
4. Display colored results (✅ GREEN for pass, ❌ RED for fail)
5. Create logs in `ctx-ai/logs/`

## Phase Test Commands

### Individual Phase Testing
```
Phase 5: "Test TWS connection"
Phase 6: "Test stock quote retrieval"  
Phase 7: "Test order placement"
Phase 8: "Test position monitoring and PnL"
Phase 9: "Test audit functionality"
Phase 10: "Test trade exit"
Phase 11: "Test CLI arguments"
```

### Multiple Phase Testing
```
"Test Phases 5 through 8"
"Run all completed phase tests"
"Regression test everything"
```

## Test Output Format
Each test displays:
```
FEATURE TEST: Phase XX - Feature Name
Test Input: [actual data used]
Expected Output: [what should happen]
Actual Output: [what actually happened]
Status: ✅ PASSED or ❌ FAILED
```

## Requirements Before Testing

### For All Phases
- ✅ Virtual environment activated (`uv`)
- ✅ Dependencies installed

### For Phases 5-11
- ✅ TWS or IBGateway running
- ✅ API connections enabled (port 7500)
- ✅ Paper trading account active

### For Market Data Tests (Phase 6+)
- ✅ Run during market hours OR
- ✅ Enable delayed data in TWS

## Common Test Scenarios

### After Implementing New Feature
```
"I just finished Phase 7 order placement, please test it"
```

### Before Moving to Next Phase
```
"Verify Phase 8 is complete and working"
```

### After Making Changes
```
"Rerun Phase 6 tests to make sure nothing broke"
```

### Debugging Failures
```
"Phase 7 tests are failing, help me debug"
```

## Test File Locations
All test files are saved in:
```
ctx-ai/tests/
├── test_phase05_connection.py
├── test_phase06_quotes.py
├── test_phase07_orders.py
├── test_phase08_positions.py
├── test_phase09_audit.py
├── test_phase10_exit.py
└── test_phase11_cli.py
```

## Manual Test Execution
If you want to run tests manually:
```bash
# Test specific phase
uv run pytest ctx-ai/tests/test_phase06*.py -v

# Test with coverage
uv run pytest ctx-ai/tests/ --cov=src

# Test single function
uv run pytest ctx-ai/tests/test_phase07_orders.py::test_order_placement -v
```

## Understanding Test Results

### Success Indicators
- ✅ All assertions pass
- ✅ No exceptions raised
- ✅ Expected behavior matches actual
- ✅ Performance within limits

### Failure Types
- **AssertionError**: Expected vs actual mismatch
- **ConnectionError**: TWS not accessible
- **TimeoutError**: Operation took too long
- **ValueError**: Invalid input/configuration

## Best Practices

### When to Test
1. **After each feature implementation**
2. **Before marking phase complete**
3. **After fixing bugs**
4. **Before major refactoring**
5. **Daily during active development**

### Test Coverage Goals
- Unit Tests: 90% coverage
- Integration Tests: Core workflows
- Feature Tests: All user scenarios
- Edge Cases: Error conditions

## Troubleshooting

### TWS Connection Issues
```
Problem: Cannot connect to TWS
Fix: Check TWS is running, API enabled on port 7500
```

### Import Errors
```
Problem: ModuleNotFoundError: ibapi
Fix: Follow Phase 3 installation guide
```

### Test Timeouts
```
Problem: Tests hang or timeout
Fix: Check market hours, TWS responsiveness
```

## Phase Completion Criteria
A phase is ONLY complete when:
1. ✅ All tests written
2. ✅ All tests passing
3. ✅ Integration verified
4. ✅ No regression
5. ✅ Log created

## Getting Help
- Review test logs in `ctx-ai/logs/test_phase_*.md`
- Check error tracebacks for specific issues
- Verify requirements in `project_plan.md`
- Confirm environment setup in `requirements.md`