# This is our search engine's user interface
# Streamlit turns this Python code into a website automatically!

import streamlit as st
from crawler import crawled_pages
from indexer import build_index, search

# Page configuration
st.set_page_config(
    page_title="Vogue Search",
    page_icon="🔎",
    layout="centered"
)

# Custom CSS to make it look cleaner and more like a real search engine
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

# Cache the index so it's not rebuilt every search
@st.cache_data
def get_index():
    return build_index(crawled_pages)

index = get_index()

# Clean, minimal header
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