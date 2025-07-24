# Reddit BJJ Gi Scraper & Analyzer 🥋

Scrapes Reddit posts from r/bjj, r/jiujitsu, and r/mma to find the most recommended BJJ gis.  
Analyzes sentiment, mentions, and phrases, then visualizes brand popularity and quality.

## Features
- 🔍 Keyword-based scraping
- 💬 Sentiment analysis and phrase spotting
- 📊 Charts: frequency, sentiment breakdown, positivity %
- 🏆 Top 5 most helpful Reddit comments

## Getting Started

```bash
pip install praw pandas textblob matplotlib seaborn nltk


import nltk
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


python bjj_gi_scraper.py
python bjj_gi_analyzer.py
python bjj_gi_visuals.py

Built by elmo29404 with ChatGPT