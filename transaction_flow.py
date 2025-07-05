import pandas as pd
from datetime import datetime

# variables
CSV_FILE = 'mock_transactions_final.csv'
ACCOUNT = 'ZignalyX120'
CUTOFF_TIME = '2025-01-30 08:42:00'

# Load data
df = pd.read_csv(CSV_FILE)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Filter by timestamp
df = df[df['timestamp'] <= pd.to_datetime(CUTOFF_TIME)]

# Filter for relevant transactions
df = df[(df['from'] == ACCOUNT) | (df['to'] == ACCOUNT)].copy()

# Determine effect and sign
def get_effect(row):
    if row['to'] == ACCOUNT:
        return float(row['amount']), '+'
    elif row['from'] == ACCOUNT:
        return -float(row['amount']), '-'
    return 0.0, ''

df[['effect', 'sign']] = df.apply(lambda row: pd.Series(get_effect(row)), axis=1)

# Sort by time just to be sure
df = df.sort_values(by='timestamp')

# Print all transactions
print(f"\nAll transactions affecting {ACCOUNT} up to {CUTOFF_TIME}:\n")
for idx, row in df.iterrows():
    print(f"{row['timestamp']} | {row['type']:10} | Amount: {row['amount']:>7} | From: {row['from']} -> To: {row['to']} | Effect: {row['sign']}")

# Optionally print final balance
print(f"\nFinal Balance: {df['effect'].sum():.2f}")
