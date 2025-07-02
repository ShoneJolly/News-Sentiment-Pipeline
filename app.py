import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")

# Centered page title
st.markdown("<h1 style='text-align: center;'>News Sentiment Dashboard</h1>", unsafe_allow_html=True)

# CSS to center column headers
st.markdown("""
<style>
    table.dataframe th {
        text-align: center !important;
        vertical-align: middle !important;
    }
</style>
""", unsafe_allow_html=True)

# Define colors for sentiment_label
sentiment_colors = {
    "positive": "background-color: green; color: black;",
    "negative": "background-color: red; color: black;",
    "neutral": "background-color: lightgray; color: black;"
}

# Read environment variables (no fallback)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    st.error("Database connection failed: Missing environment variables (DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD).")
    st.stop()

# Build connection URL from environment variables
conn = st.connection(
    "postgresql",
    type="sql",
    url=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Query data
query = "SELECT published_at, source, sentiment_label, title, description FROM news_articles;"
df = conn.query(query, ttl="10m")

# Sort by published_at descending (latest news first)
df = df.sort_values(by="published_at", ascending=False)

# Rename column RDS Header -> DashBoard Header
df.rename(columns={
    "published_at": "Published At",
    "source": "Source Name",
    "sentiment_label": "Sentiment",
    "title": "Title",
    "description": "Description"
}, inplace=True)

# Style sentiment column background and text color
styled_df = df.style.map(lambda val: sentiment_colors.get(val.lower(), ""), subset=["Sentiment"])

# Center-align 'sentiment' column text
styled_df = styled_df.set_properties(subset=["Sentiment"], **{'text-align': 'center'})

# Hide index and set table width
styled_df = styled_df.hide(axis="index").set_table_attributes('class="dataframe" style="width:100%;"')

# Render the styled dataframe as HTML
st.markdown(styled_df.to_html(), unsafe_allow_html=True)