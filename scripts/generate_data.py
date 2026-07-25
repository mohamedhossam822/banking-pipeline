"""
Generates synthetic banking transaction data with intentional
duplicates and updates
"""

import csv
import random
import os 
from pathlib import Path
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)

OUTPUT_DIR = Path(__file__).resolve().parent / "data"
print(f"OUTPUT_DIR: {OUTPUT_DIR}")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ── Config ────────────────────────────────────────────────────────────────────
NUM_CUSTOMERS   = 200
NUM_TRANSACTIONS = 1000
SNAPSHOT_DATE   = datetime.today().strftime("%Y-%m-%d")

TRANSACTION_TYPES = ["CREDIT", "DEBIT", "TRANSFER", "FEE", "INTEREST"]
ACCOUNT_TYPES     = ["CURRENT", "SAVINGS", "LOAN", "FIXED_DEPOSIT"]


# ── 1. Generate customers ─────────────────────────────────────────────────────
def generate_customers(n: int) -> list[dict]:
    customers = []
    for i in range(1, n + 1):
        customers.append({
            "customer_id":    f"CUST{i:05d}",
            "full_name":      fake.name(),
            "email":          fake.email(),
            "phone":          fake.phone_number()[:20],
            "country":        random.choice(["EG", "SA", "AE", "KW", "BH"]),
            "account_type":   random.choice(ACCOUNT_TYPES),
            "credit_score":   random.randint(300, 850),
            "is_active":      random.choice([True, True, True, False]),   # 75% active
            "snapshot_date":  SNAPSHOT_DATE,
        })
    return customers


# ── 2. Inject updates (simulates SCD Type 2 changes) ─────────────────────────
def inject_customer_updates(customers: list[dict]) -> list[dict]:
    """
    Take 10% of customers and create a new snapshot row with changed data.
    This is the pattern you handled in your snapshot unification work —
    detecting what changed and deciding which record is current.
    """
    updated = []
    for c in customers:
        updated.append(c)
        if random.random() < 0.10:                      # 10% get an update
            new_row = c.copy()
            new_row["email"]         = fake.email()     # email changed
            new_row["credit_score"]  = min(850, c["credit_score"] + random.randint(-50, 80))
            new_row["snapshot_date"] = SNAPSHOT_DATE    # same snapshot, newer record
            updated.append(new_row)
    return updated


# ── 3. Generate transactions ──────────────────────────────────────────────────
def generate_transactions(customers: list[dict], n: int) -> list[dict]:
    # Use only base customers (no duplicates from updates)
    base_customers = [c for c in customers if c["customer_id"] == customers[customers.index(c)]["customer_id"]]
    unique_ids     = list({c["customer_id"] for c in customers})

    transactions = []
    base_date    = datetime.today() - timedelta(days=30)

    for i in range(1, n + 1):
        txn_date = base_date + timedelta(
            days=random.randint(0, 29),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
        transactions.append({
            "transaction_id":   f"TXN{i:08d}",
            "customer_id":      random.choice(unique_ids),
            "transaction_date": txn_date.strftime("%Y-%m-%d %H:%M:%S"),
            "amount":           round(random.uniform(5.0, 50000.0), 2),
            "currency":         random.choice(["EGP", "USD", "SAR", "AED"]),
            "transaction_type": random.choice(TRANSACTION_TYPES),
            "status":           random.choice(["COMPLETED", "COMPLETED", "COMPLETED", "PENDING", "FAILED"]),
            "branch_code":      f"BR{random.randint(1, 50):03d}",
            "description":      fake.sentence(nb_words=5),
        })

    return transactions


# ── 4. Inject duplicates (simulates real ingestion issues) ────────────────────
def inject_duplicates(transactions: list[dict], rate: float = 0.03) -> list[dict]:
    """
    Inject ~3% duplicate records — a common real-world pipeline problem.
    Your reconciliation pipeline needs to detect and deduplicate these.
    """
    dupes = random.sample(transactions, k=int(len(transactions) * rate))
    all_records = transactions + dupes
    random.shuffle(all_records)
    return all_records


# ── 5. Write CSVs ─────────────────────────────────────────────────────────────
def write_csv(records: list[dict], filename: str) -> str:
    path = os.path.join(OUTPUT_DIR, filename)
    if not records:
        return path
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)
    return path


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"[generate_data] Snapshot date: {SNAPSHOT_DATE}")

    # Customers
    customers     = generate_customers(NUM_CUSTOMERS)
    customers_scd = inject_customer_updates(customers)
    cust_path     = write_csv(customers_scd, "customers_raw.csv")
    print(f"[generate_data] Customers written: {len(customers_scd)} rows → {cust_path}")

    # Transactions
    transactions      = generate_transactions(customers, NUM_TRANSACTIONS)
    transactions_dupl = inject_duplicates(transactions)
    txn_path          = write_csv(transactions_dupl, "transactions_raw.csv")
    print(f"[generate_data] Transactions written: {len(transactions_dupl)} rows → {txn_path}")

    return {
        "customers_path":    cust_path,
        "transactions_path": txn_path,
        "snapshot_date":     SNAPSHOT_DATE,
    }


if __name__ == "__main__":
    result = main()
    print(f"\n[generate_data] Done: {result}")