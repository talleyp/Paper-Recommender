from rss_recommender import config
from rss_recommender.core import fetch, parse
from rss_recommender.logic import storage

# (Assume config.py has a list called FEED_URLS)
# (Assume parse.py has a 'parse_articles' function)
# (Assume storage.py has a 'add_articles_to_db' function)

def run_pipeline():
    print("Starting daily feed ingestion...")
    all_new_articles = []
    
    # 1. main.py reads the list from config
    for url in config.FEED_URLS:
        
        # 2. main.py calls fetch
        print(f"Fetching {url}...")
        raw_xml = fetch.get_feed_xml(url)
        
        # 3. If fetch was successful, main.py calls parse
        if raw_xml:
            articles_list = parse.parse_articles(raw_xml)
            all_new_articles.extend(articles_list)
            
    # 4. After the loop, main.py calls storage
    print(f"Found {len(all_new_articles)} new articles. Saving to database...")
    storage.add_articles_to_db(all_new_articles)
    
    print("Pipeline finished.")

if __name__ == "__main__":
    run_pipeline()