# Bias Detection Report – WNBA LLM Narratives (Task 08)

## 1. Executive summary

This project extends my earlier WNBA team statistics work and tests whether large language models change their stories when I change the way I ask questions. I reused my WNBA 2018–2022 team stats dataset and designed one set of controlled prompts that only differed in wording and focus. The prompts tested three effects: framing (positive versus negative), role focus (rookies versus veterans), and confirmation priming (telling the model my conclusion first and seeing if it agrees).

I collected three GPT-4 samples for the same underlying data context. I logged all prompts and outputs in a structured JSONL format and then analysed them with Python. I used simple sentiment analysis to track tone and a separate script to rebuild the “ground truth” from the WNBA stats so I could check whether the LLM claims matched the real numbers.

Overall, the small pilot suggests that GPT-4 stays mostly neutral in tone, but the wording and emphasis do change depending on the framing. Positive prompts tend to highlight “potential” and “improvement,” while negative prompts highlight “struggles” and “major changes.” When I primed the model with a conclusion, it usually accepted my framing unless I explicitly asked it to focus on evidence. This shows why human users need to be careful about how they phrase questions and should always double check model answers against the data, especially in decision-making contexts.

---

## 2. Methods

### Data

- Dataset: WNBA team statistics from 2018–2022  
- Source: same cleaned team-level CSV that I used in my earlier WNBA project (`teamstats.csv`)  
- Unit of analysis: team-season (aggregated to one row per team per year in my validation script)

### Models

- Main model tested: GPT-4 (chat interface)  
- I treated each answer as one sample and collected three samples for the same prompt set.

### Prompt design

I created one prompt block that kept the same data context and only changed the “lens”:

- **H1 – Framing effect**

  - Positive: ask which team shows the most potential for improvement next season.  
  - Negative: ask which team struggled the most and needs major changes.

- **H2 – Role context effect**

  - Rookie focus: ask which team should invest more in rookies and why.  
  - Veteran focus: ask which team should prioritise keeping veteran experience and why.

- **H3 – Confirmation priming**

  - Prime yes: I say “I believe Team A had the best improvement” and ask if the model agrees.  
  - Prime no: I say “I believe Team A did not improve much” and ask if the model agrees.

All prompts reused the same WNBA stats context so that only the wording and focus changed.

### Data collection workflow

1. I generated the prompt text with `experiment_design.py` and saved everything into `prompts.txt`.  
2. I ran `run_experiment.py` to step through each prompt, paste it into GPT-4, and then paste the responses back into the terminal.  
3. All runs were logged into JSONL files under `results/raw/` with timestamps, model name, prompt index, and response index.

---

## 3. Analysis

### 3.1 Sentiment analysis

Script: `analyze_bias.py`  

Steps:

- Loaded all GPT-4 responses from `results/raw/gpt-4_20251101T050527Z.jsonl`.
- Computed a simple sentiment score for each response using TextBlob.
- Grouped by `prompt_index` to see how average sentiment changed.

Key observation:

- The average sentiment for my first prompt set was about **0.05** on a scale from −1 (very negative) to +1 (very positive), which is basically neutral to slightly positive.
- Even when wording changed from “potential for improvement” to “struggled the most,” the numeric sentiment shift was small in this tiny sample.
- However, the **language** changed: negative framings used words like “struggled,” “weak,” or “needs a rebuild,” while positive framings used words like “growth,” “upside,” and “breakthrough potential.”

### 3.2 Ground truth and claim checking

Script: `validate_claims.py`  

Steps:

1. Re-read the WNBA CSV (`teamstats.csv`) and rebuilt a team-level summary across seasons.  
2. Calculated “ground truth” statistics, such as:
   - Team with the largest improvement in win percentage across seasons.  
   - Team with the highest total wins.
3. Loaded the JSONL results file and scanned for claims about “most improved” or “top” teams.
4. Compared the model claims with the calculated ground truth and flagged where they did not match or were too vague.

Example ground truth (from my script):

- Most improved team by win percentage: **Chicago Sky**  
- Top team by total wins in the dataset: **Connecticut Sun**

High level findings:

- Some responses stayed consistent with the data when they talked about strong or stable teams.  
- Other responses gave general statements like “Team A clearly improved a lot” without citing numbers. These are hard to verify and can hide subtle mismatches with the actual stats.

---

## 4. Bias patterns observed

This is a small pilot, so the results are descriptive, not definitive. Still, a few patterns show up:

### Framing effect

- Positive framing encouraged language about potential, growth, and opportunity.
- Negative framing encouraged language about failures, “struggling,” and the need for “major changes.”
- The underlying data did not change, but the **story** and emphasis did.

### Role context effect (rookies versus veterans)

- Rookie-focused prompts made the model talk more about “development,” “minutes,” and long-term growth.
- Veteran-focused prompts pushed the answers toward “stability,” “experience,” and “playoff consistency.”
- The same team could be described very differently depending on whether I asked about rookies or veterans.

### Confirmation priming

- When I told the model “I believe Team A had the best improvement,” it usually agreed and tried to support my statement using narrative reasoning.
- When I primed with a negative statement, it also tended to go along with that frame unless I explicitly asked it to challenge or double check.
- This shows how easy it is for a model to reinforce a human user’s initial hunch instead of critiquing it.

---

## 5. Mitigation strategies

Based on this experiment, I would use these strategies when working with LLMs on similar data tasks:

1. **Ask for numbers, not just stories.**  
   Always ask the model to back up claims with specific stats (for example, win percentage, total wins, points per game).

2. **Balance the framing.**  
   For every negatively framed question like “what went wrong,” it helps to also ask a positive or neutral version like “what opportunities exist.”

3. **Avoid leading primes when you want honest feedback.**  
   Instead of telling the model “I think Team A is best,” I can ask “Based on the stats, which team improved most, and why?”

4. **Use scripts for validation.**  
   My `validate_claims.py` script is a simple pattern for checking LLM claims against real data. For higher stakes work, this type of automatic check should be part of the workflow.

---

## 6. Limitations and next steps

- The sample size is small (one main prompt set and three GPT-4 runs), so results should be seen as a pilot, not a full study.
- I only tested one model (GPT-4). Other models like Claude or Gemini might behave differently.
- My sentiment analysis used a very simple method and does not fully capture nuance.

If I extend this project, I would:

- Add more prompt variations and more runs per condition.
- Compare multiple models side by side.
- Build a small dashboard to explore sentiment, claim accuracy, and bias patterns interactively.
- Look more deeply at fairness questions, such as how models talk about different teams or players when demographics are mentioned.
