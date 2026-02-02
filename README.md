📊 Customer Support Analytics Project

Author: Ashish Ranjan
Tech Stack: Python, Pandas, PostgreSQL, SQL, Git
Project Type: Data Cleaning, Analysis & Reporting

📌 Project Overview
This project focuses on cleaning, validating, analyzing, and reporting customer support data stored in a PostgreSQL database.
The goal is to transform raw customer interaction data into business-ready insights such as customer satisfaction trends, top issues, and call center performance.
The project follows a modular, production-style pipeline:
Clean data once
Validate data quality
Generate reusable analytical reports
Export insights for business users (CSV / Excel)

📂 Project Structure

<img width="768" height="604" alt="image" src="https://github.com/user-attachments/assets/84ad45c3-190f-45fe-bf43-a0dba896cee8" />


🔄 Data Pipeline Flow
Ingest raw CSV data into PostgreSQL
Clean data (standardize, deduplicate, normalize)
Validate data quality (nulls, duplicates, schema checks)
Analyze data to generate business insights
Export reports as CSV files

🧹 Data Cleaning (clean.py)
What this module does
Standardizes column names
Removes fully empty rows and columns
Removes duplicate records
Normalizes text values ("NA", "null", "none" → missing)
Safely converts numeric values
Keeps raw intent intact (no aggressive deletion)

Why this matters
Clean data ensures analysis is accurate, consistent, and reliable without losing important records.

✅ Data Quality Checks (db_checks.py)
Checks performed
Row & column count validation
Duplicate record detection
Missing value percentage per column
Schema-level sanity checks

Purpose
Ensures data integrity before running analysis or reports.

📊 Analysis & Reporting (analysis.py)
This module generates business-ready reports from cleaned data.

Reports Generated
1️⃣ KPI Summary
Total rows & columns
Average & median CSAT
Call duration statistics
Response time metrics

2️⃣ Top Customer Issues
Most frequent customer contact reasons

3️⃣ Sentiment Distribution
Positive / Negative / Neutral sentiment breakdown

4️⃣ CSAT by State
Regional customer satisfaction performance

5️⃣ CSAT by State, Channel & Sentiment
Headline:
CSAT Breakdown by State, Channel & Sentiment
Identifies high-impact dissatisfaction areas
Helps prioritize operational improvements

6️⃣ CSAT by Channel & Call Center
Headline:
CSAT Performance by Channel and Call Center
Compares call center effectiveness
Highlights underperforming operations

📈 Key Business Takeaways
Customer dissatisfaction is concentrated in high-volume states
Call-Center and Chatbot channels drive most negative sentiment
High ticket volume does not always mean high satisfaction
Improving a few key call centers can significantly raise overall CSAT

🛠️ Technologies Used
Tool	Purpose
Python	Core programming
Pandas	Data manipulation & analysis
PostgreSQL	Data storage
SQL	Data querying
Git	Version control

▶️ How to Run the Project
Set up PostgreSQL and update db_connection.py
Ingest data:
python ingest_csv.py
Run data quality checks:
python db_checks.py
Generate reports:
python analysis.py
View results in the reports-5/ folder

🎯 Design Principles Followed
Defensive coding (schema checks, safe conversions)
Separation of concerns (cleaning ≠ analysis)
Business-first metrics
Scalable & maintainable structure
