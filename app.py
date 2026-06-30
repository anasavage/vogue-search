# This is our search engine's user interface
# Now it loads pre-crawled data from a JSON file instead of crawling every time
# This makes the app much faster!

import streamlit as st
import json  # json lets us read and write JSON files
from indexer import build_index, search

# Load our pre-crawled data from the JSON file
# This is much faster than re-crawling Vogue every time someone visits
@st.cache_data
def load_data():
    # open() opens a file, 'r' means we're reading it
    with open('crawled_data.json', 'r') as f:
        # json.load() converts the JSON file back into a Python list
        return json.load(f)

# Cache the index so it's not rebuilt every search
@st.cache_data
def get_index(data_json):
    crawled_pages = json.loads(data_json)
    return build_index(crawled_pages)

# Load data and build index
crawled_pages = load_data()
data_json = json.dumps(crawled_pages)
index = get_index(data_json)

# Page configuration
st.set_page_config(
    page_title="Vogue Search",
    page_icon="🔎",
    layout="centered"
)

# Custom CSS for clean Google-style look
st.markdown("""
    <style>
    .main {
        padding-top: 3rem;
    }
    .result-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .result-url {
        font-size: 13px;
        color: #5f6368;
        margin-bottom: 6px;
    }
    .result-preview {
        font-size: 14px;
        color: #4d5156;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# Clean minimal header
st.markdown("<h1 style='text-align: center; font-weight: 700;'>Vogue Search</h1>", unsafe_allow_html=True)
st.markdown(
    f"<p style='text-align: center; color: #5f6368;'>Custom search engine indexing {len(crawled_pages)} pages from Vogue.com</p>",
    unsafe_allow_html=True
)

st.write("")

# Search input
query = st.text_input(
    "",
    placeholder="Search Vogue articles...",
    label_visibility="collapsed"
)

st.write("")

if query:
    results = search(query, index, crawled_pages)
    
    if results:
        st.markdown(f"<p style='color: #5f6368; font-size: 14px;'>About {len(results)} results</p>", unsafe_allow_html=True)
        st.write("")
        
        for result in results:
            st.markdown(f"""
                <div class="result-url">{result['url']}</div>
                <div class="result-title"><a href="{result['url']}" target="_blank" style="text-decoration: none; color: #1a0dab;">{result['title']}</a></div>
                <div class="result-preview">{result['preview']}...</div>
            """, unsafe_allow_html=True)
            st.write("")
    else:
        st.write(f"No results found for **{query}**")

else:
    st.markdown(
        "<p style='text-align: center; color: #80868b; font-size: 13px;'>Try: dress, hair, beauty, fashion</p>",
        unsafe_allow_html=True
    )