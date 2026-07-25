import os
from pathlib import Path

from dotenv import load_dotenv
import psycopg

load_dotenv()

DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
print({
    "DB_NAME": DB_NAME,
    "DB_USER": DB_USER,
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
})
clean_customers_csv = os.environ.get("CLEAN_CUSTOMERS_CSV", "clean_customers_raw.csv")
clean_transactions_csv = os.environ.get("CLEAN_TRANSACTIONS_CSV", "clean_transactions_raw.csv")
data_dir = os.environ.get("DATA_DIR", "data")

if not DB_NAME or not DB_USER or not DB_PASSWORD:
    raise RuntimeError("Missing required database configuration in .env")

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / data_dir
CUSTOMERS_CSV =  DATA_DIR / clean_customers_csv
TRANSACTIONS_CSV = DATA_DIR / clean_transactions_csv

CREATE_CUSTOMERS_TABLE = """
CREATE TABLE IF NOT EXISTS customers_raw (
    customer_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    country TEXT,
    account_type TEXT,
    credit_score INT,
    is_active BOOLEAN,
    snapshot_date DATE
);
"""

CREATE_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS transactions_raw (
    transaction_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    transaction_date TIMESTAMP,
    amount NUMERIC(12, 2),
    currency TEXT,
    transaction_type TEXT,
    status TEXT,
    branch_code TEXT,
    description TEXT,
    CONSTRAINT fk_customer FOREIGN KEY(customer_id) REFERENCES customers_raw(customer_id)
);
"""

CUSTOMERS_COLUMNS = [
    "customer_id",
    "full_name",
    "email",
    "phone",
    "country",
    "account_type",
    "credit_score",
    "is_active",
    "snapshot_date",
]

TRANSACTIONS_COLUMNS = [
    "transaction_id",
    "customer_id",
    "transaction_date",
    "amount",
    "currency",
    "transaction_type",
    "status",
    "branch_code",
    "description",
]


def load_csv_into_table(cur: psycopg.Cursor, table: str, columns: list[str], csv_path: Path) -> None:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    columns_sql = ", ".join(columns)
    copy_sql = f"COPY {table} ({columns_sql}) FROM STDIN WITH CSV HEADER"
    


    with cur.copy(copy_sql) as copy:
        with open(csv_path, "r", encoding="utf-8") as f:
            for line in f:
                copy.write(line)


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with psycopg.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_CUSTOMERS_TABLE)
            cur.execute(CREATE_TRANSACTIONS_TABLE)
            cur.execute("TRUNCATE TABLE transactions_raw, customers_raw")
            load_csv_into_table(cur, "customers_raw", CUSTOMERS_COLUMNS, CUSTOMERS_CSV)
            load_csv_into_table(cur, "transactions_raw", TRANSACTIONS_COLUMNS, TRANSACTIONS_CSV)
            conn.commit()



if __name__ == "__main__":
    main()
