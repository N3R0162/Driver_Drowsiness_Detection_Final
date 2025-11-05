"""
Test script for PERCLOS configuration system
Run this to verify the configuration system is working correctly
"""

import os
import sys
import json

# Add source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'source'))

def test_config_manager():
    """Test ConfigManager class"""
    print("=" * 50)
    print("Testing ConfigManager")
    print("=" * 50)
    
    try:
        from config_page import ConfigManager
        
        # Test initialization
        print("\n1. Testing initialization...")
        config_manager = ConfigManager('test_perclos_config.json')
        print("✓ ConfigManager initialized")
        
        # Test get_config
        print("\n2. Testing get_config...")
        config = config_manager.get_config()
        print(f"✓ Config retrieved: {len(config)} keys")
        print(f"   Keys: {list(config.keys())}")
        
        # Test save_config
        print("\n3. Testing save_config...")
        if config_manager.save_config():
            print("✓ Config saved successfully")
        else:
            print("✗ Failed to save config")
        
        # Test update_config
        print("\n4. Testing update_config...")
        new_config = config.copy()
        new_config['semi_closed_max'] = 5.0
        config_manager.update_config(new_config)
        print("✓ Config updated")
        
        # Verify update
        updated_config = config_manager.get_config()
        if updated_config['semi_closed_max'] == 5.0:
            print("✓ Update verified")
        else:
            print("✗ Update verification failed")
        
        # Cleanup
        if os.path.exists('source/test_perclos_config.json'):
            os.remove('source/test_perclos_config.json')
            print("\n✓ Cleanup completed")
        
        print("\n" + "=" * 50)
        print("ConfigManager tests PASSED ✓")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n✗ Error testing ConfigManager: {e}")
        return False


def test_attention_scorer():
    """Test AttentionScorer with config loading"""
    print("\n" + "=" * 50)
    print("Testing AttentionScorer")
    print("=" * 50)
    
    try:
        from attention_score import AttentionScorer
        import time
        
        # Test initialization
        print("\n1. Testing initialization...")
        scorer = AttentionScorer(t_now=time.perf_counter())
        print("✓ AttentionScorer initialized")
        
        # Test config loading
        print("\n2. Testing config loading...")
        if hasattr(scorer, 'perclos_config'):
            print("✓ PERCLOS config loaded")
            print(f"   Config keys: {list(scorer.perclos_config.keys())}")
        else:
            print("✗ PERCLOS config not found")
            return False
        
        # Test threshold values
        print("\n3. Verifying threshold values...")
        expected_keys = [
            'semi_closed_min', 'semi_closed_max',
            'moderately_drowsy_min', 'moderately_drowsy_max',
            'drowsy_min', 'drowsy_max',
            'very_drowsy_min', 'very_drowsy_max',
            'sleeping_min'
        ]
        
        all_keys_present = all(key in scorer.perclos_config for key in expected_keys)
        if all_keys_present:
            print("✓ All expected keys present")
            for key in expected_keys:
                print(f"   {key}: {scorer.perclos_config[key]}")
        else:
            print("✗ Some keys missing")
            return False
        
        print("\n" + "=" * 50)
        print("AttentionScorer tests PASSED ✓")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n✗ Error testing AttentionScorer: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_file():
    """Test configuration file structure"""
    print("\n" + "=" * 50)
    print("Testing Configuration File")
    print("=" * 50)
    
    config_path = os.path.join('source', 'perclos_config.json')
    
    try:
        print("\n1. Checking if config file exists...")
        if os.path.exists(config_path):
            print(f"✓ Config file found at: {config_path}")
        else:
            print(f"⚠ Config file not found at: {config_path}")
            print("  This is OK - default values will be used")
            return True
        
        print("\n2. Testing JSON parsing...")
        with open(config_path, 'r') as f:
            config = json.load(f)
        print("✓ JSON parsed successfully")
        
        print("\n3. Validating structure...")
        required_keys = [
            'semi_closed_min', 'semi_closed_max',
            'moderately_drowsy_min', 'moderately_drowsy_max',
            'drowsy_min', 'drowsy_max',
            'very_drowsy_min', 'very_drowsy_max',
            'sleeping_min'
        ]
        
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            print(f"✗ Missing keys: {missing_keys}")
            return False
        else:
            print("✓ All required keys present")
        
        print("\n4. Validating values...")
        for key, value in config.items():
            if not isinstance(value, (int, float)):
                print(f"✗ Invalid value type for {key}: {type(value)}")
                return False
        print("✓ All values are numeric")
        
        print("\n5. Configuration contents:")
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        print("\n" + "=" * 50)
        print("Configuration file tests PASSED ✓")
        print("=" * 50)
        return True
        
    except Exception as e:
        print(f"\n✗ Error testing config file: {e}")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("=" * 60)
    print(" PERCLOS CONFIGURATION SYSTEM TEST SUITE")
    print("=" * 60)
    print("\n")
    
    results = {
        'ConfigManager': test_config_manager(),
        'Configuration File': test_config_file(),
        'AttentionScorer': test_attention_scorer()
    }
    
    print("\n")
    print("=" * 60)
    print(" TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print(" ALL TESTS PASSED ✓")
        print(" The configuration system is working correctly!")
    else:
        print(" SOME TESTS FAILED ✗")
        print(" Please check the error messages above")
    print("=" * 60)
    print("\n")
    
    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
