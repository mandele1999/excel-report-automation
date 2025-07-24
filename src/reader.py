import pandas as pd
import glob
import os

def load_and_merge_excels(folder_path: str) -> pd.DataFrame:
    all_files = glob.glob(os.path.join(folder_path, "*.xlsx"))
    if not all_files:
        raise FileNotFoundError(f"No Excel files found in {folder_path}")
    
    dataframes = []
    for file in all_files:
        try:
            df = pd.read_excel(file)
            print(f"Loaded {file} with {df.shape[0]} rows.")
            dataframes.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    merged_df = pd.concat(dataframes, ignore_index=True)
    print(f"\nMerged dataset shape: {merged_df.shape}")
    return merged_df
