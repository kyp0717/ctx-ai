"""
Unit tests for MinuteBar dataclass and basic BarDataClient functionality
Phase 12 - Bar Data Unit Tests
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import unittest
from unittest.mock import Mock, patch

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from bar_data import MinuteBar, BarDataClient


class TestMinuteBar(unittest.TestCase):
    """Test MinuteBar data class"""
    
    def test_minute_bar_creation(self):
        """Test creating a MinuteBar instance"""
        timestamp = datetime.now()
        bar = MinuteBar(
            timestamp=timestamp,
            open=150.0,
            high=151.0,
            low=149.5,
            close=150.5,
            volume=10000,
            wap=150.25,
            count=50
        )
        
        self.assertEqual(bar.timestamp, timestamp)
        self.assertEqual(bar.open, 150.0)
        self.assertEqual(bar.high, 151.0)
        self.assertEqual(bar.low, 149.5)
        self.assertEqual(bar.close, 150.5)
        self.assertEqual(bar.volume, 10000)
        self.assertEqual(bar.wap, 150.25)
        self.assertEqual(bar.count, 50)
        
    def test_minute_bar_string_representation(self):
        """Test string representation of MinuteBar"""
        timestamp = datetime(2025, 9, 4, 10, 30, 0)
        bar = MinuteBar(
            timestamp=timestamp,
            open=150.0,
            high=151.0,
            low=149.5,
            close=150.5,
            volume=10000
        )
        
        bar_str = str(bar)
        self.assertIn("10:30", bar_str)
        self.assertIn("O:150.00", bar_str)
        self.assertIn("H:151.00", bar_str)
        self.assertIn("L:149.50", bar_str)
        self.assertIn("C:150.50", bar_str)
        self.assertIn("V:10000", bar_str)


class TestBarDataClientBasics(unittest.TestCase):
    """Test basic BarDataClient functionality"""
    
    def setUp(self):
        """Set up test client"""
        self.client = BarDataClient()
        
    def test_initial_state(self):
        """Test initial state of BarDataClient"""
        self.assertEqual(len(self.client.bars), 0)
        self.assertIsNone(self.client.latest_bar)
        self.assertIsNone(self.client.current_ema)
        self.assertEqual(self.client.ema_period, 9)
        self.assertFalse(self.client.is_streaming)
        self.assertEqual(len(self.client.ema_values), 0)
        
    def test_get_bars_for_period(self):
        """Test getting bars for a specific time period"""
        now = datetime.now()
        
        # Add bars with different timestamps
        for i in range(20):
            bar = MinuteBar(
                timestamp=now - timedelta(minutes=20-i),
                open=100,
                high=101,
                low=99,
                close=100,
                volume=1000
            )
            self.client.bars.append(bar)
            
        # Get bars for last 10 minutes
        recent_bars = self.client.get_bars_for_period(10)
        
        # Should get approximately 10 bars
        self.assertTrue(8 <= len(recent_bars) <= 11)
        
        # All returned bars should be within the time period
        cutoff = now - timedelta(minutes=10)
        for bar in recent_bars:
            self.assertTrue(bar.timestamp >= cutoff)
            
    @patch('bar_data.logger')
    def test_historical_data_handler(self, mock_logger):
        """Test handling of historical data from TWS"""
        # Create a mock BarData object
        mock_bar = Mock()
        mock_bar.date = "20250904 10:30:00"
        mock_bar.open = 150.0
        mock_bar.high = 151.0
        mock_bar.low = 149.5
        mock_bar.close = 150.5
        mock_bar.volume = 10000
        mock_bar.wap = 150.25
        mock_bar.count = 50
        
        # Process the bar
        self.client.historicalData(reqId=1, bar=mock_bar)
        
        # Check that bar was added
        self.assertEqual(len(self.client.bars), 1)
        self.assertIsNotNone(self.client.latest_bar)
        self.assertEqual(self.client.latest_bar.close, 150.5)
        self.assertTrue(self.client._bar_data_received.is_set())


if __name__ == "__main__":
    print("\n" + "="*50)
    print("FEATURE TEST: Phase 12 - Bar Data Unit Tests")
    print("="*50 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestMinuteBar))
    suite.addTests(loader.loadTestsFromTestCase(TestBarDataClientBasics))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*50)
    if result.wasSuccessful():
        print("\033[92m✅ All unit tests passed!\033[0m")
    else:
        print(f"\033[91m❌ Tests failed: {len(result.failures)} failures\033[0m")
    print("="*50)
    
    sys.exit(0 if result.wasSuccessful() else 1)