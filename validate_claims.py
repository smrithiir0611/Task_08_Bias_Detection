import pandas as pd
import json
from pathlib import Path

# This is the WNBA team stats file I used earlier
CSV_FILE = "teamstats.csv"

# This is the JSONL file where I stored all LLM responses for Task 8
RESULTS_FILE = "results/raw/gpt-4_20251101T025528Z.jsonl"

BASE_YEAR = 2018
END_YEAR = 2022

# 1. Rebuild the "ground truth" from the data
# ------------------------------------------------

# Reading the WNBA data again to know the actual numbers
df = pd.read_csv(CSV_FILE)

# If a team has multiple rows per season, I combine them (same logic as analyse_data.py)
agg_funcs = {
    "gp": "sum",
    "w": "sum",
    "l": "sum",
    "win_percent": "mean",
    "ppg": "mean",
    "fgm": "mean",
    "fga": "mean",
    "fg_percent": "mean",
    "threepoint_fgm": "mean",
    "threepoint_fga": "mean",
    "threepoint_fg_percent": "mean",
    "ftm": "mean",
    "fta": "mean",
    "ft_percent": "mean",
    "oreb": "mean",
    "dreb": "mean",
    "reb": "mean",
    "ast": "mean",
    "tov": "mean",
    "stl": "mean",
    "blk": "mean",
    "pf": "mean",
    "pfd": "mean",
}
team_year = (
    df.groupby(["team", "season"], as_index=False)
      .agg(agg_funcs)
)

# Finding the most improved team (2018 → 2022) using win_percent
base = team_year[team_year["season"] == BASE_YEAR][["team", "win_percent"]].rename(
    columns={"win_percent": f"winpct_{BASE_YEAR}"}
)
end = team_year[team_year["season"] == END_YEAR][["team", "win_percent"]].rename(
    columns={"win_percent": f"winpct_{END_YEAR}"}
)
improve = (
    end.merge(base, on="team", how="inner")
       .assign(improvement=lambda d: d[f"winpct_{END_YEAR}"] - d[f"winpct_{BASE_YEAR}"])
       .sort_values("improvement", ascending=False, ignore_index=True)
)

most_improved_team = improve.iloc[0]["team"]

# Top team by total wins across all seasons
total_wins = (
    team_year.groupby("team", as_index=False)["w"].sum()
             .rename(columns={"w": "total_wins"})
             .sort_values("total_wins", ascending=False, ignore_index=True)
)
top_wins_team = total_wins.iloc[0]["team"]

print("Ground truth check:")
print(f"- Most improved team (win%): {most_improved_team}")
print(f"- Top team by total wins: {top_wins_team}")

# 2. Load the LLM responses
# ------------------------------------------------

# Reading all saved LLM responses for this experiment
results_path = Path(RESULTS_FILE)
if not results_path.exists():
    raise FileNotFoundError(f"Could not find results file: {RESULTS_FILE}")

rows = []
with open(results_path, "r") as f:
    for line in f:
        if line.strip():
            rows.append(json.loads(line))

responses_df = pd.DataFrame(rows)

# 3. Very simple validation against ground truth
# ------------------------------------------------

# Here I am just checking if the response text mentions the correct team names.
# This is not a perfect check, but it shows if the model at least points to the right team.

def mentions_team(text: str, team_name: str) -> bool:
    if not isinstance(text, str):
        return False
    return team_name.lower() in text.lower()

responses_df["mentions_most_improved_team"] = responses_df["response_text"].apply(
    lambda x: mentions_team(x, most_improved_team)
)

responses_df["mentions_top_wins_team"] = responses_df["response_text"].apply(
    lambda x: mentions_team(x, top_wins_team)
)

# Showing how many responses got each fact "right" in a basic way
summary = responses_df.groupby("prompt_index")[[
    "mentions_most_improved_team",
    "mentions_top_wins_team"
]].mean().reset_index()

print("\n=== VALIDATION SUMMARY (basic check) ===")
print(summary)

# Saving the validation results so I can refer to them in the final report
output_dir = Path("results/analysis")
output_dir.mkdir(parents=True, exist_ok=True)

responses_df.to_csv(output_dir / "llm_responses_with_flags.csv", index=False)
summary.to_csv(output_dir / "validation_summary.csv", index=False)

print("\nSaved:")
print("- results/analysis/llm_responses_with_flags.csv")
print("- results/analysis/validation_summary.csv")
