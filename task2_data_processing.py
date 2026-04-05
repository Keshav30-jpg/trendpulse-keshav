import pandas as pd
import json
import os
from datetime import datetime
 
# File paths
DATA_FOLDER = 'data'
OUTPUT_CSV = 'data/trends_clean.csv'
 
 
def find_latest_json():
    """
    Find the most recent trends JSON file in the data folder.
    
    Returns:
        str: Path to JSON file or None
    """
    if not os.path.exists(DATA_FOLDER):
        print(f"✗ Error: '{DATA_FOLDER}/' folder not found. Run Task 1 first.")
        return None
    
    # Get all JSON files that match the pattern
    json_files = [f for f in os.listdir(DATA_FOLDER) 
                  if f.startswith('trends_') and f.endswith('.json')]
    
    if not json_files:
        print(f"✗ Error: No trends JSON files found. Run Task 1 first.")
        return None
    
    # Sort by date (filename) and get the latest
    json_files.sort(reverse=True)
    return os.path.join(DATA_FOLDER, json_files[0])
 
 
# ============================================================
# TASK 1: Load JSON into a Pandas DataFrame (4 marks)
# ============================================================
 
def load_json_to_dataframe():
    """
    Load the JSON file from Task 1 into a Pandas DataFrame.
    
    Returns:
        pd.DataFrame: Loaded data or None if failed
    """
    # Find the JSON file
    json_file = find_latest_json()
    
    if not json_file:
        return None
    
    try:
        # Load JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Print how many rows were loaded
        print(f"Loaded {len(df)} stories from {json_file}")
        
        return df
        
    except Exception as e:
        print(f"✗ Error loading JSON: {e}")
        return None
 
 
# ============================================================
# TASK 2: Clean the Data (10 marks)
# ============================================================
 
def clean_data(df):
    """
    Clean the DataFrame by removing duplicates, nulls, and low-quality data.
    
    Args:
        df (pd.DataFrame): Raw data from JSON
        
    Returns:
        pd.DataFrame: Cleaned data
    """
    # Step 1: Remove duplicates by post_id
    # Keep the first occurrence of each post_id
    df = df.drop_duplicates(subset=['post_id'], keep='first')
    print(f"After removing duplicates: {len(df)}")
    
    # Step 2: Remove rows with missing post_id, title, or score
    # Drop rows where any of these critical columns is null/missing
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")
    
    # Step 3: Ensure score and num_comments are integers
    # Convert to numeric first (handles any string values), then to int
    df['score'] = pd.to_numeric(df['score'], errors='coerce').fillna(0).astype(int)
    df['num_comments'] = pd.to_numeric(df['num_comments'], errors='coerce').fillna(0).astype(int)
    
    # Step 4: Remove stories where score is less than 5 (low quality filter)
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")
    
    # Step 5: Strip whitespace from title column
    # Remove leading and trailing spaces from all titles
    df['title'] = df['title'].str.strip()
    
    return df
 
 
# ============================================================
# TASK 3: Save as CSV and Print Summary (6 marks)
# ============================================================
 
def save_to_csv(df):
    """
    Save cleaned DataFrame to CSV and print summary statistics.
    
    Args:
        df (pd.DataFrame): Cleaned data
    """
    # Save to CSV file
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    
    # Print confirmation message with row count
    print(f"Saved {len(df)} rows to {OUTPUT_CSV}")
    
    # Print stories per category summary
    print("\nStories per category:")
    
    # Count stories per category and sort by category name
    category_counts = df['subreddit'].value_counts().sort_index()
    
    # Print each category with count, formatted nicely
    for category, count in category_counts.items():
        print(f"  {category:15} {count}")
 
 
# ============================================================
# MAIN FUNCTION
# ============================================================
 
def main():
    """
    Main function to run the complete data cleaning pipeline.
    """
    
    df = load_json_to_dataframe()
    
    if df is None:
        print("\n✗ Failed to load data. Exiting.")
        return
    
    # Task 2: Clean the data
    df_clean = clean_data(df)
    
    # Task 3: Save as CSV and print summary
    save_to_csv(df_clean)
    
    print("\n✓ Task 2 complete!")
 
 
if __name__ == "__main__":
    main()