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

### 1. Start Infrastructure
```bash
docker-compose up --build -d