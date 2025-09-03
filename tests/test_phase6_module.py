#!/usr/bin/env python
"""
Phase 6 - Test 1: Module Test for Stock Quote
Tests the stock_quote module functionality for retrieving AAPL price
"""

import sys
import time
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from stock_quote import QuoteClient, StockQuote

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_retrieve_aapl_quote():
    """Test 1: Retrieve the current price for AAPL stock"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 6 - Test 1")
    print("Retrieve Current Price for AAPL Stock")
    print("="*60)
    
    # Test parameters
    symbol = "AAPL"
    host = "127.0.0.1"
    port = 7500
    client_id = 210
    
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
        print(f"   Next Order ID: {client.next_order_id}")
        
        # Request quote for AAPL
        print(f"\n3. Requesting real-time quote for {symbol}...")
        print("   Waiting for market data...")
        
        quote = client.get_stock_quote(symbol, timeout=5.0)
        
        if quote and quote.is_valid():
            print(f"   ✓ Quote received successfully!")
            
            print("\n4. Test Output - AAPL Quote Details:")
            print(f"   Symbol: {quote.symbol}")
            print(f"   Last Price: ${quote.last_price:.2f}")
            print(f"   Bid Price: ${quote.bid_price:.2f}")
            print(f"   Ask Price: ${quote.ask_price:.2f}")
            print(f"   Bid Size: {quote.bid_size}")
            print(f"   Ask Size: {quote.ask_size}")
            print(f"   Volume: {quote.volume:,}")
            print(f"   Timestamp: {quote.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Validate the data
            print("\n5. Data Validation:")
            assert quote.symbol == symbol, f"Symbol should be {symbol}"
            print(f"   ✓ Symbol matches: {quote.symbol}")
            
            assert quote.last_price > 0 or quote.bid_price > 0 or quote.ask_price > 0, "Should have price data"
            print(f"   ✓ Valid price data received")
            
            assert quote.timestamp is not None, "Should have timestamp"
            print(f"   ✓ Timestamp present")
            
            # Disconnect
            print("\n6. Disconnecting from TWS...")
            client.disconnect_from_tws()
            print("   ✓ Disconnected successfully")
            
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: Retrieved AAPL quote\033[0m")
            print(f"Current AAPL Price: ${quote.last_price:.2f}")
            print("="*60)
            return True
            
        else:
            print("   ✗ Failed to retrieve quote")
            client.disconnect_from_tws()
            
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Could not retrieve quote for AAPL\033[0m")
            print("Possible reasons:")
            print("  1. Market is closed")
            print("  2. No market data subscription")
            print("  3. Network issues")
            print("="*60)
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


if __name__ == "__main__":
    print("\n" + "#"*60)
    print("# Phase 6 - Test 1: Module Test")
    print("# Retrieve Current Price for AAPL Stock")
    print("#"*60)
    
    # Run the test
    result = test_retrieve_aapl_quote()
    
    # Exit with appropriate code
    if result:
        print("\n\033[92mMODULE TEST PASSED\033[0m")
        sys.exit(0)
    else:
        print("\n\033[91mMODULE TEST FAILED\033[0m")
        sys.exit(1)