import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modules.configuration.service import ConfigurationService
from src.modules.ncc.regulatory_officer_workflow.advisory_service import AdvisoryService
from src.modules.ncc.financial_sustainability.services import calculate_aol, AOLInput

def test_dynamic_config():
    print("--- Testing Configuration Service ---")
    config_service = ConfigurationService()
    
    # Test 1: Fetch Rules
    rule = config_service.get_rule_for_metric("NCC", "DropCallRate")
    print(f"Fetch 'DropCallRate': {rule.threshold if rule else 'None'} (Expected: 1.0)")
    assert rule.threshold == 1.0

    # Test 2: Advisory Service Logic
    print("\n--- Testing Advisory Service Refactor ---")
    advisory = AdvisoryService(config_service)
    
    # Case A: Value 1.5 > 1.0 (Breach)
    result_breach = advisory.process_qos_event("DropCallRate", 1.5)
    print(f"Event (1.5%): {result_breach['status']}")
    assert result_breach['status'] == "breach_alerted"

    # Case B: Value 0.5 < 1.0 (OK)
    result_ok = advisory.process_qos_event("DropCallRate", 0.5)
    print(f"Event (0.5%): {result_ok['status']}")
    assert result_ok['status'] == "ok"

    # Test 3: Financial Service Refactor
    print("\n--- Testing AOL Calculation Refactor ---")
    # Fetch param
    levy_percent = config_service.get_fiscal_parameter("NCC", "AOL_LEVY_PERCENT")
    print(f"Fetch AOL Levy %: {levy_percent} (Expected: 0.01)")
    
    input_data = AOLInput(gross_revenue=1000, interconnect_costs=100, roaming_costs=0)
    # (1000 - 100) * 0.01 = 9.0
    result = calculate_aol(input_data, levy_percent)
    print(f"Calculated Levy: {result.levy_payable} (Expected: 9.0)")
    assert result.levy_payable == 9.0

    print("\n✅ All Dynamic Config Tests Passed!")

if __name__ == "__main__":
    test_dynamic_config()
