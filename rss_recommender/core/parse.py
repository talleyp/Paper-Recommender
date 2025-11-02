import feedparser
import time
from datetime import datetime
from bs4 import BeautifulSoup 
from dateutil import parser  
from fetch import get_feed_xml
from pprint import pprint

def parse_articles(xml_string: str) -> list[dict]:
    """
    Parses a raw XML string into a clean list of article dicts.
    """
    
    feed = feedparser.parse(xml_string)
    articles_list = []

    for entry in feed.entries:
        # 1. Get Title, Link, and GUID
        title = entry.get('title')
        link = entry.get('link')
        
        # The 'id' field is a great fallback for 'guid'
        guid = entry.get('guid', entry.get('id'))

        # 2. Get Description 
        description = entry.get('content', [{}])[0].get('value')
        if not description:
            description = None

        # 3. Get Pub Date (Your key discovery)
        pub_date = None
        
        # ---> Step 3a: Try the standard way first
        if entry.get('updated_parsed'):
            # Convert feedparser's struct_time into a datetime object
            pub_date = datetime.fromtimestamp(time.mktime(entry.updated_parsed))
        
        # ---> Step 3b: If standard way fails, run custom logic
        if not pub_date and entry.get('summary'):
            try:
                # Use BeautifulSoup to parse the HTML in the summary
                soup = BeautifulSoup(entry.summary, 'html.parser')
                
                # Find the first <p> tag and get its text
                p_text = soup.find('p').get_text() # "Publication date: 21 January 2026"
                
                # Clean the string and parse it
                date_string = p_text.replace('Publication date: ', '') # "21 January 2026"
                pub_date = parser.parse(date_string) # This handles the string beautifully
                
            except Exception as e:
                # If our custom parsing fails, we give up
                print(f"Failed to parse date from summary: {e}")
                pub_date = datetime.now()

        # 4. Add to our list (only if we have the essentials)
        if title and link and guid and pub_date:
            articles_list.append({
                'title': title,
                'link': link,
                'description': description,
                'pub_date': pub_date,
                'guid': guid
            })
        pprint(entry)
            
    return articles_list

# test_url = 'https://rss.sciencedirect.com/publication/science/00225193'
test_url = "https://www.journals.uchicago.edu/action/showFeed?type=etoc&feed=rss&jc=an"
parse_articles(get_feed_xml(test_url))