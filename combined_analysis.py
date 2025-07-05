import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- Configuration ---
CSV_FILE = 'mock_transactions_final.csv'
ACCOUNT = 'ZignalyX120'
CUTOFF_TIME = '2025-01-30 08:42:00'
GOOGLE_CREDS = 'credentials.json'
SHEET_NAME = 'Zignaly Analysis Report'

# --- Load data ---
df = pd.read_csv(CSV_FILE)
df['timestamp'] = pd.to_datetime(df['timestamp'])

df = df[df['timestamp'] <= pd.to_datetime(CUTOFF_TIME)]
df = df[(df['from'] == ACCOUNT) | (df['to'] == ACCOUNT)].copy()

# Determine effect and sign
def get_effect(row):
    if row['to'] == ACCOUNT:
        return float(row['amount']), '+'
    elif row['from'] == ACCOUNT:
        return -float(row['amount']), '-'
    return 0.0, ''

df[['effect', 'sign']] = df.apply(lambda row: pd.Series(get_effect(row)), axis=1)
df = df.sort_values(by='timestamp')

# --- Console Output: Transaction List ---
print(f"\nAll transactions affecting {ACCOUNT} up to {CUTOFF_TIME}:\n")
for _, row in df.iterrows():
    print(f"{row['timestamp']} | {row['type']:10} | Amount: {float(row['amount']):>10.6f} | "
          f"From: {row['from']} -> To: {row['to']} | Effect: {row['sign']}")

balance = df['effect'].sum()
print(f"\nFinal Balance: {balance:.2f}")

# --- Console Output: Totals by type ---
print(f"\n\nAccount: {ACCOUNT}")
print(f"Up to: {CUTOFF_TIME}\n")
print("Totals by Transaction Type:")
type_summary = df.groupby('type')['effect'].sum()
for tx_type, total in type_summary.items():
    sign = '+' if total >= 0 else ''
    print(f" - {tx_type}: {sign}{total:.2f}")
print(f"\nFinal Balance: {balance:.2f}")

# --- Google Sheets Output ---
print("\nExporting to Google Sheets...")

# Authorize
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(GOOGLE_CREDS, scopes=scope)
client = gspread.authorize(creds)

# Create or open spreadsheet
spreadsheet = client.create(SHEET_NAME)
sheet = spreadsheet.sheet1

# Share with your Google account (OPTIONAL)
spreadsheet.share('', perm_type='user', role='writer')

# Write transaction data
sheet.update('A1', [['Timestamp', 'Type', 'Amount', 'From', 'To', 'Effect']])
rows = [
    [row['timestamp'].strftime('%Y-%m-%d %H:%M:%S'), row['type'], row['amount'], row['from'], row['to'], row['sign']]
    for _, row in df.iterrows()
]
rows = [[cell if pd.notna(cell) else '' for cell in row] for row in rows]
sheet.update(f'A2:F{len(rows)+1}', rows)

# Add summary below
summary_start = len(rows) + 3
sheet.update(f'A{summary_start}', [['Transaction Type', 'Total Effect']])
summary_rows = [[tx_type, f"{total:.2f}"] for tx_type, total in type_summary.items()]
summary_rows.append(['Final Balance', f"{balance:.2f}"])
sheet.update(f'A{summary_start+1}:B{summary_start+len(summary_rows)}', summary_rows)

print(f"✅ Report created: https://docs.google.com/spreadsheets/d/{spreadsheet.id}")
