import requests

class APIClient:
    """
    The Base Client.
    JAVA EQUIVALENT: AbstractBaseService or BasePage.
    """

    # 1. THE CONSTRUCTOR
    # In Python, '__init__' is the constructor.
    # 'self' is exactly the same as 'this' in Java. You must pass it as the first argument.
    def __init__(self, base_url):
        # We store the base_url in the instance (this.base_url = base_url)
        self.base_url = base_url
        
        # 2. SESSIONS
        # requests.Session() creates a "stateful" browser-like object.
        # It keeps the connection open (Keep-Alive) for speed and stores cookies.
        self.session = requests.Session() 

    # 3. INTERNAL GET WRAPPER
    # The underscore prefix '_get' is a hint to other devs: "This is private/protected".
    # It's not enforced by the compiler (Python is permissive), but it's a strong convention.
    def _get(self, endpoint):
        # 4. F-STRINGS
        # f"..." is String Interpolation. 
        # Java equivalent: String.format("%s%s", this.base_url, endpoint);
        url = f"{self.base_url}{endpoint}"
        
        print(f"📡 GET: {url}") # Logging helper
        
        try:
            # Perform the actual call
            response = self.session.get(url)
            
            # 5. ERROR HANDLING
            # In Java, you might check if(response.code != 200).
            # 'raise_for_status()' automatically throws an Exception if status is 4xx or 5xx.
            response.raise_for_status()
            
            return response
            
        except requests.exceptions.RequestException as e:
            # Capture any connection error (DNS, Timeout, Refused)
            print(f"❌ API Failure: {e}")
            # Re-throw it so the test fails
            raise

    # 6. INTERNAL POST WRAPPER
    def _post(self, endpoint, payload):
        url = f"{self.base_url}{endpoint}"
        # json=payload automatically converts your Python Dictionary to a JSON string
        # and sets Content-Type: application/json
        return self.session.post(url, json=payload)