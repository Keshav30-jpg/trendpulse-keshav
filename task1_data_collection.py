import requests
import json
import time
import os
from datetime import datetime
 
# API endpoints
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
 
# Category keywords for classification
CATEGORIES = {
    'technology': ['ai', 'software', 'tech', 'code', 'computer', 'data', 'cloud', 'api', 'gpu', 'llm'],
    'worldnews': ['war', 'government', 'country', 'president', 'election', 'climate', 'attack', 'global'],
    'sports': ['nfl', 'nba', 'fifa', 'sport', 'game', 'team', 'player', 'league', 'championship'],
    'science': ['research', 'study', 'space', 'physics', 'biology', 'discovery', 'nasa', 'genome'],
    'entertainment': ['movie', 'film', 'music', 'netflix', 'game', 'book', 'show', 'award', 'streaming']
}
 
# Headers for API requests
HEADERS = {"User-Agent": "TrendPulse/1.0"}
 
 
def assign_category(title):
    """
    Assign a category to a story based on keywords in its title.
    
    Args:
        title (str): Story title
        
    Returns:
        str: Category name or 'uncategorized'
    """
    if not title:
        return 'uncategorized'
    
    # Convert title to lowercase for case-insensitive matching
    title_lower = title.lower()
    
    # Check each category's keywords
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    
    # If no keywords match, return uncategorized
    return 'uncategorized'
 
 
def fetch_top_story_ids():
    """
    Fetch the list of top story IDs from HackerNews.
    
    Returns:
        list: List of story IDs (first 500)
    """
    print("Fetching top story IDs...")
    
    try:
        response = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        story_ids = response.json()
        
        # Get first 500 IDs
        story_ids = story_ids[:500]
        
        print(f"✓ Found {len(story_ids)} top stories")
        return story_ids
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error fetching story IDs: {e}")
        return []
 
 
def fetch_story_details(story_id):
    """
    Fetch details for a single story.
    
    Args:
        story_id (int): HackerNews story ID
        
    Returns:
        dict: Story details or None if failed
    """
    try:
        url = STORY_URL.format(story_id)
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        # Don't crash - just skip this story
        print(f"  ✗ Failed to fetch story {story_id}: {e}")
        return None
 
 
def extract_fields(story):
    """
    Extract required fields from a story object.
    
    Args:
        story (dict): Raw story data from API
        
    Returns:
        dict: Extracted fields in required format
    """
    # Get title (required for categorization)
    title = story.get('title', '')
    
    # Assign category based on title keywords
    category = assign_category(title)
    
    # Extract all required fields
    extracted = {
        'post_id': story.get('id'),
        'title': title,
        'subreddit': category,  # Our assigned category
        'score': story.get('score', 0),
        'num_comments': story.get('descendants', 0),  # 'descendants' = total comments
        'author': story.get('by', 'unknown'),
        'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return extracted
 
 
def collect_posts_by_category(story_ids, target_per_category=25):
    """
    Collect posts and organize them by category.
    
    Args:
        story_ids (list): List of story IDs to fetch
        target_per_category (int): Target number of posts per category
        
    Returns:
        list: All collected posts
    """
    # Track posts by category
    posts_by_category = {cat: [] for cat in CATEGORIES.keys()}
    posts_by_category['uncategorized'] = []
    
    all_posts = []
    total_fetched = 0
    
    print(f"\nCollecting stories (target: {target_per_category} per category)...")
    print("-" * 60)
    
    # Fetch stories until we have enough in each category
    for story_id in story_ids:
        # Check if we have enough posts in all categories
        if all(len(posts) >= target_per_category for posts in posts_by_category.values()):
            print("\n✓ Reached target for all categories!")
            break
        
        # Fetch story details
        story = fetch_story_details(story_id)
        
        if not story:
            continue
        
        # Only process actual stories (not jobs, polls, etc.)
        if story.get('type') != 'story':
            continue
        
        # Extract fields
        post = extract_fields(story)
        category = post['subreddit']
        
        # Add to category collection if not full
        if len(posts_by_category[category]) < target_per_category:
            posts_by_category[category].append(post)
            all_posts.append(post)
            total_fetched += 1
            
            # Print progress every 10 posts
            if total_fetched % 10 == 0:
                print(f"  Collected {total_fetched} posts so far...")
    
    # Print category breakdown
    print("\n" + "=" * 60)
    print("CATEGORY BREAKDOWN")
    print("=" * 60)
    for category, posts in posts_by_category.items():
        print(f"  {category:15} : {len(posts)} posts")
    
    # Add 2-second delay per category (as required)
    print("\nAdding delay between categories...")
    for category in CATEGORIES.keys():
        if posts_by_category[category]:
            time.sleep(2)
            print(f"  ✓ Processed {category}")
    
    return all_posts
 
 
def save_to_json(posts):
    """
    Save posts to a JSON file in the data/ folder.
    
    Args:
        posts (list): List of post dictionaries
        
    Returns:
        str: Filename where data was saved
    """
    # Create data folder if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')
        print("\n✓ Created 'data/' folder")
    
    # Generate filename with today's date
    date_str = datetime.now().strftime('%Y%m%d')
    filename = f'data/trends_{date_str}.json'
    
    # Save to JSON file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
    
    return filename
 
 
def main():
    """
    Main function to orchestrate the data collection process.
    """
    print("=" * 60)
    print("TRENDPULSE - TASK 1: DATA COLLECTION")
    print("=" * 60)
    
    # Step 1: Fetch top story IDs
    story_ids = fetch_top_story_ids()
    
    if not story_ids:
        print("\n✗ Failed to fetch story IDs. Exiting.")
        return
    
    # Step 2: Collect posts by category
    all_posts = collect_posts_by_category(story_ids, target_per_category=25)
    
    # Step 3: Save to JSON file
    if all_posts:
        filename = save_to_json(all_posts)
        
        print("\n" + "=" * 60)
        print("COLLECTION COMPLETE")
        print("=" * 60)
        print(f"✓ Collected {len(all_posts)} posts")
        print(f"✓ Saved to {filename}")
        print("=" * 60)
        
    else:
        print("\n✗ No posts collected. Please check your internet connection and try again.")
 
 
if __name__ == "__main__":
    main()