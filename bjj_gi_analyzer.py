import pandas as pd
from textblob import TextBlob
import ast
from collections import Counter

# Load scraped data
df = pd.read_csv("bjj_gi_recommendations_all_subreddits.csv")

# ✅ Top 60 BJJ gi brands + aliases
brand_aliases = {
    "shoyoroll": ["shoyoroll"],
    "tatami": ["tatami"],
    "fuji": ["fuji"],
    "origin": ["origin", "origin usa"],
    "hyperfly": ["hyperfly"],
    "kingz": ["kingz", "kingz kimonos"],
    "atama": ["atama"],
    "aesthetic": ["aesthetic", "aesthetic gi"],
    "vhts": ["vhts"],
    "gameness": ["gameness"],
    "flow": ["flow", "flow kimonos"],
    "inverted gear": ["inverted gear", "inverted"],
    "gold bjj": ["gold bjj", "goldbjj", "gold bjj gear"],
    "hayabusa": ["hayabusa"],
    "venum": ["venum"],
    "93brand": ["93brand", "93 brand"],
    "war tribe": ["war tribe", "wartribe"],
    "pearl weave": ["pearl weave"],
    "grips": ["grips", "grips athletics"],
    "maeda": ["maeda"],
    "scramble": ["scramble"],
    "storm": ["storm", "storm kimonos"],
    "syndicate": ["syndicate"],
    "do or die": ["do or die", "do-or-die"],
    "reversal": ["reversal"],
    "valor": ["valor", "valor fightwear"],
    "flowhold": ["flowhold"],
    "senso": ["senso"],
    "kahuna": ["kahuna"],
    "combat corner": ["combat corner"],
    "break point": ["break point", "breakpoint"],
    "lanky fight gear": ["lanky", "lanky fight gear"],
    "moya brand": ["moya", "moya brand"],
    "vulkan": ["vulkan"],
    "keiko": ["keiko", "keiko raca"],
    "the gi company": ["the gi company"],
    "venator": ["venator"],
    "datsusara": ["datsusara", "ds gear"],
    "reevo": ["reevo"],
    "bull terrier": ["bull terrier"],
    "dojo outfitters": ["dojo outfitters"],
    "dojo pro": ["dojo pro"],
    "shark kimonos": ["shark kimonos"],
    "gr1ps": ["gr1ps"],
    "reorg": ["reorg"],
    "xguard": ["xguard"],
    "phantom athletics": ["phantom athletics", "phantom"],
    "stormstrong": ["stormstrong"],
    "killer bee": ["killer bee", "killerbee"],
    "impact jiu jitsu": ["impact", "impact jiu jitsu"],
    "ground game": ["ground game"],
    "oks": ["oks", "oks gi"],
    "astra": ["astra"],
    "nobull": ["nobull"],
    "revgear": ["revgear"],
    "dojo wear": ["dojo wear"],
    "sabak": ["sabak"],
    "koral": ["koral"],
    "meerkatsu": ["meerkatsu"],
}

# Common review phrases
review_phrases = [
    "shrinks a lot", "great quality", "terrible quality", "worth the price",
    "super lightweight", "too stiff", "fits perfectly", "fell apart",
    "best gi", "highly recommend", "very comfortable", "good stitching",
    "poor stitching", "not durable", "washed well", "ripped easily",
    "lasted years", "cheap material", "feels premium", "runs small"
]

# Clean text
def clean(text):
    return str(text).lower()

df["cleaned_comment"] = df["comment"].apply(clean)

# Detect brands
def find_brands(text):
    found = []
    for brand, aliases in brand_aliases.items():
        if any(alias in text for alias in aliases):
            found.append(brand)
    return found

df["mentioned_brands"] = df["cleaned_comment"].apply(find_brands)

# Detect review phrases
df["matched_phrases"] = df["cleaned_comment"].apply(
    lambda text: [phrase for phrase in review_phrases if phrase in text]
)

# Sentiment scoring
df["sentiment_score"] = df["cleaned_comment"].apply(lambda x: TextBlob(x).sentiment.polarity)

def classify_sentiment(score):
    if score > 0.2:
        return "Positive"
    elif score < -0.2:
        return "Negative"
    else:
        return "Neutral"

df["sentiment"] = df["sentiment_score"].apply(classify_sentiment)

# Save final data
df.to_csv("bjj_gi_reviews_analyzed.csv", index=False)

# Print summary
from collections import Counter
brand_counter = Counter()
for brands in df["mentioned_brands"]:
    brand_counter.update(brands)

phrase_counter = Counter()
for phrases in df["matched_phrases"]:
    phrase_counter.update(phrases)

print("\n📈 Top Mentioned Brands:")
for brand, count in brand_counter.most_common(20):
    print(f"{brand.title()}: {count} mentions")

print("\n💬 Common Review Phrases:")
for phrase, count in phrase_counter.most_common(10):
    print(f"\"{phrase}\" — {count} times")

print("\n✅ Done! File saved as bjj_gi_reviews_analyzed.csv")
