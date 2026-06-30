# We are importing libraries — think of these like toolboxes
# Each library gives us special powers we can use in our code

import requests  # This lets Python visit websites like a browser
from bs4 import BeautifulSoup  # This reads HTML and pulls out the text we want
import time  # This lets us pause between requests so we don't overload Vogue's server

# A function is a reusable block of code that does one specific job
# We define functions with the word "def" followed by the function name
# This function visits a webpage and returns all the text on it

def crawl_page(url):
    # url is the web address we want to visit
    
    try:
        # headers makes our request look like a real browser
        # Without this, some websites will block us
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # requests.get() visits the URL and downloads the page content
        response = requests.get(url, headers=headers, timeout=10)
        
        # 200 means success, anything else means something went wrong
        if response.status_code != 200:
            print(f"Failed to fetch {url} - Status code: {response.status_code}")
            return None
        
        # BeautifulSoup reads the raw HTML and makes it easy to work with
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Get the page title
        title = soup.find("title")
        title_text = title.get_text() if title else "No title found"
        
        # Remove script and style tags — these contain code not real text
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get ALL the text from the page
        page_text = soup.get_text(separator=" ", strip=True)
        
        # Find all links on the page so we can crawl more pages later
        # <a> tags are links in HTML
        links = []
        for a_tag in soup.find_all("a", href=True):
            # href is the actual URL inside the link
            href = a_tag["href"]
            # Only keep links that are Vogue articles
            if href.startswith("https://www.vogue.com/article"):
                links.append(href)
        
        # Pause for 1 second to be polite to Vogue's server
        time.sleep(1)
        
        # Return a dictionary with our results
        return {
            "url": url,
            "title": title_text,
            "content": page_text,
            "links": links  # Links we found on this page
        }
    
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return None


# These are Vogue article pages we want to crawl
# We start with Vogue's main sections
urls_to_crawl = [
    "https://www.vogue.com/fashion",
    "https://www.vogue.com/beauty",
    "https://www.vogue.com/runway",
    "https://www.vogue.com/culture",
    "https://www.vogue.com/fashion-shows"
]

# This list will store all our crawled pages
crawled_pages = []

# This SET keeps track of URLs we've already crawled
# A set is like a list, but it automatically prevents duplicates
seen_urls = set()

def clean_url(url):
    # Tracking links often have extra junk after a # symbol
    # Example: vogue.com/article/dress#intcid=tracking-junk
    # We only want: vogue.com/article/dress
    # .split("#")[0] cuts off everything after the # symbol
    return url.split("#")[0]

# Loop through each URL and crawl it
for url in urls_to_crawl:
    print(f"Crawling: {url}")
    
    result = crawl_page(url)
    
    if result:
        crawled_pages.append(result)
        print(f"✅ Successfully crawled: {result['title']}")
        
       # Also crawl article links we found on each page
        for article_link in result["links"][:3]:
            # Clean the URL to remove tracking junk
            clean_link = clean_url(article_link)
            
            # Only crawl this article if we haven't seen it before
            if clean_link not in seen_urls:
                seen_urls.add(clean_link)  # Remember we've seen this URL now
                
                print(f"  Crawling article: {clean_link}")
                article_result = crawl_page(clean_link)
                if article_result:
                    crawled_pages.append(article_result)
                    print(f"  ✅ Got article: {article_result['title']}")
            else:
                print(f"  ⏭️ Skipping duplicate: {clean_link}")
    else:
        print(f"❌ Failed to crawl: {url}")

# Print final results
print(f"\nDone! Crawled {len(crawled_pages)} pages successfully")
for page in crawled_pages:
    print(f"- {page['title']}")
    import json

# Save crawled pages to a JSON file
# This means we don't need to re-crawl every time the app loads
# json.dumps() converts our Python list to a JSON string
with open('crawled_data.json', 'w') as f:
    json.dump(crawled_pages, f)
    
print("Saved crawled data to crawled_data.json!")