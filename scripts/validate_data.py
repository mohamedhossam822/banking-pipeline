import os
from pathlib import Path

from dotenv import load_dotenv
import psycopg
import pandas as pd
load_dotenv()



HERE = Path(__file__).resolve().parent
print(f"HERE: {HERE}")
DATA_DIR = HERE / Path(os.environ.get("DATA_DIR",  "data"))
CUSTOMERS_CSV = DATA_DIR / Path(os.environ.get("CUSTOMERS_CSV",  "customers_raw.csv"))
TRANSACTIONS_CSV = DATA_DIR / Path(os.environ.get("TRANSACTIONS_CSV", "transactions_raw.csv"))

CLEAN_CUSTOMERS_CSV = DATA_DIR / Path(os.environ.get("CLEAN_CUSTOMERS_CSV", "clean_customers_raw.csv"))
CLEAN_TRANSACTIONS_CSV = DATA_DIR / Path(os.environ.get("CLEAN_TRANSACTIONS_CSV", "clean_transactions_raw.csv"))

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


def read_data(csv_path: Path, columns: list[str]) -> pd.DataFrame:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    df=pd.read_csv(csv_path, usecols=columns)

    return df

def clean_customers_data(df: pd.DataFrame) -> pd.DataFrame:
    # Remove duplicates based on customer_id and snapshot_date, keeping the latest record
    df = df.sort_values(by=["customer_id", "snapshot_date"], ascending=[True, False])
    df = df.drop_duplicates(subset=["customer_id", "snapshot_date"], keep="first")

    # Ensure correct data types
    df["credit_score"] = pd.to_numeric(df["credit_score"], errors="coerce")
    df["is_active"] = df["is_active"].astype(bool)
    df["snapshot_date"] = pd.to_datetime(df["snapshot_date"], errors="coerce").dt.date

    return df

def clean_transactions_data(df: pd.DataFrame) -> pd.DataFrame:
    # Remove duplicates based on transaction_id, keeping the latest record
    df = df.sort_values(by=["transaction_id", "transaction_date"], ascending=[True, False])
    df = df.drop_duplicates(subset=["transaction_id"], keep="first")

    # Ensure correct data types
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")

    #ensure that customer_id in transactions exists in customers
    df = df[df["customer_id"].isin(df["customer_id"])]

    return df


def main() -> None:
    print(f"DATA_DIR: {DATA_DIR}")
    print(f"CUSTOMERS_CSV: {CUSTOMERS_CSV}")
    print(f"TRANSACTIONS_CSV: {TRANSACTIONS_CSV}")
    df=read_data(CUSTOMERS_CSV, CUSTOMERS_COLUMNS)
    df=clean_customers_data(df)
    df.to_csv(CLEAN_CUSTOMERS_CSV, index=False)

    df=read_data(TRANSACTIONS_CSV, TRANSACTIONS_COLUMNS)
    df=clean_transactions_data(df)
    df.to_csv(CLEAN_TRANSACTIONS_CSV, index=False)

    print(df.head())
    print("Loaded customers_raw and transactions_raw from CSV into the database.")


if __name__ == "__main__":
    main()
