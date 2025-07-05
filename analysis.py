import pandas as pd
from datetime import datetime

# variables
CSV_FILE = 'mock_transactions_final.csv'
ACCOUNT = 'ZignalyX120'
CUTOFF_TIME = '2025-01-30 08:42:00'

# Loading data into dataframe 
df = pd.read_csv(CSV_FILE)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# clearing data to only get ones before specified timeframe 
df = df[df['timestamp'] <= pd.to_datetime(CUTOFF_TIME)]

# Focus only on rows where the account is either the sender or receiver
df = df[(df['from'] == ACCOUNT) | (df['to'] == ACCOUNT)].copy()

# Determine direction of transaction
def get_effect(row):
    if row['to'] == ACCOUNT:
        return float(row['amount'])  # Money came in
    elif row['from'] == ACCOUNT:
        return -float(row['amount'])  # Money went out
    return 0

# calling get_effect function 
df['effect'] = df.apply(get_effect, axis=1)

# Calculate balance
balance = df['effect'].sum()

# Total by type
type_summary = df.groupby('type')['effect'].sum()

# Output
print(f"\nAccount: {ACCOUNT}")
print(f"Up to: {CUTOFF_TIME}\n")
print("Totals by Transaction Type:")
for tx_type, total in type_summary.items():
    print(f" - {tx_type}: {'+' if total >= 0 else ''}{total:.2f}")

print(f"\nFinal Balance: {balance:.2f}")
