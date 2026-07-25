# Banking Data Pipeline

An end-to-end banking data engineering project that simulates a real analytics workflow using **Python, PostgreSQL, Apache Airflow, dbt, and Docker**.

The project generates synthetic banking data, validates it, loads it into a database, and transforms it into analytics-ready models. It is designed to demonstrate production-style data engineering practices, including orchestration, modular SQL modeling, testing, and containerized local development.

## Project Highlights

* Synthetic banking data generation with Python
* Automated data loading into PostgreSQL
* Pre-load data validation checks
* Workflow orchestration with Apache Airflow
* dbt-based transformation layer with staging, intermediate, and mart models
* Reusable SQL logic through dbt macros
* Data quality testing and documentation
* Dockerized setup for reproducible local development

## Why This Project

This project was built to showcase practical data engineering skills in a realistic banking context. It focuses on the full lifecycle of a pipeline:

1. Create data
2. Validate it
3. Load it
4. Orchestrate the process
5. Transform it with dbt
6. Test and document the final output

It is suitable for demonstrating skills relevant to data engineering, analytics engineering, and modern ELT workflows.

## Architecture

The pipeline follows a simple layered flow:

```text
Synthetic Data
    ↓
Python Scripts
    ↓
PostgreSQL Database
    ↓
Airflow Orchestration
    ↓
dbt Transformations
    ↓
Analytics-Ready Tables
```

### Layer Breakdown

* **Python scripts** generate and validate banking data.
* **PostgreSQL** stores the raw and transformed datasets.
* **Airflow** schedules and orchestrates the workflow.
* **dbt** handles SQL transformations and testing.
* **Docker** makes the environment portable and easy to run locally.

## Repository Structure

```text
banking_models/
├── analyses/
├── macros/
├── models/
│   └── example/
├── seeds/
├── snapshots/
├── tests/
├── dbt_project.yml
├── README.md
└── .gitignore

config/
dags/
data/
logs/
plugins/
scripts/
├── data/
├── generate_data.py
├── Load_Into_Database.py
└── validate_data.py

.env
docker-compose.yaml
Dockerfile
requirements.txt
```

## Project Structure Notes

### `banking_models/`

Contains the dbt project.

* `models/` — SQL transformation models
* `macros/` — reusable SQL logic
* `tests/` — custom SQL tests
* `seeds/` — CSV reference data
* `snapshots/` — historical record tracking
* `analyses/` — ad hoc analytical queries

### `dags/`

Apache Airflow DAGs for running the pipeline in order.

### `scripts/`

Python scripts for data generation, validation, and database loading.

### `data/`

Input, sample, or generated data files used by the project.

### `logs/`

Runtime logs. This folder should usually be ignored by Git.

## Tech Stack

* **Python**
* **PostgreSQL**
* **Apache Airflow**
* **dbt**
* **Docker**
* **Docker Compose**

## Setup Instructions

### Prerequisites

Make sure the following are installed:

* Docker
* Docker Compose
* Python 3.10+ or later
* dbt
* Git

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/banking-data-pipeline.git
cd banking-data-pipeline
```

### 2. Create your environment file

Create a `.env` file in the project root and define your local configuration.

Example:

```env
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=banking
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
AIRFLOW_UID=50000
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Build and start the services

```bash
docker compose up --build
```

This will start the services defined in `docker-compose.yaml`, including the database and orchestration components.

## Running the Pipeline

### 1. Generate data

```bash
python scripts/generate_data.py
```

### 2. Validate data

```bash
python scripts/validate_data.py
```

### 3. Load data into the database

```bash
python scripts/Load_Into_Database.py
```

### 4. Run dbt transformations

From داخل the `banking_models/` directory:

```bash
dbt run
```

### 5. Run tests

```bash
dbt test
```

### 6. Generate documentation

```bash
dbt docs generate
dbt docs serve
```

## dbt Model Layers

The dbt project is intended to follow a clear layered structure:

* **Staging models** clean and standardize source data
* **Intermediate models** apply business logic and combine datasets
* **Mart models** create final reporting tables for analytics and BI

A common naming pattern is:

* `stg_*` for staging
* `int_*` for intermediate
* `fact_*` and `dim_*` for marts

## Testing and Data Quality

The project includes multiple layers of validation:

* Python-level validation before loading data
* dbt schema tests
* Custom SQL tests
* Snapshot-based history tracking

Typical checks include:

* required fields are present
* null values are handled correctly
* numeric values fall within expected ranges
* duplicate records are identified
* historical changes are captured properly

## Future Improvements

Possible enhancements include:

* expanding the banking domain logic
* adding more realistic edge cases
* improving dbt documentation and lineage
* adding CI/CD with GitHub Actions
* adding unit tests for Python scripts
* creating dashboard visualizations on top of the mart layer


## License

This project is intended for educational and portfolio use.

---
