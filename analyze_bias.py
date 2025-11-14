import pandas as pd
import json
from textblob import TextBlob

import glob

# Read ALL JSONL files from results/raw folder
data = []
for file in glob.glob("results/raw/*.jsonl"):
    with open(file, "r") as f:
        for line in f:
            data.append(json.loads(line))

# Converting the responses into a dataframe so it is easy to work with
df = pd.DataFrame(data)

# Checking how many responses I got for each prompt type
summary = df.groupby("prompt_index").size().reset_index(name="response_count")

# Doing a simple sentiment check to see if tone changes depending on the prompt framing
df["sentiment"] = df["response_text"].apply(lambda x: TextBlob(x).sentiment.polarity)

# Getting the average sentiment for each prompt (positive vs negative tone difference)
sentiment_summary = df.groupby("prompt_index")["sentiment"].mean().reset_index(name="avg_sentiment")

# Putting both summaries together to see everything clearly
report = summary.merge(sentiment_summary, on="prompt_index")
print("\n=== SENTIMENT SUMMARY BY PROMPT ===")
print(report)

# Saving the analysis so I can use it later in my final report
report.to_csv("results/analysis/sentiment_summary.csv", index=False)
print("\nSaved analysis: results/analysis/sentiment_summary.csv")