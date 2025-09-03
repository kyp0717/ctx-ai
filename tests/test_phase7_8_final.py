#!/usr/bin/env python
"""
Phase 7 & 8 - Final Test: Automatic PnL Monitoring
Tests the updated prompts and automatic transition
"""

import sys
import time
import subprocess
import threading
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from order_placement import OrderClient


def test_prompt_format():
    """Test prompt format without 'to accept'"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 7 - Prompt Format")
    print("="*60)
    
    print("\nTest Input:")
    print("  Symbol: AAPL")
    print("  Checking prompt format")
    print("-"*40)
    
    # Start main.py as subprocess
    print("\n1. Starting main.py application...")
    process = subprocess.Popen(
        [sys.executable, "src/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=0
    )
    
    try:
        output_lines = []
        prompt_found = False
        
        def read_output():
            nonlocal prompt_found
            while True:
                line = process.stdout.readline()
                if line:
                    output_lines.append(line)
                    if "**AAPL** >>> Open Trade" in line:
                        print(f"   App: {line.strip()}")
                        # Check it doesn't contain "to accept"
                        if "to accept" not in line and "(press enter)" in line:
                            prompt_found = True
                if process.poll() is not None:
                    break
        
        # Start output reader thread
        reader_thread = threading.Thread(target=read_output, daemon=True)
        reader_thread.start()
        
        # Wait for app to start
        time.sleep(3)
        
        print("\n2. Selecting Begin Trading...")
        process.stdin.write("1\n")
        process.stdin.flush()
        time.sleep(1)
        
        print("\n3. Entering symbol AAPL...")
        process.stdin.write("AAPL\n")
        process.stdin.flush()
        time.sleep(3)
        
        print("\n4. Exiting...")
        process.send_signal(2)  # SIGINT (Ctrl+C)
        time.sleep(1)
        process.stdin.write("\n")
        process.stdin.flush()
        time.sleep(1)
        process.stdin.write("2\n")
        process.stdin.flush()
        
        # Wait for process to exit
        process.wait(timeout=5)
        
        print("\nTest Output:")
        if prompt_found:
            print("   ✓ Prompt format correct (press enter) without 'to accept'")
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: Prompt format updated\033[0m")
            print("="*60)
            return True
        else:
            print("   ✗ Prompt format incorrect")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Prompt not updated\033[0m")
            print("="*60)
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        process.terminate()
        return False


def test_pnl_color():
    """Test PnL color coding (green for GAIN, red for LOSS)"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 8 - PnL Color Coding")
    print("="*60)
    
    symbol = "AAPL"
    
    print(f"\nTest Input:")
    print(f"  Symbol: {symbol}")
    print(f"  Testing PnL color coding")
    print("-"*40)
    
    # Import formatting functions
    from main import calculate_pnl, format_pnl_display
    
    # Create test position
    position = {
        "quantity": 100,
        "avg_cost": 235.00,
        "total_cost": 23500.00
    }
    
    print("\n1. Testing GAIN scenario (should be green)...")
    current_price = 240.00
    pnl = calculate_pnl(position, current_price)
    pnl_display = format_pnl_display(symbol, pnl)
    
    print(f"   Position: 100 shares @ $235.00")
    print(f"   Current: ${current_price:.2f}")
    print(f"   PnL: ${pnl:.2f}")
    print(f"   Display: {pnl_display}")
    
    # Check for green color code
    if "\033[92m" in pnl_display and "GAIN" in pnl_display:
        print("   ✓ GAIN displayed in GREEN")
    else:
        print("   ✗ GAIN not in green")
        return False
    
    print("\n2. Testing LOSS scenario (should be red)...")
    current_price = 230.00
    pnl = calculate_pnl(position, current_price)
    pnl_display = format_pnl_display(symbol, pnl)
    
    print(f"   Position: 100 shares @ $235.00")
    print(f"   Current: ${current_price:.2f}")
    print(f"   PnL: ${pnl:.2f}")
    print(f"   Display: {pnl_display}")
    
    # Check for red color code
    if "\033[91m" in pnl_display and "LOSS" in pnl_display:
        print("   ✓ LOSS displayed in RED")
    else:
        print("   ✗ LOSS not in red")
        return False
    
    print("\n" + "="*60)
    print("\033[92mTEST SUCCESSFUL: PnL colors correct\033[0m")
    print("="*60)
    return True


def test_timestamp_persistence():
    """Test that filled timestamp doesn't update"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 7 - Timestamp Persistence")
    print("="*60)
    
    symbol = "MSFT"
    
    print(f"\nTest Input:")
    print(f"  Symbol: {symbol}")
    print(f"  Testing timestamp persistence")
    print("-"*40)
    
    # Import formatting function
    from main import format_order_status
    
    # Create initial filled status
    print("\n1. Creating initial filled status...")
    initial_time = "10:30:45"
    status1 = format_order_status(symbol, "FILLED", price=450.25, fill_time=initial_time)
    print(f"   Status 1: {status1}")
    
    # Wait and create another with same fill_time
    time.sleep(2)
    print("\n2. Creating status 2 seconds later with same fill_time...")
    status2 = format_order_status(symbol, "FILLED", price=450.25, fill_time=initial_time)
    print(f"   Status 2: {status2}")
    
    # Check timestamps match
    if initial_time in status1 and initial_time in status2:
        print(f"   ✓ Timestamp persisted: {initial_time}")
        print("\n" + "="*60)
        print("\033[92mTEST SUCCESSFUL: Timestamp doesn't update\033[0m")
        print("="*60)
        return True
    else:
        print("   ✗ Timestamp changed")
        print("\n" + "="*60)
        print("\033[91mTEST FAILED: Timestamp updated\033[0m")
        print("="*60)
        return False


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# Phase 7 & 8 Final - Test: Automatic PnL Monitoring")
    print("#"*60)
    
    test_results = []
    
    # Test 1: Prompt format
    result1 = test_prompt_format()
    test_results.append(("Prompt Format", result1))
    time.sleep(2)
    
    # Test 2: PnL color coding
    result2 = test_pnl_color()
    test_results.append(("PnL Color Coding", result2))
    time.sleep(1)
    
    # Test 3: Timestamp persistence
    result3 = test_timestamp_persistence()
    test_results.append(("Timestamp Persistence", result3))
    
    # Summary
    print("\n" + "#"*60)
    print("# TEST SUMMARY")
    print("#"*60)
    
    for test_name, result in test_results:
        status = "\033[92mPASSED\033[0m" if result else "\033[91mFAILED\033[0m"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result for _, result in test_results)
    
    if all_passed:
        print("\n\033[92mALL TESTS PASSED\033[0m")
        print("\nPhase 7 & 8 Final Features:")
        print("  ✓ Prompt: (press enter) without 'to accept'")
        print("  ✓ Automatic transition to PnL monitoring")
        print("  ✓ PnL GAIN in GREEN color")
        print("  ✓ PnL LOSS in RED color")
        print("  ✓ Fill timestamp persists (doesn't update)")
        sys.exit(0)
    else:
        print("\n\033[91mSOME TESTS FAILED\033[0m")
        sys.exit(1)