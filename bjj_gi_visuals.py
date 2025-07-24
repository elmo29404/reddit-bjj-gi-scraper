import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from collections import Counter

# Load analyzed CSV
df = pd.read_csv("bjj_gi_reviews_analyzed.csv")

# Parse stringified lists
df["mentioned_brands"] = df["mentioned_brands"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])

# === BRAND FREQUENCY ===
all_brands = sum(df["mentioned_brands"], [])
brand_counts = Counter(all_brands)
brand_df = pd.DataFrame(brand_counts.items(), columns=["brand", "count"]).sort_values(by="count", ascending=False)

# Chart 1: Brand Frequency
plt.figure(figsize=(12, 5))
sns.barplot(data=brand_df, x="brand", y="count", hue="brand", legend=False, palette="Blues_d")
plt.title("BJJ Gi Brand Mention Frequency")
plt.ylabel("Mentions")
plt.xlabel("Brand")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("brand_frequency_chart.png")
plt.show()

# === SENTIMENT BREAKDOWN PER BRAND ===
exploded = df.explode("mentioned_brands")
exploded = exploded[exploded["mentioned_brands"] != ""]

sentiment_counts = exploded.groupby(["mentioned_brands", "sentiment"]).size().reset_index(name="count")
pivot = sentiment_counts.pivot(index="mentioned_brands", columns="sentiment", values="count").fillna(0)

# Keep only brands that appear in frequency chart
existing_brands = brand_df["brand"].tolist()
pivot = pivot.loc[pivot.index.intersection(existing_brands)]

# Chart 2: Stacked Sentiment Breakdown
pivot.plot(kind="bar", stacked=True, figsize=(14, 6), colormap="Set2")
plt.title("Sentiment Breakdown per BJJ Gi Brand")
plt.xlabel("Brand")
plt.ylabel("Number of Mentions")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Sentiment")
plt.tight_layout()
plt.savefig("brand_sentiment_chart.png")
plt.show()

# === QUALITY RANKING CHART: Positivity % ===
quality = pivot.copy()
quality["total"] = quality.sum(axis=1)
quality["positive_pct"] = (quality["Positive"] / quality["total"]) * 100
quality_sorted = quality.sort_values(by="positive_pct", ascending=False)

# Chart 3: Positivity % per Brand
plt.figure(figsize=(12, 6))
sns.barplot(x=quality_sorted.index, y=quality_sorted["positive_pct"], palette="Greens_d")
plt.title("BJJ Gi Brand Quality Ranking (Positivity %)")
plt.ylabel("Positive Mentions (%)")
plt.xlabel("Brand")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("brand_quality_chart.png")
plt.show()

# === TOP 5 MOST HELPFUL COMMENTS (by Reddit score) ===
top_comments = exploded[["mentioned_brands", "comment", "score", "sentiment", "url"]]
top_comments = top_comments.sort_values(by="score", ascending=False).dropna(subset=["comment"])
top_5 = top_comments.head(5)

print("\n🧠 Top 5 Most Helpful Comments (by upvotes):")
for idx, row in top_5.iterrows():
    print(f"\n⭐️ Score: {row['score']}")
    print(f"Brand: {row['mentioned_brands']}")
    print(f"Sentiment: {row['sentiment']}")
    print(f"Comment: {row['comment'][:300]}{'...' if len(row['comment']) > 300 else ''}")
    print(f"Link: {row['url']}")
