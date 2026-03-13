import pandas as pd
import os

files = [f for f in os.listdir('.') if f.endswith(('.csv', '.xlsx'))]

for file in files:
    print(f"\n--- FILE: {file} ---")
    try:
        if file.endswith('.csv'):
            df = pd.read_csv(file, nrows=0) # Only reads the header (very fast)
        else:
            df = pd.read_excel(file, nrows=0)
        print(list(df.columns))
    except Exception as e:
        print(f"Could not read {file}: {e}")
        