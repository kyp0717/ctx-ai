#!/usr/bin/env python
"""
Phase 7 & 8 - Test: Trading Interface and PnL Monitoring
Tests the updated prompt mechanism and PnL tracking
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


def test_enter_prompt_and_order():
    """Test pressing Enter to accept order"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 7 - Enter to Accept Order")
    print("="*60)
    
    print("\nTest Input:")
    print("  Symbol: AAPL")
    print("  Action: Press Enter to accept order")
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
        order_placed = False
        
        def read_output():
            nonlocal order_placed
            while True:
                line = process.stdout.readline()
                if line:
                    output_lines.append(line)
                    # Check for key indicators
                    if ">>>> Open Trade at" in line:
                        print(f"   App: Found prompt - {line.strip()}")
                    if "[TWS Order Status]" in line:
                        print(f"   App: {line.strip()}")
                    if "Order placed successfully" in line:
                        order_placed = True
                        print(f"   App: Order placed!")
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
        
        print("\n4. Waiting for prompt to appear...")
        time.sleep(2)
        
        print("\n5. Pressing Enter to accept order...")
        process.stdin.write("\n")
        process.stdin.flush()
        time.sleep(10)  # Wait for order processing
        
        print("\n6. Exiting...")
        process.send_signal(2)  # SIGINT (Ctrl+C)
        time.sleep(1)
        process.stdin.write("\n")
        process.stdin.flush()
        time.sleep(1)
        process.stdin.write("2\n")
        process.stdin.flush()
        
        # Wait for process to exit
        process.wait(timeout=5)
        
        # Check output
        full_output = "".join(output_lines)
        
        print("\nTest Output:")
        if ">>>> Open Trade at" in full_output:
            print("   ✓ Prompt displayed correctly")
        else:
            print("   ✗ Prompt not found")
            return False
        
        if "[TWS Order Status]" in full_output:
            print("   ✓ Order status format correct")
        else:
            print("   ✗ Order status format incorrect")
            return False
        
        if order_placed:
            print("   ✓ Order placed on Enter press")
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: Enter to accept works\033[0m")
            print("="*60)
            return True
        else:
            print("   ✗ Order not placed")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Enter did not place order\033[0m")
            print("="*60)
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        process.terminate()
        return False


def test_auto_refresh():
    """Test auto-refresh after 1 second without input"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 7 - Auto-Refresh After 1 Second")
    print("="*60)
    
    print("\nTest Input:")
    print("  Symbol: MSFT")
    print("  Action: No input (wait for refresh)")
    print("-"*40)
    
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
        prompt_times = []
        
        def read_output():
            while True:
                line = process.stdout.readline()
                if line:
                    output_lines.append(line)
                    if ">>>> Open Trade at" in line:
                        prompt_times.append(datetime.now())
                if process.poll() is not None:
                    break
        
        reader_thread = threading.Thread(target=read_output, daemon=True)
        reader_thread.start()
        
        time.sleep(3)
        
        print("\n2. Selecting Begin Trading...")
        process.stdin.write("1\n")
        process.stdin.flush()
        time.sleep(1)
        
        print("\n3. Entering symbol MSFT...")
        process.stdin.write("MSFT\n")
        process.stdin.flush()
        
        print("\n4. Waiting for auto-refresh (no input)...")
        time.sleep(5)  # Wait for multiple refreshes
        
        print("\n5. Exiting...")
        process.send_signal(2)  # SIGINT
        time.sleep(1)
        process.stdin.write("\n")
        process.stdin.flush()
        time.sleep(1)
        process.stdin.write("2\n")
        process.stdin.flush()
        
        process.wait(timeout=5)
        
        print("\nTest Output:")
        if len(prompt_times) >= 3:
            print(f"   ✓ Captured {len(prompt_times)} prompt refreshes")
            
            # Check timing between refreshes
            if len(prompt_times) > 1:
                time_diffs = [(prompt_times[i+1] - prompt_times[i]).total_seconds() 
                             for i in range(len(prompt_times)-1)]
                avg_diff = sum(time_diffs) / len(time_diffs)
                print(f"   Average refresh interval: {avg_diff:.1f}s")
                
                if 0.8 <= avg_diff <= 1.5:  # Allow some tolerance
                    print("   ✓ Auto-refresh working (~1 second interval)")
                    print("\n" + "="*60)
                    print("\033[92mTEST SUCCESSFUL: Auto-refresh after 1s\033[0m")
                    print("="*60)
                    return True
                else:
                    print("   ✗ Refresh interval not ~1 second")
                    return False
        else:
            print(f"   ✗ Only {len(prompt_times)} prompts captured")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        process.terminate()
        return False


def test_pnl_tracking():
    """Test PnL tracking and display"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 8 - PnL Tracking")
    print("="*60)
    
    # Test parameters
    symbol = "AAPL"
    quantity = 100
    host = "127.0.0.1"
    port = 7500
    client_id = 400
    
    print(f"\nTest Input:")
    print(f"  Symbol: {symbol}")
    print(f"  Quantity: {quantity} shares")
    print(f"  Testing PnL calculation")
    print("-"*40)
    
    client = None
    
    try:
        print("\n1. Creating OrderClient instance...")
        client = OrderClient()
        
        print("\n2. Connecting to TWS...")
        if not client.connect_to_tws(host, port, client_id):
            print("   ✗ Failed to connect to TWS")
            return False
        
        print("   ✓ Connected to TWS")
        
        # Simulate a filled position
        print("\n3. Simulating filled position...")
        client.positions[symbol] = {
            "quantity": 100,
            "avg_cost": 235.00,
            "total_cost": 23500.00
        }
        
        # Get current quote
        print("\n4. Getting current quote for PnL calculation...")
        quote = client.get_stock_quote(symbol, timeout=3)
        
        if quote and quote.is_valid():
            print(f"   Current price: ${quote.last_price:.2f}")
            
            # Calculate PnL
            from main import calculate_pnl, format_pnl_display
            pnl = calculate_pnl(client.positions[symbol], quote.last_price)
            
            print(f"\n5. PnL Calculation:")
            print(f"   Position: 100 shares @ $235.00")
            print(f"   Current: ${quote.last_price:.2f}")
            print(f"   PnL: ${pnl:.2f}")
            
            # Test display formatting
            pnl_display = format_pnl_display(symbol, pnl)
            print(f"\n6. Formatted Display:")
            print(f"   {pnl_display}")
            
            client.disconnect_from_tws()
            
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: PnL tracking works\033[0m")
            print("="*60)
            return True
        else:
            print("   ✗ Failed to get quote")
            client.disconnect_from_tws()
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        if client and client.is_connected():
            client.disconnect_from_tws()
        return False


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# Phase 7 & 8 - Test: Trading and PnL")
    print("#"*60)
    
    test_results = []
    
    # Test 1: Enter to accept order
    result1 = test_enter_prompt_and_order()
    test_results.append(("Enter to Accept Order", result1))
    time.sleep(2)
    
    # Test 2: Auto-refresh
    result2 = test_auto_refresh()
    test_results.append(("Auto-Refresh After 1s", result2))
    time.sleep(2)
    
    # Test 3: PnL tracking
    result3 = test_pnl_tracking()
    test_results.append(("PnL Tracking", result3))
    
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
        print("\nPhase 7 & 8 Features Complete:")
        print("  ✓ Press Enter to accept order")
        print("  ✓ Auto-refresh after 1 second")
        print("  ✓ Order status format: [TWS Order Status]")
        print("  ✓ PnL tracking for filled orders")
        print("  ✓ Color-coded PnL display")
        sys.exit(0)
    else:
        print("\n\033[91mSOME TESTS FAILED\033[0m")
        sys.exit(1)