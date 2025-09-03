#!/usr/bin/env python
"""
Phase 7 - Feature 1: Order Placement Test
Test script to verify order placement with user prompt
"""

import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from order_placement import OrderClient, OrderResult, interactive_order_prompt, place_order_with_prompt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_order_placement_prompt():
    """Test the interactive order placement with prompt"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 7 - Order Placement with Prompt")
    print("="*60)
    
    # Test parameters
    symbol = "AAPL"
    quantity = 1  # Small quantity for testing
    host = "127.0.0.1"
    port = 7500
    client_id = 30
    
    print(f"\nTest Input:")
    print(f"  Symbol: {symbol}")
    print(f"  Quantity: {quantity} share")
    print(f"  Order Type: MARKET")
    print(f"  Test Mode: Enabled (auto-confirms)")
    print("-"*40)
    
    try:
        # Create client
        print("\n1. Creating OrderClient instance...")
        client = OrderClient()
        print("   ✓ Instance created successfully")
        
        # Connect to TWS
        print(f"\n2. Connecting to TWS at {host}:{port}...")
        success = client.connect_to_tws(host, port, client_id)
        
        if not success:
            print("   ✗ Failed to connect to TWS")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Could not connect to TWS\033[0m")
            print("="*60)
            return False
            
        print("   ✓ Connected successfully")
        
        # Test interactive prompt in test mode
        print(f"\n3. Testing interactive order prompt for {symbol}...")
        print("   Running in test mode - will automatically select 'y'")
        
        result = interactive_order_prompt(symbol, client, quantity=quantity, test_mode=True)
        
        if result:
            print(f"\n4. Order Result:")
            print(f"   Order ID: {result.order_id}")
            print(f"   Symbol: {result.symbol}")
            print(f"   Action: {result.action}")
            print(f"   Quantity: {result.quantity}")
            print(f"   Type: {result.order_type}")
            print(f"   Status: {result.status}")
            
            # Wait for order to potentially fill
            print("\n5. Waiting for order status update (3 seconds)...")
            time.sleep(3)
            
            # Check final status
            if result.order_id in client.orders:
                final_result = client.orders[result.order_id]
                print(f"\n6. Final Order Status:")
                print(f"   Status: {final_result.status}")
                print(f"   Filled: {final_result.filled_qty}/{final_result.quantity}")
                if final_result.avg_fill_price > 0:
                    print(f"   Avg Fill Price: ${final_result.avg_fill_price:.2f}")
            
            # Disconnect
            print("\n7. Disconnecting from TWS...")
            client.disconnect_from_tws()
            print("   ✓ Disconnected successfully")
            
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: Order placed with prompt\033[0m")
            print("="*60)
            return True
        else:
            print("   ✗ Order placement failed or was cancelled")
            client.disconnect_from_tws()
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Order not placed\033[0m")
            print("="*60)
            return False
            
    except Exception as e:
        print("\n" + "="*60)
        print(f"\033[91mTEST FAILED: Unexpected error\033[0m")
        print(f"Error: {e}")
        print("="*60)
        if 'client' in locals() and client.is_connected():
            client.disconnect_from_tws()
        return False


def test_quote_refresh():
    """Test quote refresh when user selects 'n'"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 7 - Quote Refresh Test")
    print("="*60)
    
    symbol = "MSFT"
    
    print(f"\nTest Input:")
    print(f"  Symbol: {symbol}")
    print(f"  Testing quote refresh functionality")
    print("-"*40)
    
    try:
        # Create and connect client
        print("\n1. Setting up connection...")
        client = OrderClient()
        if not client.connect_to_tws(port=7500, client_id=31):
            print("   ✗ Failed to connect to TWS")
            return False
            
        print("   ✓ Connected to TWS")
        
        # Get initial quote
        print(f"\n2. Getting initial quote for {symbol}...")
        quote1 = client.get_stock_quote(symbol, timeout=3)
        
        if quote1 and quote1.is_valid():
            print(f"   ✓ Initial quote: ${quote1.last_price:.2f}")
            
            # Wait and get another quote
            print("\n3. Waiting 2 seconds and getting refreshed quote...")
            time.sleep(2)
            quote2 = client.get_stock_quote(symbol, timeout=3)
            
            if quote2 and quote2.is_valid():
                print(f"   ✓ Refreshed quote: ${quote2.last_price:.2f}")
                
                # Check if we got valid quotes
                if quote2.timestamp > quote1.timestamp:
                    print("   ✓ Timestamp updated correctly")
                    
                client.disconnect_from_tws()
                
                print("\n" + "="*60)
                print("\033[92mTEST SUCCESSFUL: Quote refresh works\033[0m")
                print("="*60)
                return True
            else:
                print("   ✗ Failed to get refreshed quote")
        else:
            print("   ✗ Failed to get initial quote")
            
        client.disconnect_from_tws()
        print("\n" + "="*60)
        print("\033[91mTEST FAILED: Quote refresh failed\033[0m")
        print("="*60)
        return False
        
    except Exception as e:
        print("\n" + "="*60)
        print(f"\033[91mTEST FAILED: Unexpected error\033[0m")
        print(f"Error: {e}")
        print("="*60)
        if 'client' in locals() and client.is_connected():
            client.disconnect_from_tws()
        return False


def test_convenience_function():
    """Test the convenience function for order placement"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 7 - Convenience Function Test")
    print("="*60)
    
    print("\nTest Input:")
    print("  Using place_order_with_prompt() convenience function")
    print("  Symbol: GOOGL")
    print("  Quantity: 1 share")
    print("-"*40)
    
    try:
        print("\n1. Testing convenience function...")
        print("   Running in test mode - will automatically confirm")
        
        result = place_order_with_prompt(
            symbol="GOOGL", 
            quantity=1, 
            client_id=32,
            test_mode=True
        )
        
        if result:
            print(f"\n2. Order placed successfully:")
            print(f"   {result}")
            
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: Convenience function works\033[0m")
            print("="*60)
            return True
        else:
            print("   ✗ Order placement failed")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Convenience function failed\033[0m")
            print("="*60)
            return False
            
    except Exception as e:
        print("\n" + "="*60)
        print(f"\033[91mTEST FAILED: Unexpected error\033[0m")
        print(f"Error: {e}")
        print("="*60)
        return False


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# Phase 7 - Feature 1: Order Placement Test Suite")
    print("#"*60)
    print("\nNOTE: This test will place REAL ORDERS in your paper trading account!")
    print("Make sure you are connected to a paper trading account.")
    
    # Run tests
    test_results = []
    
    # Test 1: Order placement with prompt
    result1 = test_order_placement_prompt()
    test_results.append(("Order Placement with Prompt", result1))
    
    # Small delay between tests
    time.sleep(2)
    
    # Test 2: Quote refresh
    result2 = test_quote_refresh()
    test_results.append(("Quote Refresh Test", result2))
    
    # Small delay between tests
    time.sleep(2)
    
    # Test 3: Convenience function
    result3 = test_convenience_function()
    test_results.append(("Convenience Function Test", result3))
    
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
        sys.exit(0)
    else:
        print("\n\033[91mSOME TESTS FAILED\033[0m")
        print("\nNote: If tests failed, ensure:")
        print("  - TWS/IB Gateway is running with paper trading account")
        print("  - API connections are enabled")
        print("  - You have permissions to place orders")
        print("  - Market is open (for market orders)")
        sys.exit(1)