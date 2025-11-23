import pytest
from framework.services.incident_service import IncidentService

# CONSTANTS
BASE_URL = "http://localhost:5001"
SLA_THRESHOLD_SECONDS = 5.0

# 1. FIXTURES (Dependency Injection)
# A fixture is a setup function. 
# pytest will run this BEFORE the test and pass the return value into the test.
# Java equivalent: @BeforeMethod that initializes the service.
@pytest.fixture
def incident_service():
    service = IncidentService(BASE_URL)
    return service

# 2. THE TEST FUNCTION
# Notice we pass 'incident_service' as an argument. 
# Pytest looks for a fixture with that name and injects it automatically.
def test_thundering_herd_lag(incident_service):
    """
    Scenario: Verify Consumer Lag stays within SLA.
    """
    print("\n⚡ STARTING: Thundering Herd Resiliency Test")
    
    # Call the business logic method
    current_lag = incident_service.calculate_current_lag()
    
    print(f"📊 REPORTED LAG: {current_lag:.2f} seconds")

    # 3. ASSERTIONS
    # Python doesn't need Assert.assertEquals(). 
    # You just use the keyword 'assert'.
    # If the statement is False, the test fails.
    # The string after the comma is the error message printed on failure.
    assert current_lag < SLA_THRESHOLD_SECONDS, \
        f"SLA Violation! Lag {current_lag}s is greater than {SLA_THRESHOLD_SECONDS}s"