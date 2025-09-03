#!/usr/bin/env python
"""
Phase 7 - Test 2: Prompt and Order Placement Test
Tests the refactored interface with limit orders and order monitoring
"""

import sys
import time
import logging
import subprocess
import threading
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from order_placement import OrderClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_menu_refactoring():
    """Test that menu only shows 2 options"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 7 - Menu Refactoring")
    print("="*60)
    
    print("\nTest Input: Checking menu display")
    print("-"*40)
    
    print("\n1. Starting main.py application...")
    
    # Start main.py as subprocess
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
        
        def read_output():
            while True:
                line = process.stdout.readline()
                if line:
                    output_lines.append(line)
                if process.poll() is not None:
                    break
        
        # Start output reader thread
        reader_thread = threading.Thread(target=read_output, daemon=True)
        reader_thread.start()
        
        # Wait for app to start
        time.sleep(3)
        
        # Exit immediately to check menu
        print("2. Checking menu options...")
        process.stdin.write("2\n")
        process.stdin.flush()
        
        # Wait for process to exit
        process.wait(timeout=5)
        
        # Check output
        full_output = "".join(output_lines)
        
        # Verify menu options
        checks = {
            "Begin Trading": False,
            "Exit": False,
            "Continuous Quote Monitor": False  # Should NOT be present
        }
        
        for line in output_lines:
            if "Begin Trading" in line:
                checks["Begin Trading"] = True
            if "Exit" in line:
                checks["Exit"] = True
            if "Continuous Quote Monitor" in line:
                checks["Continuous Quote Monitor"] = True
        
        # Verify correct menu
        success = True
        print("\nTest Output:")
        if checks["Begin Trading"]:
            print("   ✓ 'Begin Trading' option present")
        else:
            print("   ✗ 'Begin Trading' option missing")
            success = False
            
        if checks["Exit"]:
            print("   ✓ 'Exit' option present")
        else:
            print("   ✗ 'Exit' option missing")
            success = False
            
        if not checks["Continuous Quote Monitor"]:
            print("   ✓ 'Continuous Quote Monitor' removed")
        else:
            print("   ✗ 'Continuous Quote Monitor' still present")
            success = False
        
        if success:
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: Menu refactored correctly\033[0m")
            print("="*60)
        else:
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Menu not properly refactored\033[0m")
            print("="*60)
            
        return success
        
    except subprocess.TimeoutExpired:
        print("   ⚠ Timeout - terminating")
        process.terminate()
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        process.terminate()
        return False


def test_limit_order_placement():
    """Test placing a limit order with monitoring"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 7 - Limit Order Placement")
    print("="*60)
    
    # Test parameters
    symbol = "AAPL"
    quantity = 100
    host = "127.0.0.1"
    port = 7500
    client_id = 300
    
    print(f"\nTest Input:")
    print(f"  Symbol: {symbol}")
    print(f"  Quantity: {quantity} shares")
    print(f"  Order Type: LIMIT")
    print(f"  Action: BUY")
    print("-"*40)
    
    client = None
    
    try:
        print("\n1. Creating OrderClient instance...")
        client = OrderClient()
        print("   ✓ Instance created successfully")
        
        print(f"\n2. Connecting to TWS at {host}:{port}...")
        if not client.connect_to_tws(host, port, client_id):
            print("   ✗ Failed to connect to TWS")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Could not connect to TWS\033[0m")
            print("="*60)
            return False
            
        print("   ✓ Connected to TWS")
        print(f"   Next Order ID: {client.next_order_id}")
        
        # Get current quote
        print(f"\n3. Getting current quote for {symbol}...")
        quote = client.get_stock_quote(symbol, timeout=5)
        
        if not quote or not quote.is_valid():
            print("   ✗ Failed to get quote")
            client.disconnect_from_tws()
            return False
            
        print(f"   ✓ Current price: ${quote.last_price:.2f}")
        print(f"   Ask price: ${quote.ask_price:.2f}")
        
        # Simulate user selecting 'y' to place order
        print(f"\n4. Simulating order placement at ${quote.ask_price:.2f}...")
        print(f"   User response: 'y' (placing order)")
        
        # Place limit order
        result = client.place_limit_order(symbol, "BUY", quantity, quote.ask_price)
        
        if result:
            print(f"\n5. Order placed successfully!")
            print(f"   Order ID: {result.order_id}")
            print(f"   Symbol: {result.symbol}")
            print(f"   Action: {result.action}")
            print(f"   Quantity: {result.quantity}")
            print(f"   Type: LIMIT @ ${result.limit_price:.2f}")
            print(f"   Status: {result.status}")
            
            # Monitor order status for a few seconds
            print("\n6. Monitoring order status...")
            start_time = time.time()
            max_wait = 10  # Wait max 10 seconds
            
            while time.time() - start_time < max_wait:
                if result.order_id in client.orders:
                    result = client.orders[result.order_id]
                    
                    status_line = f"   Status: {result.status}"
                    
                    if result.filled_qty > 0:
                        pct_filled = (result.filled_qty / result.quantity) * 100
                        status_line += f" - {result.filled_qty}/{result.quantity} shares filled ({pct_filled:.0f}%)"
                        if result.avg_fill_price > 0:
                            status_line += f" @ ${result.avg_fill_price:.2f}"
                    
                    print(status_line)
                    
                    if result.is_filled():
                        print(f"\n   ✓ Order completely filled!")
                        print(f"   Total: ${result.quantity * result.avg_fill_price:,.2f}")
                        break
                    elif result.status == "CANCELLED":
                        print("\n   ⚠ Order cancelled")
                        break
                
                time.sleep(1)
            
            # Disconnect
            client.disconnect_from_tws()
            
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: Limit order placed and monitored\033[0m")
            print("="*60)
            return True
        else:
            print("   ✗ Failed to place order")
            client.disconnect_from_tws()
            return False
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        if client and client.is_connected():
            client.disconnect_from_tws()
        return False


def test_immediate_quote_refresh():
    """Test immediate quote refresh on 'n' press"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 7 - Immediate Quote Refresh")
    print("="*60)
    
    print("\nTest Input: Testing 'n' for immediate refresh")
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
        timestamps = []
        
        def read_output():
            while True:
                line = process.stdout.readline()
                if line:
                    output_lines.append(line)
                    # Capture timestamps when quote is displayed
                    if "Time:" in line:
                        timestamps.append(datetime.now())
                if process.poll() is not None:
                    break
        
        reader_thread = threading.Thread(target=read_output, daemon=True)
        reader_thread.start()
        
        # Wait for startup
        time.sleep(3)
        
        print("2. Selecting Begin Trading...")
        process.stdin.write("1\n")
        process.stdin.flush()
        time.sleep(1)
        
        print("3. Entering symbol AAPL...")
        process.stdin.write("AAPL\n")
        process.stdin.flush()
        time.sleep(3)
        
        print("4. Pressing 'n' to refresh immediately...")
        # Press 'n' multiple times quickly
        for i in range(3):
            process.stdin.write("n")
            process.stdin.flush()
            time.sleep(0.5)  # Very short delay
        
        print("5. Exiting...")
        process.send_signal(2)  # SIGINT (Ctrl+C)
        time.sleep(1)
        process.stdin.write("\n")
        process.stdin.flush()
        time.sleep(1)
        process.stdin.write("2\n")
        process.stdin.flush()
        
        process.wait(timeout=5)
        
        # Check that multiple timestamps were captured quickly
        print("\nTest Output:")
        if len(timestamps) >= 3:
            print(f"   ✓ Captured {len(timestamps)} quote refreshes")
            
            # Check time between refreshes
            if len(timestamps) > 1:
                time_diffs = [(timestamps[i+1] - timestamps[i]).total_seconds() 
                             for i in range(len(timestamps)-1)]
                avg_diff = sum(time_diffs) / len(time_diffs)
                print(f"   Average time between refreshes: {avg_diff:.2f}s")
                
                if avg_diff < 2:  # Should be much less than the 5-second auto-refresh
                    print("   ✓ Immediate refresh working (< 2s between refreshes)")
                    print("\n" + "="*60)
                    print("\033[92mTEST SUCCESSFUL: Immediate refresh on 'n'\033[0m")
                    print("="*60)
                    return True
                else:
                    print("   ✗ Refresh not immediate enough")
                    print("\n" + "="*60)
                    print("\033[91mTEST FAILED: Refresh delay too high\033[0m")
                    print("="*60)
                    return False
        else:
            print(f"   ✗ Only {len(timestamps)} quotes captured")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Insufficient quote refreshes\033[0m")
            print("="*60)
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        process.terminate()
        return False


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# Phase 7 - Test 2: Prompt and Order Placement")
    print("#"*60)
    print("\nNOTE: This test will place REAL LIMIT ORDERS in paper trading")
    
    test_results = []
    
    # Test 1: Menu refactoring
    result1 = test_menu_refactoring()
    test_results.append(("Menu Refactoring", result1))
    time.sleep(2)
    
    # Test 2: Limit order placement
    result2 = test_limit_order_placement()
    test_results.append(("Limit Order Placement", result2))
    time.sleep(2)
    
    # Test 3: Immediate quote refresh
    result3 = test_immediate_quote_refresh()
    test_results.append(("Immediate Quote Refresh", result3))
    
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
        print("\nPhase 7 Features Complete:")
        print("  ✓ Menu simplified to 2 options")
        print("  ✓ Limit orders implemented")
        print("  ✓ Order status monitoring added")
        print("  ✓ Immediate quote refresh on 'n'")
        sys.exit(0)
    else:
        print("\n\033[91mSOME TESTS FAILED\033[0m")
        sys.exit(1)