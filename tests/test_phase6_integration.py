#!/usr/bin/env python
"""
Phase 6 - Test 2: Integration Test
Runs main.py as a subprocess and tests the integrated stock quote functionality
Connects to TWS as a client and retrieves stock quotes
"""

import sys
import time
import subprocess
import threading
from pathlib import Path
import signal
import os

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from stock_quote import QuoteClient


def test_main_app_connection():
    """Test that main.py can connect to TWS"""
    
    print("\n" + "="*60)
    print("INTEGRATION TEST: Main App Connection")
    print("="*60)
    
    print("\n1. Starting main.py application...")
    
    # Start main.py as subprocess with input simulation
    process = subprocess.Popen(
        [sys.executable, "src/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Give app time to start and connect
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("   ✓ Main app started successfully")
            
            # Send menu choice "4" to exit gracefully
            process.stdin.write("4\n")
            process.stdin.flush()
            
            # Wait for graceful exit
            process.wait(timeout=5)
            
            # Read output
            stdout, stderr = process.communicate(timeout=1)
            
            if "Successfully connected to TWS!" in stdout:
                print("   ✓ Main app connected to TWS successfully")
                print("\n✅ Connection test passed")
                return True
            else:
                print("   ✗ Main app failed to connect to TWS")
                print(f"Output: {stdout[:500]}")
                return False
        else:
            stdout, stderr = process.communicate()
            print("   ✗ Main app exited unexpectedly")
            print(f"Output: {stdout[:500]}")
            if stderr:
                print(f"Errors: {stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ⚠ Main app timeout - terminating")
        process.terminate()
        return False
    except Exception as e:
        print(f"   ✗ Error running main app: {e}")
        process.terminate()
        return False


def test_main_app_quote_retrieval():
    """Test that main.py can retrieve quotes through menu option 1"""
    
    print("\n" + "="*60)
    print("INTEGRATION TEST: Quote Retrieval via Main App")
    print("="*60)
    
    print("\n1. Starting main.py application...")
    
    # Start main.py as subprocess
    process = subprocess.Popen(
        [sys.executable, "src/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=0  # Unbuffered for real-time interaction
    )
    
    try:
        # Function to read output in background
        output_lines = []
        
        def read_output():
            while True:
                line = process.stdout.readline()
                if line:
                    output_lines.append(line)
                    if "Enter your choice" in line or "Enter stock symbol" in line:
                        print(f"   App prompt: {line.strip()}")
                if process.poll() is not None:
                    break
        
        # Start output reader thread
        reader_thread = threading.Thread(target=read_output, daemon=True)
        reader_thread.start()
        
        # Wait for app to start
        time.sleep(3)
        
        print("\n2. Selecting menu option 1 (Get Stock Quote)...")
        process.stdin.write("1\n")
        process.stdin.flush()
        time.sleep(1)
        
        print("\n3. Entering symbol AAPL...")
        process.stdin.write("AAPL\n")
        process.stdin.flush()
        time.sleep(5)  # Wait for quote retrieval
        
        print("\n4. Pressing Enter to continue...")
        process.stdin.write("\n")
        process.stdin.flush()
        time.sleep(1)
        
        print("\n5. Selecting menu option 4 (Exit)...")
        process.stdin.write("4\n")
        process.stdin.flush()
        
        # Wait for process to exit
        process.wait(timeout=5)
        
        # Check output for quote data
        full_output = "".join(output_lines)
        
        if "AAPL Quote:" in full_output and "Last Price: $" in full_output:
            print("   ✓ Successfully retrieved AAPL quote via main app")
            
            # Extract price if possible
            for line in output_lines:
                if "Last Price: $" in line:
                    print(f"   Retrieved: {line.strip()}")
                    break
            
            print("\n✅ Quote retrieval test passed")
            return True
        else:
            print("   ✗ Failed to retrieve quote via main app")
            print(f"Output excerpt: {full_output[:1000]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ⚠ Main app timeout - terminating")
        process.terminate()
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        process.terminate()
        return False


def test_concurrent_client_access():
    """Test that a separate client can connect while main.py is running"""
    
    print("\n" + "="*60)
    print("INTEGRATION TEST: Concurrent Client Access")
    print("="*60)
    
    print("\n1. Starting main.py application...")
    
    # Start main.py
    process = subprocess.Popen(
        [sys.executable, "src/main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Give main.py time to connect
        time.sleep(3)
        
        if process.poll() is None:
            print("   ✓ Main app running")
            
            # Now create a separate client connection
            print("\n2. Creating separate QuoteClient connection...")
            client = QuoteClient()
            
            # Use different client ID to avoid conflicts
            success = client.connect_to_tws(port=7500, client_id=220)
            
            if success:
                print("   ✓ Separate client connected successfully")
                
                # Try to get a quote
                print("\n3. Retrieving MSFT quote via separate client...")
                quote = client.get_stock_quote("MSFT", timeout=5)
                
                if quote and quote.is_valid():
                    print(f"   ✓ Retrieved MSFT quote: ${quote.last_price:.2f}")
                    
                    # Disconnect our client
                    client.disconnect_from_tws()
                    
                    # Exit main app
                    process.stdin.write("4\n")
                    process.stdin.flush()
                    process.wait(timeout=5)
                    
                    print("\n✅ Concurrent access test passed")
                    return True
                else:
                    print("   ✗ Failed to retrieve quote")
                    client.disconnect_from_tws()
            else:
                print("   ✗ Failed to connect separate client")
            
            # Clean up main app
            process.stdin.write("4\n")
            process.stdin.flush()
            process.wait(timeout=5)
            
        return False
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        process.terminate()
        if 'client' in locals() and client.is_connected():
            client.disconnect_from_tws()
        return False


def test_main_app_multiple_quotes():
    """Test retrieving multiple quotes through main.py menu option 2"""
    
    print("\n" + "="*60)
    print("INTEGRATION TEST: Multiple Quotes via Main App")
    print("="*60)
    
    print("\n1. Starting main.py application...")
    
    # Start main.py
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
        
        reader_thread = threading.Thread(target=read_output, daemon=True)
        reader_thread.start()
        
        # Wait for startup
        time.sleep(3)
        
        print("\n2. Selecting menu option 2 (Get Multiple Quotes)...")
        process.stdin.write("2\n")
        process.stdin.flush()
        time.sleep(1)
        
        print("\n3. Entering symbols: AAPL,GOOGL,MSFT...")
        process.stdin.write("AAPL,GOOGL,MSFT\n")
        process.stdin.flush()
        time.sleep(8)  # Wait for all quotes
        
        print("\n4. Pressing Enter to continue...")
        process.stdin.write("\n")
        process.stdin.flush()
        time.sleep(1)
        
        print("\n5. Exiting application...")
        process.stdin.write("4\n")
        process.stdin.flush()
        
        process.wait(timeout=5)
        
        # Check output
        full_output = "".join(output_lines)
        
        symbols_found = 0
        for symbol in ["AAPL", "GOOGL", "MSFT"]:
            if symbol in full_output and "Last:" in full_output:
                symbols_found += 1
                print(f"   ✓ Found quote for {symbol}")
        
        if symbols_found >= 2:  # At least 2 out of 3
            print(f"\n✅ Multiple quotes test passed ({symbols_found}/3 symbols)")
            return True
        else:
            print(f"\n✗ Multiple quotes test failed ({symbols_found}/3 symbols)")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        process.terminate()
        return False


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# Phase 6 - Test 2: Integration Test")
    print("# Testing main.py with real TWS connection")
    print("#"*60)
    
    print("\nNOTE: This test requires TWS to be running on port 7500")
    print("The test will run main.py and interact with it programmatically")
    
    test_results = []
    
    # Test 1: Connection test
    result1 = test_main_app_connection()
    test_results.append(("Main App Connection", result1))
    time.sleep(2)
    
    # Test 2: Quote retrieval
    result2 = test_main_app_quote_retrieval()
    test_results.append(("Quote Retrieval via Menu", result2))
    time.sleep(2)
    
    # Test 3: Concurrent access
    result3 = test_concurrent_client_access()
    test_results.append(("Concurrent Client Access", result3))
    time.sleep(2)
    
    # Test 4: Multiple quotes
    result4 = test_main_app_multiple_quotes()
    test_results.append(("Multiple Quotes via Menu", result4))
    
    # Summary
    print("\n" + "#"*60)
    print("# INTEGRATION TEST SUMMARY")
    print("#"*60)
    
    for test_name, result in test_results:
        status = "\033[92mPASSED\033[0m" if result else "\033[91mFAILED\033[0m"
        print(f"  {test_name}: {status}")
    
    all_passed = all(result for _, result in test_results)
    
    if all_passed:
        print("\n\033[92mALL INTEGRATION TESTS PASSED\033[0m")
        sys.exit(0)
    else:
        print("\n\033[91mSOME INTEGRATION TESTS FAILED\033[0m")
        sys.exit(1)