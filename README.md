# odoo-analytics-pipeline

An end-to-end automated ETL pipeline to extract CRM and Sales data from **Odoo 19**, transform it using **Python**, and load it into **PostgreSQL** for real-time visualization in **Apache Superset**.


##🏗️ Odoo ERP Setup & Data Entry
The journey started by configuring Odoo 19 to generate the source data:

* Product Management: Created master data for products (e.g., Laptops,..) with defined costs and sales prices.

* CRM Workflow: Simulated a real-world sales cycle by creating opportunities (e.g., Ahmed Ali's opportunity).

* Pipeline Stages: Organized leads into stages: New -> Qualified -> Laptop Inquiry -> Won.

* Database: Odoo stores this operational data in its internal PostgreSQL tables.

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
* **Source:** Odoo 19 ERP System (Community Edition)
* **Database:** PostgreSQL 18
* **Engine:** Python 3.12 (Pandas, SQLAlchemy)
* **BI Tool:** Apache Superset

---

## 🚀 Getting Started

### Environment Setup
Install the necessary Python libraries::
```bash
pip install pandas sqlalchemy psycopg2-binary
```
# Database Setup
Create the dedicated analytical schema in your PostgreSQL instance:

```bash
CREATE SCHEMA odoo_analytics_dw;
```
# Run the Pipeline
Update the credentials in odoo_etl.py and execute:

```bash
python odoo_etl.py
```
# BI Connection
* Open Apache Superset.

* Connect to the odoo database.

* Select the odoo_analytics_dw schema and the tables to start building charts.
