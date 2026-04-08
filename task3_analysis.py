import pandas as pd
import numpy as np
import os
 
# File paths
INPUT_CSV = 'data/trends_clean.csv'
OUTPUT_CSV = 'data/trends_analysed.csv'
 
 

# TASK 1: Load and Explore 

 
def load_and_explore():
    """
    Load the cleaned CSV from Task 2 and print basic exploration stats.
    
    Returns:
        pd.DataFrame: Loaded data or None if failed
    """
    # Check if file exists
    if not os.path.exists(INPUT_CSV):
        print(f"✗ Error: '{INPUT_CSV}' not found. Run Task 2 first.")
        return None
    
    try:
        # Load CSV into DataFrame
        df = pd.read_csv(INPUT_CSV)
        
        # Print shape (rows, columns)
        print(f"Loaded data: {df.shape}")
        
        # Print first 5 rows
        print("\nFirst 5 rows:")
        print(df.head())
        
        # Calculate and print average score
        avg_score = df['score'].mean()
        print(f"\nAverage score   : {avg_score:,.0f}")
        
        # Calculate and print average comments
        avg_comments = df['num_comments'].mean()
        print(f"Average comments: {avg_comments:,.0f}")
        
        return df
        
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        return None
 
 

# TASK 2: Basic Analysis with NumPy 

 
def numpy_analysis(df):
    """
    Use NumPy to compute statistics and answer analytical questions.
    
    Args:
        df (pd.DataFrame): Data to analyze
    """
    print("\n--- NumPy Stats ---")
    
    # Convert score column to NumPy array
    scores = df['score'].to_numpy()
    
    # Calculate mean, median, and standard deviation using NumPy
    mean_score = np.mean(scores)
    median_score = np.median(scores)
    std_score = np.std(scores)
    
    print(f"Mean score   : {mean_score:,.0f}")
    print(f"Median score : {median_score:,.0f}")
    print(f"Std deviation: {std_score:,.0f}")
    
    # Find highest and lowest score using NumPy
    max_score = np.max(scores)
    min_score = np.min(scores)
    
    print(f"Max score    : {max_score:,}")
    print(f"Min score    : {min_score:,}")
    
    # Find category with most stories
    # Count stories per category
    category_counts = df['subreddit'].value_counts()
    most_common_category = category_counts.idxmax()
    most_common_count = category_counts.max()
    
    print(f"Most stories in: {most_common_category} ({most_common_count} stories)")
    
    # Find story with most comments
    # Get index of row with maximum comments
    max_comments_idx = df['num_comments'].idxmax()
    most_commented_story = df.loc[max_comments_idx]
    
    print(f'Most commented story: "{most_commented_story["title"]}" — {most_commented_story["num_comments"]:,} comments')
 
 

# TASK 3: Add New Columns 

 
def add_new_columns(df):
    """
    Add two new columns: engagement and is_popular.
    
    Args:
        df (pd.DataFrame): Data to modify
        
    Returns:
        pd.DataFrame: Data with new columns
    """
    # Column 1: engagement
    # Formula: num_comments / (score + 1)
    # The +1 prevents division by zero
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    # Column 2: is_popular
    # Formula: True if score > average score, else False
    average_score = df['score'].mean()
    df['is_popular'] = df['score'] > average_score
    
    return df
 
 

# TASK 4: Save the Result 

 
def save_result(df):
    """
    Save the updated DataFrame to CSV.
    
    Args:
        df (pd.DataFrame): Data to save
    """
    # Save to CSV file
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    
    # Print confirmation message
    print(f"\nSaved to {OUTPUT_CSV}")
 
 

# MAIN FUNCTION

 
def main():
    """
    Main function to run the complete analysis pipeline.
    """
    # Task 1: Load and explore the data
    df = load_and_explore()
    
    if df is None:
        print("\n✗ Failed to load data. Exiting.")
        return
    
    # Task 2: Perform NumPy analysis
    numpy_analysis(df)
    
    # Task 3: Add new columns
    df = add_new_columns(df)
    
    # Task 4: Save the result
    save_result(df)
    
    print("\n✓ Task 3 complete!")
 
 
if __name__ == "__main__":
    main()