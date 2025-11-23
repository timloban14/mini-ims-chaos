# Mini-IMS: Resiliency Testing Framework

## Overview
A Proof-of-Concept (PoC) Incident Management System (IMS) designed to simulate high-scale ingestion bottlenecks and demonstrate "Thundering Herd" scenarios. 

This project implements a **Service Object Model (SOM)** in Python to validate system resiliency against SLA violations during traffic spikes.

## Architecture
**Producer (Agent)** $\rightarrow$ **Kafka (Buffer)** $\rightarrow$ **Consumer (Backend)** $\rightarrow$ **Redis (Store)**

* **Infrastructure:** Docker Compose (Kafka, Zookeeper, Redis).
* **Backend:** Python (Producer/Consumer with threading).
* **Automation:** Pytest + Requests (Service Object Model pattern).

## The Challenge (Simulated)
In a distributed architecture, if the Ingestion Agent (Producer) outpaces the Backend Processor (Consumer), the queue depth increases linearly. This results in **Consumer Lag**, causing a violation of the visibility SLA (e.g., Malware alerts appearing 10 minutes late).

## Capabilities
1.  **Traffic Generation:** Simulates a "Thundering Herd" of 100+ events per second.
2.  **Chaos Injection:** Simulates backend latency (I/O binding) to force queue buildup.
3.  **Black-Box Monitoring:** An automated test suite that calculates real-time lag.

## How to Run

### 1. Setup the Environment
Clone the repository and set up the Python virtual environment to isolate dependencies.

```bash
# 1. Clone the repository
git clone [https://github.com/](https://github.com/)<YOUR_GITHUB_USERNAME>/mini-ims-chaos.git
cd mini-ims-chaos

# 2. Create Virtual Environment
python3 -m venv venv

# 3. Activate Environment
source venv/bin/activate

# 4. Install Dependencies
pip install -r backend/requirements.txt
pip install pytest requests
```

### 2. Configure the Simulation
The behavior of the system (Chaos vs. Stable) is controlled by the threading timers in `backend/app.py`.

**Option A: Simulate "Thundering Herd" (The Interview Scenario)**
1.  Open `backend/app.py`.
2.  Set `generate_traffic()` sleep to **0.01** (Fast Producer).
3.  Set `ingest_data()` sleep to **0.5** (Slow Consumer).
4.  *Result:* The Producer outpaces the Consumer. Lag increases linearly. Tests will **FAIL**.

**Option B: Simulate "Stable State" (The Fix)**
1.  Open `backend/app.py`.
2.  Set `generate_traffic()` sleep to **1.0** (Throttled Producer).
3.  *Result:* The Consumer keeps up with the Producer. Lag stays near zero. Tests will **PASS**.

### 3. Start the Infrastructure
This spins up Kafka, Zookeeper, Redis, and the Python Backend.

```bash
docker-compose up --build -d
```
*> Note: Wait approx. 30 seconds for Kafka to fully initialize.*

### 4. Check the Dashboard (Manual Verification)
Open your browser to: [http://localhost:5001/incidents](http://localhost:5001/incidents)
* You should see JSON data populating.
* Refresh the page to see new incidents arriving.

### 5. Run the Automated Resiliency Suite
Execute the Pytest suite to verify if the system is meeting its SLAs.

```bash
# Run with -s to see stdout (logs) and -v for verbose output
pytest -s -v tests/test_resiliency.py
```

### 6. Teardown & Cleanup
To stop the containers and **wipe the Redis database** (essential to reset lag calculations for the next run):

```bash
docker-compose down
```

---

## The Test Strategy (Service Object Model)
The framework uses a **Service Object Model** pattern located in `framework/` to abstract the API details.

1.  **Test Logic (`tests/test_resiliency.py`)**: Defines the Business Rule.
    * *Rule:* "Data must appear in the dashboard within 5 seconds of creation."
2.  **Service Layer (`framework/services/incident_service.py`)**: Handles the Domain Logic.
    * *Action:* Queries API, finds the latest ID, calculates `now() - created_at`.
3.  **Base Layer (`framework/base/api_client.py`)**: Handles HTTP transport.
    * *Action:* Manages Sessions, Base URLs, and Exception Handling.

---

## Project Structure
```text
mini-ims-chaos/
├── backend/                
│   ├── app.py              # The "Brains": Traffic Generator + Ingestion + API
│   ├── Dockerfile          # Container definition
│   └── requirements.txt    # Backend dependencies
├── framework/              # Automation Library
│   ├── base/               # Base API Client (Requests wrapper)
│   └── services/           # Service Objects (Incident domain logic)
├── tests/                  # Pytest Suites
├── docker-compose.yml      # Infrastructure (Kafka, Redis, Zookeeper)
├── conftest.py             # Pytest configuration (Root anchor)
└── README.md               # Documentation
```