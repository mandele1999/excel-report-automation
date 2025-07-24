import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    original_shape = df.shape
    print(f"Original shape: {original_shape}")

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Drop duplicates
    df = df.drop_duplicates()
    print(f"After dropping duplicates: {df.shape}")

    # Handle missing values
    for col in ['quantity', 'sales']:
        if col in df.columns:
            mean_val = df[col].mean()
            df[col].fillna(mean_val, inplace=True)
            print(f"Filled missing {col} with mean: {mean_val:.2f}")

    for col in ['product', 'category']:
        if col in df.columns:
            mode_val = df[col].mode()[0]
            df[col].fillna(mode_val, inplace=True)
            print(f"Filled missing {col} with mode: {mode_val}")

    # Convert date column
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        print("Parsed 'date' column as datetime.")

    # Drop rows with completely missing or broken date
    df = df.dropna(subset=['date'])
    print(f"After date cleaning: {df.shape}")

    return df