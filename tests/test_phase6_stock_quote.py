#!/usr/bin/env python
"""
Phase 6 - Feature 1: Stock Quote Test
Test script to verify retrieval of real-time stock quotes
"""

import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from stock_quote import QuoteClient, StockQuote, get_stock_quote

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_aapl_quote():
    """Test retrieving real-time quote for AAPL stock"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 6 - Get Stock Quote for AAPL")
    print("="*60)
    
    # Test parameters
    symbol = "AAPL"
    host = "127.0.0.1"
    port = 7500
    client_id = 10  # Using different ID to avoid conflicts
    
    print(f"\nTest Input:")
    print(f"  Symbol: {symbol}")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Client ID: {client_id}")
    print("-"*40)
    
    try:
        # Create QuoteClient instance
        print("\n1. Creating QuoteClient instance...")
        client = QuoteClient()
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
        
        # Request quote for AAPL
        print(f"\n3. Requesting quote for {symbol}...")
        print("   Waiting for market data (up to 5 seconds)...")
        
        quote = client.get_stock_quote(symbol, timeout=5.0)
        
        if quote and quote.is_valid():
            print(f"   ✓ Quote received successfully!")
            
            print("\n4. Quote Details:")
            print(f"   Symbol: {quote.symbol}")
            print(f"   Last Price: ${quote.last_price:.2f}")
            print(f"   Bid Price: ${quote.bid_price:.2f}")
            print(f"   Ask Price: ${quote.ask_price:.2f}")
            print(f"   Bid Size: {quote.bid_size}")
            print(f"   Ask Size: {quote.ask_size}")
            print(f"   Volume: {quote.volume:,}")
            print(f"   High: ${quote.high:.2f}")
            print(f"   Low: ${quote.low:.2f}")
            print(f"   Close: ${quote.close:.2f}")
            print(f"   Timestamp: {quote.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Verify we have meaningful data
            if quote.last_price > 0 or (quote.bid_price > 0 and quote.ask_price > 0):
                print("\n5. Data Validation:")
                print("   ✓ Quote contains valid price data")
                
                # Disconnect
                print("\n6. Disconnecting from TWS...")
                client.disconnect_from_tws()
                print("   ✓ Disconnected successfully")
                
                print("\n" + "="*60)
                print("\033[92mTEST SUCCESSFUL: Retrieved quote for AAPL\033[0m")
                print("="*60)
                return True
            else:
                print("\n" + "="*60)
                print("\033[91mTEST FAILED: Quote has no valid price data\033[0m")
                print("="*60)
                client.disconnect_from_tws()
                return False
        else:
            print("   ✗ Failed to retrieve quote")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Could not retrieve quote for AAPL\033[0m")
            print("Possible reasons:")
            print("  1. Market is closed (quotes may be delayed)")
            print("  2. No market data subscription for AAPL")
            print("  3. Network or connectivity issues")
            print("="*60)
            client.disconnect_from_tws()
            return False
            
    except ImportError as e:
        print("\n" + "="*60)
        print("\033[91mTEST FAILED: Import Error\033[0m")
        print(f"Error: {e}")
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
    """Test the get_stock_quote convenience function"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 6 - Convenience Function Test")
    print("="*60)
    
    symbol = "MSFT"
    
    print(f"\nTest Input:")
    print(f"  Using get_stock_quote() convenience function")
    print(f"  Symbol: {symbol}")
    print("-"*40)
    
    try:
        print(f"\n1. Testing get_stock_quote() for {symbol}...")
        
        # Create a QuoteClient connection first
        client = QuoteClient()
        if not client.connect_to_tws(port=7500, client_id=11):
            print("   ✗ Failed to connect to TWS")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Could not connect to TWS\033[0m")
            print("="*60)
            return False
            
        # Use the convenience function with existing connection
        quote = get_stock_quote(symbol, connection=client)
        
        if quote and quote.is_valid():
            print(f"   ✓ Quote retrieved: {quote}")
            
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: Convenience function works\033[0m")
            print("="*60)
            client.disconnect_from_tws()
            return True
        else:
            print(f"   ✗ Failed to retrieve quote for {symbol}")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: No quote retrieved\033[0m")
            print("="*60)
            client.disconnect_from_tws()
            return False
            
    except Exception as e:
        print("\n" + "="*60)
        print(f"\033[91mTEST FAILED: Unexpected error\033[0m")
        print(f"Error: {e}")
        print("="*60)
        if 'client' in locals() and client.is_connected():
            client.disconnect_from_tws()
        return False


def test_multiple_quotes():
    """Test retrieving quotes for multiple stocks"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 6 - Multiple Stock Quotes")
    print("="*60)
    
    symbols = ["AAPL", "GOOGL", "TSLA"]
    
    print(f"\nTest Input:")
    print(f"  Symbols: {', '.join(symbols)}")
    print("-"*40)
    
    try:
        # Create and connect client
        print("\n1. Setting up connection...")
        client = QuoteClient()
        if not client.connect_to_tws(port=7500, client_id=12):
            print("   ✗ Failed to connect to TWS")
            return False
            
        print("   ✓ Connected to TWS")
        
        # Get quotes for each symbol
        print("\n2. Retrieving quotes for multiple symbols...")
        results = []
        
        for symbol in symbols:
            print(f"\n   Requesting {symbol}...")
            quote = client.get_stock_quote(symbol, timeout=3.0)
            
            if quote and quote.is_valid():
                print(f"   ✓ {quote}")
                results.append((symbol, True))
            else:
                print(f"   ✗ Failed to get quote for {symbol}")
                results.append((symbol, False))
                
            # Small delay between requests
            time.sleep(0.5)
        
        # Disconnect
        client.disconnect_from_tws()
        
        # Check results
        success_count = sum(1 for _, success in results if success)
        
        print("\n3. Results Summary:")
        for symbol, success in results:
            status = "✓" if success else "✗"
            print(f"   {status} {symbol}")
            
        if success_count == len(symbols):
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: All quotes retrieved\033[0m")
            print("="*60)
            return True
        elif success_count > 0:
            print("\n" + "="*60)
            print(f"\033[93mTEST PARTIAL: {success_count}/{len(symbols)} quotes retrieved\033[0m")
            print("="*60)
            return True
        else:
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: No quotes retrieved\033[0m")
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


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# Phase 6 - Feature 1: Stock Quote Test Suite")
    print("#"*60)
    
    # Run tests
    test_results = []
    
    # Test 1: AAPL quote
    result1 = test_aapl_quote()
    test_results.append(("AAPL Quote Test", result1))
    
    # Small delay between tests
    time.sleep(1)
    
    # Test 2: Convenience function
    result2 = test_convenience_function()
    test_results.append(("Convenience Function Test", result2))
    
    # Small delay between tests
    time.sleep(1)
    
    # Test 3: Multiple quotes
    result3 = test_multiple_quotes()
    test_results.append(("Multiple Quotes Test", result3))
    
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
        print("  - Market data subscriptions are active")
        print("  - API connections are enabled")
        print("  - Markets are open (or delayed data is available)")
        sys.exit(1)