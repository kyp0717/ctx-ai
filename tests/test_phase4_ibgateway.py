#!/usr/bin/env python3
"""
Phase 4 Tests - IBGateway Installation and Startup
Tests to verify IBGateway installation and running status
"""

import os
import sys
import socket
import subprocess
import time
import unittest
import json
from pathlib import Path


class TestIBGatewayInstallation(unittest.TestCase):
    """Test suite for IBGateway installation verification"""
    
    def setUp(self):
        """Setup test environment"""
        self.home_dir = Path.home()
        self.config_dir = self.home_dir / ".ibxpy"
        self.possible_gateway_paths = [
            self.home_dir / "Jts",
            self.home_dir / "IBGateway",
            Path("/Applications/IB Gateway.app"),
            self.home_dir / "Applications/IB Gateway.app"
        ]
        
    def test_01_ibgateway_installation_exists(self):
        """Test: Check whether IBGateway has been installed"""
        print("\n" + "="*60)
        print("FEATURE TEST: Phase 04 - IBGateway Installation Check")
        print("="*60)
        
        print("\nTest Input: Searching for IBGateway installation in common locations")
        print("Checking paths:")
        
        gateway_found = False
        gateway_location = None
        
        for path in self.possible_gateway_paths:
            print(f"  - {path}")
            if path.exists():
                # Look for ibgateway executable or app
                if path.name == "IB Gateway.app":
                    # macOS application
                    gateway_exec = path / "Contents/MacOS/ibgateway"
                    if gateway_exec.exists():
                        gateway_found = True
                        gateway_location = gateway_exec
                        break
                else:
                    # Search for ibgateway executable in subdirectories
                    for gateway_file in path.rglob("ibgateway"):
                        if gateway_file.is_file() and os.access(gateway_file, os.X_OK):
                            gateway_found = True
                            gateway_location = gateway_file
                            break
                    
                    if gateway_found:
                        break
        
        print("\nTest Output:")
        if gateway_found:
            print(f"\033[92m✓ SUCCESS: IBGateway found at: {gateway_location}\033[0m")
            
            # Check if it's executable
            if os.access(gateway_location, os.X_OK):
                print(f"\033[92m✓ Gateway is executable\033[0m")
            else:
                print(f"\033[93m⚠ Warning: Gateway found but not executable\033[0m")
                
        else:
            print(f"\033[91m✗ FAILURE: IBGateway installation not found\033[0m")
            print("\nPlease install IBGateway using one of these methods:")
            print("  1. Run: ./ctx-ai/scripts/install_ibgateway.sh")
            print("  2. Download manually from: https://www.interactivebrokers.com/en/index.php?f=16457")
            
        self.assertTrue(gateway_found, "IBGateway installation not found")
        
    def test_02_startup_script_exists(self):
        """Test: Verify startup script exists and is executable"""
        print("\n" + "="*60)
        print("FEATURE TEST: Phase 04 - Startup Script Verification")
        print("="*60)
        
        script_path = Path("ctx-ai/scripts/start_ibgateway.sh")
        
        print(f"\nTest Input: Checking for startup script at {script_path}")
        
        print("\nTest Output:")
        if script_path.exists():
            print(f"\033[92m✓ SUCCESS: Startup script exists\033[0m")
            
            # Check if executable
            if os.access(script_path, os.X_OK):
                print(f"\033[92m✓ Script is executable\033[0m")
            else:
                print(f"\033[93m⚠ Warning: Script exists but not executable\033[0m")
                print("  Fix with: chmod +x ctx-ai/scripts/start_ibgateway.sh")
        else:
            print(f"\033[91m✗ FAILURE: Startup script not found\033[0m")
            
        self.assertTrue(script_path.exists(), "Startup script not found")
        

class TestIBGatewayRunning(unittest.TestCase):
    """Test suite for IBGateway running status"""
    
    def setUp(self):
        """Setup test environment"""
        self.paper_port = 7497
        self.live_port = 7496
        self.config_dir = Path.home() / ".ibxpy"
        self.credentials_file = self.config_dir / "credentials.conf"
        
    def test_03_credentials_configuration(self):
        """Test: Run IBGateway with proper credentials"""
        print("\n" + "="*60)
        print("FEATURE TEST: Phase 04 - Credentials Configuration")
        print("="*60)
        
        print("\nTest Input: Checking credentials configuration")
        
        # First, setup configuration if needed
        setup_result = subprocess.run(
            ["./ctx-ai/scripts/start_ibgateway.sh", "setup"],
            capture_output=True,
            text=True
        )
        
        print("\nTest Output:")
        
        if self.credentials_file.exists():
            print(f"\033[92m✓ SUCCESS: Credentials file exists at {self.credentials_file}\033[0m")
            
            # Check file permissions (should be 600 for security)
            stat_info = os.stat(self.credentials_file)
            mode = oct(stat_info.st_mode)[-3:]
            
            if mode == "600":
                print(f"\033[92m✓ File has secure permissions (600)\033[0m")
            else:
                print(f"\033[93m⚠ Warning: File permissions are {mode}, should be 600\033[0m")
                
            # Check if credentials are configured
            with open(self.credentials_file, 'r') as f:
                content = f.read()
                
            has_username = "IB_USERNAME=" in content and "IB_USERNAME=\n" not in content
            has_password = "IB_PASSWORD=" in content and "IB_PASSWORD=\n" not in content
            
            if has_username and has_password:
                print(f"\033[92m✓ Credentials are configured\033[0m")
            else:
                print(f"\033[93m⚠ Warning: Credentials not fully configured\033[0m")
                print(f"  Please edit: {self.credentials_file}")
                print("  Set IB_USERNAME and IB_PASSWORD values")
                
        else:
            print(f"\033[91m✗ FAILURE: Credentials file not created\033[0m")
            print(f"  Run: ./ctx-ai/scripts/start_ibgateway.sh setup")
            
        self.assertTrue(self.credentials_file.exists(), "Credentials configuration not found")
        
    def test_04_ibgateway_port_check(self):
        """Test: Check if IBGateway is running"""
        print("\n" + "="*60)
        print("FEATURE TEST: Phase 04 - IBGateway Running Status")
        print("="*60)
        
        print("\nTest Input: Checking IBGateway API ports")
        print(f"  - Paper Trading Port: {self.paper_port}")
        print(f"  - Live Trading Port: {self.live_port}")
        
        def check_port(host, port):
            """Check if a port is open"""
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((host, port))
                sock.close()
                return result == 0
            except:
                return False
        
        print("\nTest Output:")
        
        paper_running = check_port("127.0.0.1", self.paper_port)
        live_running = check_port("127.0.0.1", self.live_port)
        
        if paper_running:
            print(f"\033[92m✓ SUCCESS: IBGateway is running on paper port {self.paper_port}\033[0m")
        else:
            print(f"\033[93m⚠ IBGateway not detected on paper port {self.paper_port}\033[0m")
            
        if live_running:
            print(f"\033[92m✓ SUCCESS: IBGateway is running on live port {self.live_port}\033[0m")
        else:
            print(f"\033[93m⚠ IBGateway not detected on live port {self.live_port}\033[0m")
            
        if not paper_running and not live_running:
            print(f"\033[91m✗ FAILURE: IBGateway is not running\033[0m")
            print("\nTo start IBGateway:")
            print("  1. Configure credentials: ./ctx-ai/scripts/start_ibgateway.sh setup")
            print("  2. Edit: ~/.ibxpy/credentials.conf")
            print("  3. Start: ./ctx-ai/scripts/start_ibgateway.sh start")
            
            # Check if we can get status from the script
            status_result = subprocess.run(
                ["./ctx-ai/scripts/start_ibgateway.sh", "status"],
                capture_output=True,
                text=True
            )
            
            if "not running" in status_result.stdout.lower():
                print("\nScript confirms: IBGateway is not running")
        else:
            # At least one port is active
            print(f"\033[92m✓ IBGateway API is accessible\033[0m")
            
        # Test passes if at least one port is available
        self.assertTrue(
            paper_running or live_running,
            "IBGateway is not running on any port"
        )
        
    def test_05_connection_test(self):
        """Test: Verify API connection capability"""
        print("\n" + "="*60)
        print("FEATURE TEST: Phase 04 - API Connection Test")
        print("="*60)
        
        print("\nTest Input: Testing API connection capability")
        
        # Try to import ibapi to test connection
        try:
            from ibapi.client import EClient
            from ibapi.wrapper import EWrapper
            import threading
            
            class TestApp(EWrapper, EClient):
                def __init__(self):
                    EClient.__init__(self, self)
                    self.connected = False
                    
                def error(self, reqId, errorCode, errorString, advancedOrderRejectJson=""):
                    if errorCode == 502:  # Cannot connect to TWS
                        print(f"\033[91m✗ Cannot connect to IBGateway\033[0m")
                    elif errorCode == 504:  # Not connected
                        pass  # Expected when disconnecting
                    else:
                        print(f"  API Message: {errorString}")
                        
                def nextValidId(self, orderId):
                    self.connected = True
                    print(f"\033[92m✓ Connected! Next Valid Order ID: {orderId}\033[0m")
                    self.disconnect()
                    
            print("\nTest Output:")
            
            # Try paper trading port first
            app = TestApp()
            app.connect("127.0.0.1", 7497, clientId=999)
            
            # Run in thread with timeout
            api_thread = threading.Thread(target=app.run)
            api_thread.daemon = True
            api_thread.start()
            
            # Wait up to 5 seconds for connection
            timeout = 5
            start_time = time.time()
            
            while (time.time() - start_time) < timeout and not app.connected:
                time.sleep(0.1)
                
            if app.connected:
                print(f"\033[92m✓ SUCCESS: API connection established\033[0m")
                result = True
            else:
                print(f"\033[91m✗ FAILURE: Could not establish API connection\033[0m")
                result = False
                
            try:
                app.disconnect()
            except:
                pass
                
        except ImportError:
            print("\nTest Output:")
            print(f"\033[93m⚠ Warning: ibapi package not installed\033[0m")
            print("  Cannot perform connection test")
            print("  Install with: ./ctx-ai/scripts/install_ibapi.sh")
            result = None
            
        # This test is informational - don't fail if ibapi is not installed
        if result is not None:
            self.assertTrue(result, "Could not establish API connection")
        else:
            self.skipTest("ibapi not installed - skipping connection test")


def run_tests():
    """Run all Phase 4 tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests in order
    suite.addTests(loader.loadTestsFromTestCase(TestIBGatewayInstallation))
    suite.addTests(loader.loadTestsFromTestCase(TestIBGatewayRunning))
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success/failure
    return result.wasSuccessful()


if __name__ == "__main__":
    # Change to project root directory
    project_root = Path(__file__).parent.parent.parent
    os.chdir(project_root)
    
    print("\n" + "="*60)
    print("RUNNING PHASE 4 TESTS - IBGateway Installation & Startup")
    print("="*60)
    
    success = run_tests()
    
    print("\n" + "="*60)
    if success:
        print("\033[92mALL PHASE 4 TESTS PASSED\033[0m")
    else:
        print("\033[91mSOME PHASE 4 TESTS FAILED\033[0m")
    print("="*60)
    
    sys.exit(0 if success else 1)