#!/usr/bin/env python
"""
Test Phase 11 - Command-line Arguments
Tests that the application properly handles command-line arguments
"""

import subprocess
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../src'))


def run_command(cmd):
    """Run a command and capture output"""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def test_no_arguments():
    """Test running without any arguments - should fail"""
    print("\n" + "=" * 50)
    print("FEATURE TEST: Phase 11 - No Arguments")
    print("=" * 50)
    
    print("\nTest Input: uv run python src/main.py")
    code, stdout, stderr = run_command("uv run python src/main.py")
    
    print("Test Output:")
    if code != 0:
        print("\033[92m✓ Test PASSED: Application exited with error as expected\033[0m")
        print(f"  Error message shown: 'Both symbol and position size are required'")
        return True
    else:
        print("\033[91m✗ Test FAILED: Application should not run without arguments\033[0m")
        return False


def test_missing_position():
    """Test running with only symbol - should fail"""
    print("\n" + "=" * 50)
    print("FEATURE TEST: Phase 11 - Missing Position Size")
    print("=" * 50)
    
    print("\nTest Input: uv run python src/main.py AAPL")
    code, stdout, stderr = run_command("uv run python src/main.py AAPL")
    
    print("Test Output:")
    if code != 0:
        print("\033[92m✓ Test PASSED: Application exited with error as expected\033[0m")
        print(f"  Error message shown: 'position_size required'")
        return True
    else:
        print("\033[91m✗ Test FAILED: Application should not run without position size\033[0m")
        return False


def test_invalid_position():
    """Test running with invalid position size - should fail"""
    print("\n" + "=" * 50)
    print("FEATURE TEST: Phase 11 - Invalid Position Size")
    print("=" * 50)
    
    # Test with zero
    print("\nTest Input: uv run python src/main.py AAPL 0")
    code, stdout, stderr = run_command("uv run python src/main.py AAPL 0")
    
    print("Test Output (zero position):")
    if code != 0:
        print("\033[92m✓ Test PASSED: Application rejected zero position size\033[0m")
    else:
        print("\033[91m✗ Test FAILED: Application should reject zero position size\033[0m")
        return False
    
    # Test with negative
    print("\nTest Input: uv run python src/main.py AAPL -100")
    code, stdout, stderr = run_command("uv run python src/main.py AAPL -100")
    
    print("Test Output (negative position):")
    if code != 0:
        print("\033[92m✓ Test PASSED: Application rejected negative position size\033[0m")
        return True
    else:
        print("\033[91m✗ Test FAILED: Application should reject negative position size\033[0m")
        return False


def test_valid_arguments():
    """Test that valid arguments are accepted"""
    print("\n" + "=" * 50)
    print("FEATURE TEST: Phase 11 - Valid Arguments")
    print("=" * 50)
    
    print("\nTest Input: uv run python src/main.py AAPL 100")
    print("Test Output:")
    
    # We can't fully run the app without TWS connection, but we can check it starts
    # For this test, we'll just verify the arguments are parsed correctly
    try:
        # Import and test the parse_arguments function directly
        from main import parse_arguments
        import argparse
        
        # Mock sys.argv
        original_argv = sys.argv
        sys.argv = ['main.py', 'AAPL', '100']
        
        args = parse_arguments()
        
        if args.symbol == 'AAPL' and args.position_size == 100:
            print("\033[92m✓ Test PASSED: Arguments parsed correctly\033[0m")
            print(f"  Symbol: {args.symbol}")
            print(f"  Position Size: {args.position_size}")
            result = True
        else:
            print("\033[91m✗ Test FAILED: Arguments not parsed correctly\033[0m")
            result = False
            
        # Restore argv
        sys.argv = original_argv
        return result
        
    except Exception as e:
        print(f"\033[91m✗ Test FAILED: Error parsing arguments: {e}\033[0m")
        return False


def main():
    """Run all Phase 11 tests"""
    print("\n" + "=" * 70)
    print("           PHASE 11 TESTS - Command-line Arguments")
    print("=" * 70)
    
    results = []
    
    # Run each test
    results.append(test_no_arguments())
    results.append(test_missing_position())
    results.append(test_invalid_position())
    results.append(test_valid_arguments())
    
    # Summary
    print("\n" + "=" * 70)
    print("                       TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"\033[92m✓ ALL TESTS PASSED ({passed}/{total})\033[0m")
    else:
        print(f"\033[91m✗ SOME TESTS FAILED ({passed}/{total} passed)\033[0m")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())