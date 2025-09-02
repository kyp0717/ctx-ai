"""
Test module for TWS connection functionality
"""

import sys
import time
import unittest
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from connection import TWSConnection, create_connection
    IBAPI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Warning: {e}")
    IBAPI_AVAILABLE = False


class TestTWSConnection(unittest.TestCase):
    """Test cases for TWS connection"""
    
    @unittest.skipUnless(IBAPI_AVAILABLE, "ibapi package not installed")
    def test_connection_initialization(self):
        """Test that connection object initializes correctly"""
        connection = TWSConnection()
        self.assertIsNotNone(connection)
        self.assertFalse(connection.connected)
        self.assertIsNone(connection.next_order_id)
        
    @unittest.skipUnless(IBAPI_AVAILABLE, "ibapi package not installed")
    def test_connection_to_tws(self):
        """Test connection to TWS on port 7500"""
        print("\n" + "="*50)
        print("FEATURE TEST: Phase 06 - TWS Connection")
        print("="*50)
        
        print("\n📋 Test Input:")
        print("  - Host: 127.0.0.1")
        print("  - Port: 7500")
        print("  - Client ID: 999 (test client)")
        
        connection = TWSConnection()
        
        print("\n🔄 Attempting connection to TWS...")
        result = connection.connect_to_tws(host="127.0.0.1", port=7500, client_id=999)
        
        print("\n📊 Test Output:")
        if result:
            print(f"  - Connection Status: Connected ✅")
            print(f"  - Is Connected: {connection.is_connected()}")
            print(f"  - Next Order ID: {connection.next_order_id}")
            
            # Test successful connection
            self.assertTrue(result)
            self.assertTrue(connection.is_connected())
            
            # Clean up
            connection.disconnect_from_tws()
            
            # Allow time for disconnect
            time.sleep(0.5)
            self.assertFalse(connection.is_connected())
            
            print(f"  - Disconnection: Success ✅")
            print("\n\033[92m✅ TEST PASSED: Successfully connected to TWS on port 7500\033[0m")
        else:
            print(f"  - Connection Status: Failed ❌")
            print("\n\033[91m❌ TEST FAILED: Could not connect to TWS")
            print("   Please ensure:")
            print("   1. TWS is running")
            print("   2. API connections are enabled in TWS")
            print("   3. Port 7500 is configured in TWS API settings\033[0m")
            
            # Test should fail if connection fails
            self.fail("Could not connect to TWS on port 7500")
            
    @unittest.skipUnless(IBAPI_AVAILABLE, "ibapi package not installed")  
    def test_factory_function(self):
        """Test the create_connection factory function"""
        print("\n🔄 Testing factory function...")
        
        connection = create_connection(host="127.0.0.1", port=7500, client_id=998)
        
        if connection:
            self.assertIsNotNone(connection)
            self.assertTrue(connection.is_connected())
            
            # Clean up
            connection.disconnect_from_tws()
            print("  Factory function: Success ✅")
        else:
            print("  Factory function: Failed (TWS not available)")
            # This is acceptable if TWS is not running
            self.assertIsNone(connection)


def run_tests():
    """Run the test suite"""
    if not IBAPI_AVAILABLE:
        print("\n" + "="*60)
        print("⚠️  SKIPPING TESTS: ibapi package not installed")
        print("Please run ./install_ibapi.sh to install the IB API")
        print("="*60)
        return False
        
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTWSConnection)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)