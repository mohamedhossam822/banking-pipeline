
# Banking Data Pipeline

![CI](https://github.com/mohamedhossam822/banking-pipeline/actions/workflows/ci.yml/badge.svg)

An end-to-end banking data engineering project that simulates a real analytics workflow using **Python, PostgreSQL, Apache Airflow, dbt, Docker, and GitHub Actions CI**.

The project generates synthetic banking data, validates it, loads it into a database, and transforms it into analytics-ready models — orchestrated by Airflow and continuously tested via CI on every push.

## Project Highlights

* Synthetic banking data generation with Python (Faker)
* Automated schema and referential-integrity validation before load
* Bulk-loading into PostgreSQL via `COPY FROM STDIN`
* Workflow orchestration with Apache Airflow (CeleryExecutor)
* dbt-based transformation layer with staging, snapshot (SCD Type 2), and mart models
* Automated data quality tests (`not_null`, `unique`, `relationships`) run via `dbt build`
* **Continuous Integration with GitHub Actions** — every push spins up a real Postgres service, runs the full pipeline end-to-end, and fails the build if data quality or dbt tests fail
* Dockerized setup for reproducible local development

## Why This Project

This project was built to demonstrate practical, production-style data engineering skills in a realistic banking context — not just a script that runs once locally, but a pipeline that is orchestrated, tested, and continuously validated on every change.

1. Generate synthetic banking data
2. Validate schema and referential integrity
3. Load into PostgreSQL
4. Orchestrate the full flow with Airflow
5. Transform with dbt (staging → SCD2 snapshot → marts)
6. Test data quality automatically
7. **Validate the entire pipeline automatically via CI on every push**

## Architecture

```text
Synthetic Data (Faker)
    ↓
Python Scripts (generate → validate → load)
    ↓
PostgreSQL (raw tables, FK-constrained)
    ↓
Airflow Orchestration (DAG: generate → validate → load → dbt build)
    ↓
dbt Transformations
    ├── staging   (cleaned, typed models)
    ├── snapshots (SCD Type 2 customer history via dbt snapshot)
    └── marts     (dim_customers, fct_daily_balances)
    ↓
Analytics-Ready Tables + dbt Tests + dbt Docs
    ↓
GitHub Actions CI (runs the full pipeline on every push)
```

### Layer Breakdown

* **Python scripts** generate synthetic data, validate schema/referential integrity, and bulk-load into Postgres.
* **PostgreSQL** stores raw and transformed datasets, with FK constraints enforcing integrity between customers and transactions.
* **Airflow** schedules and orchestrates the full pipeline as a single DAG.
* **dbt** handles SQL transformations, SCD Type 2 history tracking, and automated data quality tests.
* **Docker / Docker Compose** makes the environment portable and reproducible locally.
* **GitHub Actions** runs the entire pipeline (generate → validate → load → `dbt build`) against a real Postgres service on every push and pull request, catching breakages before they reach `main`.

## Repository Structure

```text
.github/
└── workflows/
    └── ci.yml               ← CI pipeline definition

banking_models/
├── models/
│   ├── staging/
│   │   └── stg_transactions.sql
│   └── marts/
│       ├── dim_customers.sql
│       └── fct_daily_balances.sql
├── snapshots/
│   └── customers_snapshot.yml    ← SCD Type 2 via dbt snapshot
├── tests/                        ← schema tests (not_null, unique, relationships)
├── macros/
├── seeds/
├── analyses/
├── dbt_project.yml
└── profiles.yml

config/
dags/
├── banking_pipeline_dag.py
data/
logs/
plugins/
scripts/
├── generate_data.py
├── validate_data.py
└── load_into_database.py

.env.example
docker-compose.yaml
Dockerfile
requirements.txt
```

## Tech Stack

* **Python** (Faker, pandas, psycopg)
* **PostgreSQL**
* **Apache Airflow** (CeleryExecutor)
* **dbt** (staging, snapshots, marts, tests)
* **Docker / Docker Compose**
* **GitHub Actions (CI/CD)**

## Setup Instructions

### Prerequisites

* Docker & Docker Compose
* Python 3.10+
* dbt
* Git

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/banking-data-pipeline.git
cd banking-data-pipeline
```

### 2. Create your environment file

```bash
cp .env.example .env
# fill in POSTGRES_*, AIRFLOW_UID, FERNET_KEY, etc.
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Build and start the services

```bash
docker compose up --build
```

## Running the Pipeline

### Locally (manual)

```bash
python scripts/generate_data.py
python scripts/validate_data.py
python scripts/load_into_database.py

cd banking_models
dbt build          # runs models + snapshots + tests in one command
dbt docs generate
dbt docs serve
```

### Via Airflow

Trigger the `banking_pipeline_dag` DAG from the Airflow UI (`localhost:8080`). It runs the same four steps in order: `generate_data → validate_data → load_into_database → build_dbt_models`.

### Via CI (automatic)

Every push to `main` (and every pull request) triggers `.github/workflows/ci.yml`, which:

1. Spins up a real PostgreSQL 16 service container
2. Installs dependencies from `requirements.txt`
3. Runs `generate_data.py → validate_data.py → load_into_database.py`
4. Runs `dbt build` (models + snapshots + tests) against that Postgres instance
5. Generates and uploads dbt docs as a build artifact
6. Fails the build if any step — including a dbt test — fails

This means every change to the pipeline is validated end-to-end before merging, the same way it would be in a real data engineering team.

## dbt Model Layers

* **Staging** (`stg_*`) — cleaned, typed source data
* **Snapshots** — SCD Type 2 history tracking via dbt's native `snapshot` feature (`check` strategy on `customers_raw`)
* **Marts** (`dim_*`, `fct_*`) — final reporting tables, including a daily running-balance fact table built with window functions

## Testing and Data Quality

* Python-level validation before loading (schema + referential integrity checks)
* dbt schema tests: `unique`, `not_null`, `relationships` across staging and mart models
* SCD Type 2 history captured automatically via dbt snapshot
* **CI enforcement**: all of the above run automatically on every push — a failing test blocks the pipeline the same way it would in production

## Future Improvements

* Expand dbt test coverage (e.g. `accepted_values`, custom singular tests)
* Add pytest unit tests for the Python scripts
* Add a lightweight BI layer (e.g. Metabase) on top of the mart models
* Migrate one ingestion path to cloud storage (Azure Blob) as a stepping stone toward cloud-native orchestration

## License

This project is intended for educational and portfolio use.
