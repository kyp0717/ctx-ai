"""
Unit tests for EMA calculation functionality
Phase 12 - EMA Calculation Tests
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import unittest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from bar_data import MinuteBar, BarDataClient


class TestEMACalculation(unittest.TestCase):
    """Test EMA calculation functionality"""
    
    def setUp(self):
        """Set up test client"""
        self.client = BarDataClient()
        
    def test_ema_calculation_initial(self):
        """Test initial EMA calculation with historical data"""
        # Create sample bars with known values
        for i in range(15):
            bar = MinuteBar(
                timestamp=datetime.now() - timedelta(minutes=15-i),
                open=100 + i * 0.1,
                high=100 + i * 0.2,
                low=100 - i * 0.1,
                close=100 + i * 0.5,  # Closing prices: 100, 100.5, 101, ... 107
                volume=1000 + i * 100
            )
            self.client.bars.append(bar)
            
        # Calculate initial EMA
        self.client.calculate_initial_ema()
        
        # Check that EMA was calculated
        self.assertIsNotNone(self.client.current_ema)
        self.assertTrue(len(self.client.ema_values) > 0)
        
        # Verify the first EMA is the SMA of first 9 values
        expected_first_sma = sum(self.client.bars[i].close for i in range(9)) / 9
        self.assertAlmostEqual(self.client.ema_values[0], expected_first_sma, places=2)
        
        # EMA should be reasonable given the upward trend
        self.assertTrue(100 < self.client.current_ema < 108)
        
    def test_ema_calculation_incremental(self):
        """Test incremental EMA calculation with new prices"""
        # Set up initial EMA
        self.client.current_ema = 100.0
        
        # Calculate EMA for new prices
        new_prices = [101.0, 102.0, 103.0]
        self.client.calculate_ema(new_prices)
        
        # Check that EMA was updated
        self.assertIsNotNone(self.client.current_ema)
        self.assertEqual(len(self.client.ema_values), 3)
        
        # Verify EMA is smoothed (between old value and new prices)
        self.assertTrue(100.0 < self.client.current_ema < 103.0)
        
        # Verify each EMA value is progressively higher
        for i in range(1, len(self.client.ema_values)):
            self.assertGreater(self.client.ema_values[i], self.client.ema_values[i-1])
            
    def test_ema_calculation_with_insufficient_data(self):
        """Test EMA calculation with insufficient data"""
        # Add only 5 bars (less than 9 period)
        for i in range(5):
            bar = MinuteBar(
                timestamp=datetime.now() - timedelta(minutes=5-i),
                open=100,
                high=101,
                low=99,
                close=100 + i,
                volume=1000
            )
            self.client.bars.append(bar)
            
        # Try to calculate EMA
        self.client.calculate_initial_ema()
        
        # EMA should remain None due to insufficient data
        self.assertIsNone(self.client.current_ema)
        self.assertEqual(len(self.client.ema_values), 0)
        
    def test_ema_formula_accuracy(self):
        """Test that EMA formula is correctly implemented"""
        # Use known test data
        prices = [22.27, 22.19, 22.08, 22.17, 22.18, 
                 22.13, 22.23, 22.43, 22.24, 22.29,
                 22.15, 22.39, 22.38, 22.61, 23.36]
        
        # Add bars with these prices
        for i, price in enumerate(prices):
            bar = MinuteBar(
                timestamp=datetime.now() - timedelta(minutes=len(prices)-i),
                open=price,
                high=price + 0.1,
                low=price - 0.1,
                close=price,
                volume=1000
            )
            self.client.bars.append(bar)
            
        # Calculate EMA
        self.client.calculate_initial_ema()
        
        # Verify EMA was calculated
        self.assertIsNotNone(self.client.current_ema)
        
        # The 9-period EMA should follow the upward trend
        # First SMA should be average of first 9 prices
        first_nine_avg = sum(prices[:9]) / 9
        self.assertAlmostEqual(self.client.ema_values[0], first_nine_avg, places=2)
        
        # Current EMA should reflect the recent upward movement
        self.assertGreater(self.client.current_ema, first_nine_avg)
        
    def test_ema_multiplier(self):
        """Test that EMA multiplier is correctly calculated"""
        # The multiplier for 9-period EMA should be 2/(9+1) = 0.2
        expected_multiplier = 2 / (self.client.ema_period + 1)
        self.assertAlmostEqual(expected_multiplier, 0.2, places=4)
        
        # Verify this is used in calculation
        self.client.current_ema = 100.0
        new_price = 110.0
        
        # Calculate expected new EMA manually
        multiplier = 2 / (self.client.ema_period + 1)
        expected_ema = (new_price * multiplier) + (100.0 * (1 - multiplier))
        
        # Calculate using the method
        self.client.calculate_ema([new_price])
        
        # Should match our manual calculation
        self.assertAlmostEqual(self.client.current_ema, expected_ema, places=4)


if __name__ == "__main__":
    print("\n" + "="*50)
    print("FEATURE TEST: Phase 12 - EMA Calculation Tests")
    print("="*50 + "\n")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestEMACalculation))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*50)
    if result.wasSuccessful():
        print("\033[92m✅ All EMA tests passed!\033[0m")
    else:
        print(f"\033[91m❌ Tests failed: {len(result.failures)} failures\033[0m")
    print("="*50)
    
    sys.exit(0 if result.wasSuccessful() else 1)