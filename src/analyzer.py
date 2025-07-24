import pandas as pd

def summarize_sales(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby(['product', 'category', 'date'], as_index=False)
        .agg({
            'quantity': 'sum',
            'sales': 'sum'
        })
        .sort_values(by='date')
    )
    
    print(f"Grouped summary shape: {grouped.shape}")
    return grouped