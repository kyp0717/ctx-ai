"""
Live integration test for bar data functionality with real TWS
Phase 12 - Bar Data Live TWS Test
NOTE: Requires TWS to be running on port 7500
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import unittest
import time

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from bar_data import BarDataClient


class TestBarDataLiveTWS(unittest.TestCase):
    """Test BarDataClient with real TWS connection"""
    
    @classmethod
    def setUpClass(cls):
        """Set up TWS connection for all tests"""
        cls.client = BarDataClient()
        print("\nConnecting to TWS on port 7500...")
        
        # Try to connect to TWS
        cls.connected = cls.client.connect_to_tws(
            host="127.0.0.1", 
            port=7500, 
            client_id=12  # Use unique client ID for Phase 12
        )
        
        if cls.connected:
            print("✅ Connected to TWS")
            time.sleep(2)  # Wait for connection to stabilize
        else:
            print("⚠️ Could not connect to TWS - tests will be skipped")
            
    @classmethod
    def tearDownClass(cls):
        """Disconnect from TWS after all tests"""
        if cls.connected and cls.client.is_connected():
            cls.client.disconnect_from_tws()
            print("\nDisconnected from TWS")
            
    def test_request_historical_minute_bars(self):
        """Test requesting real historical minute bars from TWS"""
        if not self.connected:
            self.skipTest("TWS not connected")
            
        print("\n📊 Requesting historical minute bars for AAPL...")
        
        # Request 1 day of 1-minute bars for AAPL
        bars = self.client.request_historical_bars(
            symbol="AAPL",
            duration="1 D",
            bar_size="1 min"
        )
        
        # Verify we got bars
        self.assertGreater(len(bars), 0, "Should receive historical bars")
        print(f"✅ Received {len(bars)} historical bars")
        
        # Check first and last bar
        if bars:
            first_bar = bars[0]
            last_bar = bars[-1]
            print(f"First bar: {first_bar}")
            print(f"Last bar: {last_bar}")
            
            # Verify bar data integrity
            for bar in bars[:5]:  # Check first 5 bars
                self.assertIsNotNone(bar.timestamp)
                self.assertGreater(bar.high, 0)
                self.assertGreater(bar.low, 0)
                self.assertGreaterEqual(bar.high, bar.low)
                self.assertGreaterEqual(bar.high, bar.open)
                self.assertGreaterEqual(bar.high, bar.close)
                self.assertLessEqual(bar.low, bar.open)
                self.assertLessEqual(bar.low, bar.close)
                
    def test_ema_calculation_with_real_data(self):
        """Test EMA calculation with real market data"""
        if not self.connected:
            self.skipTest("TWS not connected")
            
        print("\n📈 Testing EMA calculation with real AAPL data...")
        
        # Request historical bars
        bars = self.client.request_historical_bars(
            symbol="AAPL",
            duration="1 D",
            bar_size="1 min"
        )
        
        if len(bars) < self.client.ema_period:
            self.skipTest(f"Not enough bars ({len(bars)}) for EMA calculation")
            
        # EMA should have been calculated automatically
        self.assertIsNotNone(self.client.current_ema)
        print(f"✅ Current 9-period EMA: ${self.client.current_ema:.2f}")
        
        # Verify EMA is within reasonable range of recent prices
        recent_prices = [bar.close for bar in bars[-10:]]
        avg_recent = sum(recent_prices) / len(recent_prices)
        
        # EMA should be close to recent average (within 5%)
        ema_diff_pct = abs(self.client.current_ema - avg_recent) / avg_recent * 100
        self.assertLess(ema_diff_pct, 5, 
                       f"EMA should be within 5% of recent average")
        print(f"✅ EMA validation passed (within {ema_diff_pct:.2f}% of recent avg)")
        
    def test_streaming_bars(self):
        """Test real-time bar streaming"""
        if not self.connected:
            self.skipTest("TWS not connected")
            
        print("\n📡 Testing real-time bar streaming for SPY...")
        
        # Start streaming bars for SPY
        self.client.start_streaming_bars("SPY")
        self.assertTrue(self.client.is_streaming)
        
        print("Waiting for real-time bars (10 seconds)...")
        time.sleep(10)  # Wait for some bars
        
        # Check if we received streaming bars
        streaming_count = len(self.client._streaming_bars)
        print(f"✅ Received {streaming_count} streaming bars")
        
        # Stop streaming
        self.client.stop_streaming_bars()
        self.assertFalse(self.client.is_streaming)
        
        # Verify we got some bars
        self.assertGreater(streaming_count, 0, "Should receive streaming bars")
        
        # Check the latest bar if available
        if self.client.latest_bar:
            print(f"Latest bar: {self.client.latest_bar}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("FEATURE TEST: Phase 12 - Bar Data Live TWS Test")
    print("="*60)
    print("\n⚠️  REQUIREMENTS:")
    print("  - TWS must be running on port 7500")
    print("  - API connections must be enabled")
    print("  - Paper trading account recommended")
    print("  - Market should be open for best results\n")
    
    # Ask for confirmation
    response = input("Is TWS running? (y/n): ")
    if response.lower() != 'y':
        print("❌ Test skipped - TWS not running")
        sys.exit(0)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestBarDataLiveTWS))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("\033[92m✅ All live tests passed!\033[0m")
    else:
        print(f"\033[91m❌ Tests failed: {len(result.failures)} failures\033[0m")
    print("="*60)
    
    sys.exit(0 if result.wasSuccessful() else 1)