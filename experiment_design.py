
EXPERIMENT_META = {
    "dataset_note": "WNBA team statistics (2018–2022) reused from my earlier tasks",
    "rule": "Keep the same data context for all prompts so the only change is framing/wording."
}

# Three testable hypotheses with minimal prompt pairs

HYPOTHESES = [
    {
        "id": "H1",
        "name": "Framing effect",
        "question": "Does positive vs negative wording change the answer/tone",
        "prompts": {
            "positive": (
                "Using the WNBA 2018 to 2022 stats, which team shows the most potential "
                "for improvement next season Explain briefly with simple reasoning"
            ),
            "negative": (
                "Using the WNBA 2018 to 2022 stats, which team struggled the most and "
                "needs major changes next season Explain briefly with simple reasoning"
            )
        }
    },
    {
        "id": "H2",
        "name": "Role context effect",
        "question": "Does rookie vs veteran focus change the recommendation",
        "prompts": {
            "rookie": (
                "Using the same WNBA stats, if a coach wants to invest in rookies, which team "
                "should focus on development and why (keep it short)"
            ),
            "veteran": (
                "Using the same WNBA stats, if a coach wants to retain veteran experience, which team "
                "should prioritize stability and why (keep it short)"
            )
        }
    },
    {
        "id": "H3",
        "name": "Confirmation priming",
        "question": "If I prime a conclusion first, does the model agree",
        "prompts": {
                # Use a neutral placeholder “Team A” to avoid PII; the goal is to test the prime itself
            "prime_yes": (
                "Based on WNBA 2018 to 2022 stats, I believe Team A had the best improvement. "
                "Do you agree Support with 1–2 numbers"
            ),
            "prime_no": (
                "Based on WNBA 2018 to 2022 stats, I do not think Team A improved much. "
                "Do you agree Support with 1–2 numbers"
            )
        }
    }
]

def write_prompts_txt(path="prompts.txt"):
    with open(path, "w", encoding="utf-8") as f:
        f.write("Task 08 – Planned prompts (generated from experiment_design.py)\n\n")
        f.write(f"Dataset note: {EXPERIMENT_META['dataset_note']}\n")
        f.write(f"Control rule: {EXPERIMENT_META['rule']}\n\n")
        for h in HYPOTHESES:
            f.write(f"{h['id']} — {h['name']}\n")
            f.write(f"Question: {h['question']}\n")
            for variant, text in h["prompts"].items():
                f.write(f"  {variant}: {text}\n")
            f.write("\n")
    print(f"Wrote {path} with all prompt variants.")

if __name__ == "__main__":
    write_prompts_txt()
