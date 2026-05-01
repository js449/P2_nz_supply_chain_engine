# NZ Supply Chain Resilience Engine 🚛🇳🇿

Project Overview
This is a professional-grade Data Engineering pipeline designed to monitor New Zealand Transport Agency (NZTA) road events and quantify their economic impact on supply chains. It demonstrates a full Medallion Architecture using modern data stack tools.

Core Architecture
Data Contract (The Firewall): Uses Pydantic to validate incoming JSON data against a strict schema.

Bronze Layer: Raw ingestion with SQL Window Functions for deduplication.

Silver Layer: Transformation of raw data into standardized "Fact" tables with urgency labels.

Gold Layer: Business-ready reporting calculating Delay Hours and Economic Impact ($).

Orchestration: Automated via a custom Python wrapper that manages task dependencies and error handling.

The Tech Stack
Python: Core logic and data validation.

dbt: Data transformation, testing, and documentation.

Docker: Containerized Postgres database environment.

Postgres: Reliable data warehouse storage.

How to Run
Start the Database:

PowerShell
docker-compose up -d
Install Dependencies:

PowerShell
pip install -r requirements.txt
Execute the Pipeline:

PowerShell
python run_pipeline.py
Monitoring & Visibility
Testing: 4 automated data quality tests ensure uniqueness and non-null values in the reporting layer.

Lineage: View the full data flow by running dbt docs generate and dbt docs serve.
