print("indexer.py is running!")
# The Indexer — this is the heart of our search engine
# It takes all the pages we crawled and builds a searchable index
# Think of it like building the index at the back of a textbook
# where you can look up any word and find which pages it appears on

import re  # re stands for "regular expressions" — helps us clean up text
import math  # math gives us mathematical functions we'll need for ranking

# =============================================
# STEP 1: CLEAN THE TEXT
# =============================================

def clean_text(text):
    # This function takes raw messy text and cleans it up
    # Raw text from websites has lots of junk we don't want
    
    # .lower() converts ALL text to lowercase
    # This means "Vogue" and "vogue" are treated as the same word
    text = text.lower()
    
    # re.sub() finds and replaces text using patterns
    # [^a-z0-9\s] means "find anything that is NOT a letter, number, or space"
    # We replace those characters with nothing "" — effectively deleting them
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    # .split() breaks the text into individual words
    # "hello world" becomes ["hello", "world"]
    words = text.split()
    
    # These are "stop words" — common words that don't help with searching
    # Words like "the", "and", "is" appear everywhere and aren't useful
    stop_words = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", 
        "to", "for", "of", "with", "by", "from", "is", "are", 
        "was", "were", "be", "been", "have", "has", "had", "do",
        "does", "did", "will", "would", "could", "should", "may",
        "might", "this", "that", "these", "those", "it", "its"
    }
    
    # List comprehension — this is a shortcut way to create a new list
    # It means: "keep the word only if it's NOT in stop_words"
    # and only if the word is longer than 2 characters
    words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Return our clean list of words
    return words


# =============================================
# STEP 2: BUILD THE INVERTED INDEX
# =============================================

def build_index(crawled_pages):
    # An inverted index maps each word to the pages it appears on
    # Example: {"moisturizer": ["page1_url", "page3_url"], "foundation": ["page2_url"]}
    # This is EXACTLY how Google's search index works at its core!
    
    # We use a dictionary to store our index
    # {} creates an empty dictionary
    index = {}
    
    # Loop through each page we crawled
    for page in crawled_pages:
        # Get the URL of this page — we'll use it as the page identifier
        url = page["url"]
        
        # Combine the title and content for better search results
        # Titles are important so we add them twice to give them more weight
        full_text = page["title"] + " " + page["title"] + " " + page["content"]
        
        # Clean the text using our function from above
        words = clean_text(full_text)
        
        # Count how many times each word appears on this page
        # This is called "term frequency"
        word_count = {}
        for word in words:
            # If we've seen this word before, add 1 to its count
            # If not, start counting from 0 and add 1
            word_count[word] = word_count.get(word, 0) + 1
        
        # Add each word to our index
        for word, count in word_count.items():
            # If this word isn't in our index yet, add it with an empty list
            if word not in index:
                index[word] = []
            
            # Add this page and its word count to the index
            index[word].append({
                "url": url,
                "title": page["title"],
                "count": count,  # How many times the word appears
                "content_preview": page["content"][:200]  # First 200 characters as preview
            })
    
    # Return our completed index
    return index


# =============================================
# STEP 3: SEARCH THE INDEX
# =============================================

def search(query, index, crawled_pages):
    # This function takes a search query and finds the most relevant pages
    
    # Clean the query the same way we cleaned our pages
    # This ensures "Moisturizer" matches "moisturizer"
    query_words = clean_text(query)
    
    # If the query is empty after cleaning, return nothing
    if not query_words:
        return []
    
    # This dictionary will store scores for each page
    # Higher score = more relevant to the search query
    scores = {}
    
    # Loop through each word in the search query
    for word in query_words:
        # Check if this word exists in our index
        if word in index:
            # Get all pages that contain this word
            pages_with_word = index[word]
            
            # Calculate how rare this word is across all pages
            # Rare words are more meaningful than common words
            # This is called "Inverse Document Frequency" (IDF)
            # It's a key part of the TF-IDF algorithm used by real search engines!
            num_pages_with_word = len(pages_with_word)
            total_pages = len(crawled_pages)
            
            # math.log() calculates the logarithm
            # We add 1 to avoid dividing by zero
            idf = math.log(total_pages / (num_pages_with_word + 1))
            
            # Loop through each page that contains this word
            for page_info in pages_with_word:
                url = page_info["url"]
                
                # TF = Term Frequency (how often the word appears on this page)
                tf = page_info["count"]
                
                # TF-IDF score: multiply term frequency by inverse document frequency
                # This is the same algorithm Google originally used!
                tf_idf_score = tf * idf
                
                # Add this score to the page's total score
                # .get(url, 0) returns the current score or 0 if not seen yet
                scores[url] = scores.get(url, 0) + tf_idf_score
    
    # Sort pages by score from highest to lowest
    # sorted() sorts a list, key tells it what to sort by
    # reverse=True means highest first
    sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Build our final results list
    results = []
    for url, score in sorted_results[:10]:  # Only return top 10 results
        # Find the full page info for this URL
        for page in crawled_pages:
            if page["url"] == url:
                results.append({
                    "url": url,
                    "title": page["title"],
                    "score": round(score, 2),  # Round to 2 decimal places
                    "preview": page["content"][:300]  # First 300 chars as preview
                })
                break
    
    return results


# =============================================
# TEST OUR SEARCH ENGINE
# =============================================

# Import our crawled pages from crawler.py
# First let's run the crawler to get fresh pages
from crawler import crawled_pages

# Build the index from our crawled pages
print("Building search index...")
index = build_index(crawled_pages)
print(f"Index built! Indexed {len(index)} unique words\n")

# Test some searches
test_queries = ["hair", "fashion", "beauty", "dress", "skincare"]

for query in test_queries:
    print(f"🔍 Search: '{query}'")
    results = search(query, index, crawled_pages)
    
    if results:
        # Show top 3 results for each query
        for i, result in enumerate(results[:3], 1):
            print(f"  {i}. {result['title']}")
            print(f"     Score: {result['score']} | URL: {result['url']}")
    else:
        print("  No results found")
    print()