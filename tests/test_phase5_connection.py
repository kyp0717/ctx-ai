#!/usr/bin/env python
"""
Phase 5 - Feature 1: Connection Test
Test script to verify connection to TWS on port 7500
"""

import sys
import time
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from connection import TWSConnection, create_connection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_tws_connection():
    """Test connection to TWS on port 7500"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 5 - Connection to TWS")
    print("="*60)
    
    # Test parameters
    host = "127.0.0.1"
    port = 7500
    client_id = 1
    
    print(f"\nTest Input:")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Client ID: {client_id}")
    print("-"*40)
    
    try:
        # Create connection instance
        print("\n1. Creating TWSConnection instance...")
        connection = TWSConnection()
        print("   ✓ Instance created successfully")
        
        # Attempt to connect
        print(f"\n2. Attempting connection to TWS at {host}:{port}...")
        success = connection.connect_to_tws(host, port, client_id)
        
        if success:
            print(f"   ✓ Connected successfully!")
            
            # Check connection status
            print("\n3. Verifying connection status...")
            is_connected = connection.is_connected()
            print(f"   Connected: {is_connected}")
            print(f"   Next Order ID: {connection.next_order_id}")
            
            if is_connected:
                print("\n4. Connection details:")
                print(f"   - Connection established: Yes")
                print(f"   - Next Order ID: {connection.next_order_id}")
                print(f"   - Connection time: {connection.connection_time}")
                
                # Keep connection alive for a moment
                print("\n5. Testing connection stability (3 seconds)...")
                time.sleep(3)
                
                if connection.is_connected():
                    print("   ✓ Connection remains stable")
                else:
                    print("   ✗ Connection lost")
                    
                # Disconnect
                print("\n6. Disconnecting from TWS...")
                connection.disconnect_from_tws()
                print("   ✓ Disconnected successfully")
                
                # Final result
                print("\n" + "="*60)
                print("\033[92mTEST SUCCESSFUL: Connection to TWS established\033[0m")
                print("="*60)
                return True
            else:
                print("\n" + "="*60)
                print("\033[91mTEST FAILED: Connected but not fully established\033[0m")
                print("="*60)
                return False
                
        else:
            print(f"   ✗ Failed to connect")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Could not connect to TWS\033[0m")
            print("Possible reasons:")
            print("  1. TWS/IB Gateway is not running")
            print("  2. API connections are not enabled in TWS")
            print("  3. Port 7500 is not configured or blocked")
            print("  4. Another client is using the same client ID")
            print("="*60)
            return False
            
    except ImportError as e:
        print("\n" + "="*60)
        print("\033[91mTEST FAILED: Import Error\033[0m")
        print(f"Error: {e}")
        print("Please ensure ibapi is installed in the virtual environment")
        print("="*60)
        return False
        
    except Exception as e:
        print("\n" + "="*60)
        print(f"\033[91mTEST FAILED: Unexpected error\033[0m")
        print(f"Error: {e}")
        print("="*60)
        return False


def test_factory_function():
    """Test the create_connection factory function"""
    
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 5 - Factory Function Test")
    print("="*60)
    
    print("\nTest Input:")
    print("  Using create_connection() factory function")
    print("-"*40)
    
    try:
        print("\n1. Testing create_connection factory function...")
        connection = create_connection(host="127.0.0.1", port=7500, client_id=2)
        
        if connection:
            print("   ✓ Factory function returned connection object")
            print(f"   Connected: {connection.is_connected()}")
            print(f"   Next Order ID: {connection.next_order_id}")
            
            # Disconnect
            connection.disconnect_from_tws()
            
            print("\n" + "="*60)
            print("\033[92mTEST SUCCESSFUL: Factory function works correctly\033[0m")
            print("="*60)
            return True
        else:
            print("   ✗ Factory function returned None")
            print("\n" + "="*60)
            print("\033[91mTEST FAILED: Factory function returned None\033[0m")
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
    print("# Phase 5 - Feature 1: TWS Connection Test Suite")
    print("#"*60)
    
    # Run tests
    test_results = []
    
    # Test 1: Direct connection
    result1 = test_tws_connection()
    test_results.append(("Direct Connection Test", result1))
    
    # Small delay between tests
    time.sleep(1)
    
    # Test 2: Factory function
    result2 = test_factory_function()
    test_results.append(("Factory Function Test", result2))
    
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
        sys.exit(1)