import pandas as pd
import matplotlib.pyplot as plt
import os
 
# File paths
INPUT_CSV = 'data/trends_analysed.csv'
OUTPUT_FOLDER = 'outputs'
 
 

# TASK 1: Setup 

 
def setup():
    """
    Load the data and create the outputs folder.
    
    Returns:
        pd.DataFrame: Loaded data or None if failed
    """
    # Check if input file exists
    if not os.path.exists(INPUT_CSV):
        print(f"✗ Error: '{INPUT_CSV}' not found. Run Task 3 first.")
        return None
    
    # Load CSV into DataFrame
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"✓ Loaded {len(df)} stories from {INPUT_CSV}")
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        return None
    
    # Create outputs folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"✓ Created '{OUTPUT_FOLDER}/' folder")
    
    return df
 
 

# TASK 2: Chart 1 - Top 10 Stories by Score 

 
def create_chart1_top_stories(df):
    """
    Create a horizontal bar chart of top 10 stories by score.
    
    Args:
        df (pd.DataFrame): Data to visualize
    """
    print("\n📊 Creating Chart 1: Top 10 Stories by Score...")
    
    # Get top 10 stories by score
    top_10 = df.nlargest(10, 'score')[['title', 'score']].copy()
    
    # Shorten titles longer than 50 characters
    top_10['short_title'] = top_10['title'].apply(
        lambda x: x[:50] + '...' if len(x) > 50 else x
    )
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Create horizontal bar chart
    # Reverse order so highest is at top
    plt.barh(range(len(top_10)), top_10['score'], color='steelblue', edgecolor='black')
    
    # Set y-axis labels (story titles)
    plt.yticks(range(len(top_10)), top_10['short_title'])
    
    # Add title and axis labels
    plt.title('Top 10 Stories by Score', fontsize=14, fontweight='bold')
    plt.xlabel('Score', fontsize=12)
    plt.ylabel('Story Title', fontsize=12)
    
    # Add gridlines for better readability
    plt.grid(axis='x', alpha=0.3)
    
    # Tight layout to prevent label cutoff
    plt.tight_layout()
    
    # Save figure BEFORE showing
    output_path = os.path.join(OUTPUT_FOLDER, 'chart1_top_stories.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    # Close the figure to free memory
    plt.close()
    
    print(f"  ✓ Saved: {output_path}")
 
 

# TASK 3: Chart 2 - Stories per Category 

 
def create_chart2_categories(df):
    """
    Create a bar chart showing stories per category.
    
    Args:
        df (pd.DataFrame): Data to visualize
    """
    print("\n📊 Creating Chart 2: Stories per Category...")
    
    # Count stories per category
    category_counts = df['subreddit'].value_counts()
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Define different colors for each bar
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    # Create bar chart with different colors
    bars = plt.bar(category_counts.index, category_counts.values, 
                   color=colors[:len(category_counts)], edgecolor='black')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')
    
    # Add title and axis labels
    plt.title('Stories per Category', fontsize=14, fontweight='bold')
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Number of Stories', fontsize=12)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Add gridlines
    plt.grid(axis='y', alpha=0.3)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure BEFORE showing
    output_path = os.path.join(OUTPUT_FOLDER, 'chart2_categories.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    # Close figure
    plt.close()
    
    print(f"  ✓ Saved: {output_path}")
 
 

# TASK 4: Chart 3 - Score vs Comments Scatter 

 
def create_chart3_scatter(df):
    """
    Create a scatter plot of score vs comments, colored by popularity.
    
    Args:
        df (pd.DataFrame): Data to visualize
    """
    print("\n📊 Creating Chart 3: Score vs Comments Scatter...")
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Separate popular and non-popular stories
    popular = df[df['is_popular'] == True]
    not_popular = df[df['is_popular'] == False]
    
    # Plot popular stories (one color)
    plt.scatter(popular['score'], popular['num_comments'], 
               color='#FF6B6B', label='Popular', alpha=0.6, s=50, edgecolor='black')
    
    # Plot non-popular stories (different color)
    plt.scatter(not_popular['score'], not_popular['num_comments'], 
               color='#4ECDC4', label='Not Popular', alpha=0.6, s=50, edgecolor='black')
    
    # Add title and axis labels
    plt.title('Score vs Comments', fontsize=14, fontweight='bold')
    plt.xlabel('Score', fontsize=12)
    plt.ylabel('Number of Comments', fontsize=12)
    
    # Add legend
    plt.legend(loc='upper right')
    
    # Add gridlines
    plt.grid(alpha=0.3)
    
    # Tight layout
    plt.tight_layout()
    
    # Save figure BEFORE showing
    output_path = os.path.join(OUTPUT_FOLDER, 'chart3_scatter.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    # Close figure
    plt.close()
    
    print(f"  ✓ Saved: {output_path}")
 
 

# BONUS: Combined Dashboard 

 
def create_dashboard(df):
    """
    Combine all 3 charts into a single dashboard figure.
    
    Args:
        df (pd.DataFrame): Data to visualize
    """
    print("\n📊 Creating BONUS: Combined Dashboard...")
    
    # Create figure with 3 subplots (1 row, 3 columns)
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # ========== Subplot 1: Top 10 Stories ==========
    ax1 = axes[0]
    
    # Get top 10 stories
    top_10 = df.nlargest(10, 'score')[['title', 'score']].copy()
    top_10['short_title'] = top_10['title'].apply(
        lambda x: x[:30] + '...' if len(x) > 30 else x
    )
    
    # Create horizontal bar chart
    ax1.barh(range(len(top_10)), top_10['score'], color='steelblue', edgecolor='black')
    ax1.set_yticks(range(len(top_10)))
    ax1.set_yticklabels(top_10['short_title'], fontsize=8)
    ax1.set_xlabel('Score')
    ax1.set_title('Top 10 Stories', fontweight='bold')
    ax1.grid(axis='x', alpha=0.3)
    
    # ========== Subplot 2: Stories per Category ==========
    ax2 = axes[1]
    
    # Count stories per category
    category_counts = df['subreddit'].value_counts()
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
    
    # Create bar chart
    bars = ax2.bar(category_counts.index, category_counts.values, 
                   color=colors[:len(category_counts)], edgecolor='black')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=9)
    
    ax2.set_xlabel('Category')
    ax2.set_ylabel('Count')
    ax2.set_title('Stories per Category', fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    # ========== Subplot 3: Score vs Comments ==========
    ax3 = axes[2]
    
    # Separate by popularity
    popular = df[df['is_popular'] == True]
    not_popular = df[df['is_popular'] == False]
    
    # Scatter plot
    ax3.scatter(popular['score'], popular['num_comments'], 
               color='#FF6B6B', label='Popular', alpha=0.6, s=30)
    ax3.scatter(not_popular['score'], not_popular['num_comments'], 
               color='#4ECDC4', label='Not Popular', alpha=0.6, s=30)
    
    ax3.set_xlabel('Score')
    ax3.set_ylabel('Comments')
    ax3.set_title('Score vs Comments', fontweight='bold')
    ax3.legend(fontsize=8)
    ax3.grid(alpha=0.3)
    
    # ========== Overall Title ==========
    fig.suptitle('TrendPulse Dashboard', fontsize=16, fontweight='bold', y=1.02)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save dashboard
    output_path = os.path.join(OUTPUT_FOLDER, 'dashboard.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    # Close figure
    plt.close()
    
    print(f"  ✓ Saved: {output_path}")
 
 

# MAIN FUNCTION

 
def main():
    """
    Main function to run the complete visualization pipeline.
    """
    print("=" * 60)
    print("TRENDPULSE - TASK 4: VISUALIZATIONS")
    print("=" * 60)
    
    # Task 1: Setup and load data
    df = setup()
    
    if df is None:
        print("\n✗ Failed to load data. Exiting.")
        return
    
    # Task 2: Create Chart 1 - Top Stories
    create_chart1_top_stories(df)
    
    # Task 3: Create Chart 2 - Categories
    create_chart2_categories(df)
    
    # Task 4: Create Chart 3 - Scatter
    create_chart3_scatter(df)
    
    # Bonus: Create Dashboard
    create_dashboard(df)
    
    # Summary
    print("\n" + "=" * 60)
    print("ALL VISUALIZATIONS COMPLETE")
    print("=" * 60)
    print(f"✓ 3 individual charts created")
    print(f"✓ 1 combined dashboard created (BONUS)")
    print(f"✓ All files saved in '{OUTPUT_FOLDER}/' folder")
    print("=" * 60)
    print("\n✓ Task 4 complete!")
    print("✓ TrendPulse pipeline complete! 🎉")
 
 
if __name__ == "__main__":
    main()