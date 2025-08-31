import pandas as pd
import os

def append_unique_csv(new_file, result_file):
    # Columns to keep
    columns_to_keep = ["Title", "Link", "Difficulty"]
    
    # Read the new file
    new_df = pd.read_csv(new_file, usecols=columns_to_keep)
    
    # If result file exists, read it; otherwise create an empty DataFrame
    if os.path.exists(result_file):
        result_df = pd.read_csv(result_file)
        # Combine and drop duplicates based on 'id' (or you can use multiple columns)
        combined_df = pd.concat([result_df, new_df], ignore_index=True)
        combined_df.drop_duplicates(subset=["Title"], inplace=True)
    else:
        combined_df = new_df.drop_duplicates(subset=["Title"])
    
    # Write back to the result file
    combined_df.to_csv(result_file, index=False)
    print(f"Updated result file: {result_file} (Total rows: {len(combined_df)})")


# Example usage
new_csv_files = ["Adobe.csv", "Myntra.csv", "Netflix.csv"]
result_csv = "all_questions_filtered.csv"

for file in new_csv_files:
    append_unique_csv(file, result_csv)
