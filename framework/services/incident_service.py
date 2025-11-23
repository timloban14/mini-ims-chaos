import time
# Import the class we just made.
# Format: from [folder].[folder].[filename] import [ClassName]
from framework.base.api_client import APIClient

# INHERITANCE: IncidentService extends APIClient
# Java equivalent: public class IncidentService extends APIClient {
class IncidentService(APIClient):
    
    def __init__(self, base_url):
        # SUPER: Call the parent constructor.
        # Java equivalent: super(base_url);
        super().__init__(base_url)
        
        # Define the specific endpoint for this service
        self.endpoint = "/incidents"

    def get_all_incidents(self):
        """
        Fetches list of incidents and returns a Python List of Dictionaries.

        Each dictionary contains keys such as:
            - 'id': int, unique identifier of the incident
            - 'timestamp': float, epoch time when the incident was created
            - ... (other relevant fields)
        """
        # We use 'self._get' which we defined in the parent class
        response = self._get(self.endpoint)
        
        # .json() deserializes the response body.
        # Java equivalent: gson.fromJson(response, List.class);
        return response.json()

    def get_latest_incident(self):
        """Helper to find the newest incident by ID"""
        data = self.get_all_incidents()
        
        # Guard clause: if list is empty, return None (null)
        if not data:
            return None
        
        # 1. THE MAX FUNCTION & LAMBDA
        # We want the object with the highest 'id'.
        # 'key=lambda x: x['id']' is an anonymous function.
        # Java Stream equivalent: data.stream().max(Comparator.comparingInt(x -> x.getId()));
        latest_record = max(data, key=lambda x: x['id'])
        
        return latest_record

    # TYPE HINTING: '-> float' tells the IDE this returns a decimal number.
    # Python doesn't enforce types, but this helps with auto-complete.
    def calculate_current_lag(self) -> float:
        """
        Calculates: (Current Time) - (Time the incident was created)
        """
        latest = self.get_latest_incident()
        
        if not latest:
            return 0.0
        
        # Extract timestamp from the JSON dictionary
        created_at = latest['timestamp']
        
        # Get current system time (Epoch seconds)
        now = time.time()
        
        # Return the difference
        return now - created_at