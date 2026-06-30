# Vogue Search Engine

A search engine built from scratch using Python featuring a web crawler, inverted index, and TF-IDF ranking algorithm on Vogue.com content.

## Live Demo
https://vogue-search.streamlit.app/

## About
This project implements core search engine concepts from scratch without using any search libraries. It crawls Vogue.com, processes the content, builds an inverted index, and ranks results using the TF-IDF algorithm used by early search engines like Google.

## How It Works
1. crawler.py visits Vogue.com pages and extracts text content
2. indexer.py builds an inverted index and ranks results using TF-IDF
3. app.py provides a clean search interface built with Streamlit

## Tech Stack
- Python
- BeautifulSoup4 (web crawling)
- Requests (HTTP)
- Streamlit (UI)

## Concepts Implemented
- Web crawling and HTML parsing
- Inverted index data structure
- TF-IDF ranking algorithm
- Duplicate URL detection
- Stop word filtering

## Run Locally
pip install requests beautifulsoup4 streamlit
streamlit run app.py

## Author
Built by Ana Savage, MS Computer Science
