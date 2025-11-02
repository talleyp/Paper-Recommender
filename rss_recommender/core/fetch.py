import requests
import logging

def get_feed_xml(url: str) -> str | None:
    """
    Fetches the raw XML content from a single URL.
    Returns the content as a string, or None if it fails.
    """
    try:
        headers = {'User-Agent': 'RSSRecommenderProject/1.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
        
    except requests.exceptions.RequestException as e:
        # Log the error for debugging
        logging.error(f"Failed to fetch {url}: {e}")
        return None