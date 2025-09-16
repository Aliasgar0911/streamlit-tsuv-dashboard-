import streamlit as st
import pandas as pd
import feedparser

st.set_page_config(page_title="MIS Dashboard with News Ticker", layout="wide")

st.title("📊 MIS Dashboard")

# File uploader for MIS data
uploaded_file = st.file_uploader("Upload your MIS Excel/CSV", type=["xlsx","csv"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.dataframe(df.head())

# --- NEWS TICKER ---

feeds = [
    "https://techcrunch.com/tag/startups/feed/",   # Global startup funding/acquisitions
    "https://www.inc42.com/feed/",                 # Indian startup/VC funding
    "https://yourstory.com/feed",                  # Indian startup ecosystem
    "https://www.vccircle.com/rss"                 # India PE/VC deals
]

headlines = []
for url in feeds:
    try:
        feed = feedparser.parse(url)
        headlines.extend([f"<a href='{entry.link}' target='_blank' style='color:white;text-decoration:none;'>{entry.title}</a>" for entry in feed.entries[:3]])
    except Exception:
        pass

if headlines:
    news_text = " 🔔 ".join(headlines)
else:
    news_text = "No news available right now."

st.markdown(f"""
    <style>
    .ticker {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: black;
        color: white;
        padding: 10px;
        font-size: 16px;
        font-weight: bold;
        overflow: hidden;
        white-space: nowrap;
        box-sizing: border-box;
        z-index: 9999;
    }}
    .ticker-text {{
        display: inline-block;
        padding-left: 100%;
        animation: ticker 40s linear infinite;
    }}
    @keyframes ticker {{
        0%   {{ transform: translateX(0%); }}
        100% {{ transform: translateX(-100%); }}
    }}
    </style>
    <div class="ticker"><div class="ticker-text">
        {news_text}
    </div></div>
""", unsafe_allow_html=True)
