# odoo-analytics-pipeline

An end-to-end automated ETL pipeline to extract CRM and Sales data from **Odoo 19**, transform it using **Python**, and load it into **PostgreSQL** for real-time visualization in **Apache Superset**.

## 🛠️ Project Workflow
The pipeline is designed to handle operational data and convert it into analytical insights through three main stages:

### 1. Extract
* Connectivity with Odoo's PostgreSQL database.
* Automated retrieval of CRM Leads, Opportunities, and Stages.

### 2. Transform (The Logic)
* **JSONB Handling:** Flattening Odoo's multi-language dictionaries (JSONB) into clean text.
* **Data Cleaning:** Removing null values and normalizing data types using Pandas.
* **Metric Calculation:** Generation of Weighted Revenue ($Expected \ Revenue \times Probability$).

### 3. Load
* Synchronizing data into a dedicated analytical schema (`odoo_analytics_dw`).
* Ensuring data availability for BI tools without impacting ERP performance.

---

## 💻 Tech Stack
* **ERP System:** Odoo 19 (Community)
* **Database:** PostgreSQL 18
* **Engine:** Python 3.12 (Pandas, SQLAlchemy)
* **BI Tool:** Apache Superset

---

## 🚀 Getting Started

### Prerequisites
Ensure you have the following Python libraries installed:
```bash
pip install pandas sqlalchemy psycopg2-binary
```
# Database Setup
Create the target schema in your PostgreSQL:

```bash
CREATE SCHEMA odoo_analytics_dw;
```
# Run the Pipeline
Update the credentials in odoo_etl.py and execute:

```bash
python odoo_etl.py
```
