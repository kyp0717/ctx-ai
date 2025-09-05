"""
Integration tests for bar data functionality with TWS
Phase 12 - Bar Data Integration Tests
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import unittest
import time
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from bar_data import MinuteBar, BarDataClient


class TestBarDataIntegration(unittest.TestCase):
    """Test BarDataClient integration with TWS"""
    
    def setUp(self):
        """Set up test client"""
        self.client = BarDataClient()
        
    def test_realtime_bar_handler(self):
        """Test handling of real-time bar data"""
        # Set initial EMA for testing
        self.client.current_ema = 100.0
        
        # Process a real-time bar
        timestamp = int(datetime.now().timestamp())
        self.client.realtimeBar(
            reqId=1,
            time=timestamp,
            open_=101.0,
            high=102.0,
            low=100.5,
            close=101.5,
            volume=1000,
            wap=101.25,
            count=10
        )
        
        # Check that bar was added to streaming bars
        self.assertTrue(len(self.client._streaming_bars) > 0)
        self.assertIsNotNone(self.client.latest_bar)
        self.assertEqual(self.client.latest_bar.close, 101.5)
        
        # Check that EMA was updated
        self.assertNotEqual(self.client.current_ema, 100.0)
        self.assertTrue(len(self.client.ema_values) > 0)
        
    def test_historical_data_end_handler(self):
        """Test handling of historical data completion"""
        # Add some test bars
        for i in range(5):
            self.client.bars.append(MinuteBar(
                timestamp=datetime.now(),
                open=100, high=101, low=99, close=100,
                volume=1000
            ))
            
        # Call historicalDataEnd
        self.client.historicalDataEnd(reqId=1, start="", end="")
        
        # Check that event was set
        self.assertTrue(self.client._historical_data_end.is_set())
        
    def test_streaming_state_management(self):
        """Test streaming state transitions"""
        # Initially not streaming
        self.assertFalse(self.client.is_streaming)
        
        # Mock the reqRealTimeBars method
        self.client.reqRealTimeBars = Mock()
        
        # Start streaming
        self.client.start_streaming_bars("AAPL")
        self.assertTrue(self.client.is_streaming)
        self.client.reqRealTimeBars.assert_called_once()
        
        # Try to start again (should not call again)
        self.client.reqRealTimeBars.reset_mock()
        self.client.start_streaming_bars("AAPL")
        self.client.reqRealTimeBars.assert_not_called()
        
        # Stop streaming
        self.client.cancelRealTimeBars = Mock()
        self.client.stop_streaming_bars(req_id=1)
        self.assertFalse(self.client.is_streaming)
        self.client.cancelRealTimeBars.assert_called_once_with(1)
        
    @patch('bar_data.BarDataClient.reqHistoricalData')
    def test_request_historical_bars(self, mock_req_historical):
        """Test requesting historical bars"""
        # Set up mock to simulate data received
        def simulate_data_received(*args, **kwargs):
            # Add some test bars
            for i in range(10):
                bar = Mock()
                bar.date = f"20250904 10:{30+i}:00"
                bar.open = 150.0 + i
                bar.high = 151.0 + i
                bar.low = 149.0 + i
                bar.close = 150.0 + i
                bar.volume = 1000 * (i + 1)
                bar.wap = 150.0 + i
                bar.count = 50
                self.client.historicalData(1, bar)
            
            # Signal end of data
            self.client.historicalDataEnd(1, "", "")
            
        mock_req_historical.side_effect = simulate_data_received
        
        # Request bars
        bars = self.client.request_historical_bars("AAPL", "1 D", "1 min")
        
        # Verify request was made
        mock_req_historical.assert_called_once()
        
        # Check results
        self.assertEqual(len(bars), 10)
        self.assertEqual(len(self.client.bars), 10)
        
        # Verify EMA was calculated
        self.assertIsNotNone(self.client.current_ema)
        
    def test_get_current_ema_and_latest_bar(self):
        """Test accessor methods"""
        # Initially None
        self.assertIsNone(self.client.get_current_ema())
        self.assertIsNone(self.client.get_latest_bar())
        
        # Set values
        self.client.current_ema = 105.5
        test_bar = MinuteBar(
            timestamp=datetime.now(),
            open=100, high=101, low=99, close=100.5,
            volume=1000
        )
        self.client.latest_bar = test_bar
        
        # Test accessors
        self.assertEqual(self.client.get_current_ema(), 105.5)
        self.assertEqual(self.client.get_latest_bar(), test_bar)


if __name__ == "__main__":
    print("\n" + "="*50)
    print("FEATURE TEST: Phase 12 - Bar Data Integration Tests")
    print("="*50 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestBarDataIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*50)
    if result.wasSuccessful():
        print("\033[92m✅ All integration tests passed!\033[0m")
    else:
        print(f"\033[91m❌ Tests failed: {len(result.failures)} failures\033[0m")
    print("="*50)
    
    sys.exit(0 if result.wasSuccessful() else 1)