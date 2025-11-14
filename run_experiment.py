import os, json, time, argparse, getpass
from datetime import datetime

PROMPTS_FILE = "prompts.txt"

def read_prompts(path):
    prompts = []
    with open(path, "r", encoding="utf-8") as f:
        buf = []
        for line in f:
            # treat lines that start with "H" or "-" as content too
            if line.strip() == "":
                continue
            buf.append(line.rstrip("\n"))
        if buf:
            # split on numbered bullets if present, else keep as one
            text = "\n".join(buf)
            # simple split: each prompt separated by a line starting with "H" or "Prompt"
            # if your prompts are listed as bullets, this still works since we record whole file per line
            for block in text.split("##"):
                b = block.strip()
                if len(b) > 0:
                    prompts.append(b)
    # fallback: if that split made too many pieces, just keep whole file as one prompt
    if len(prompts) == 0:
        with open(path, "r", encoding="utf-8") as f:
            prompts = [f.read()]
    return prompts

def ensure_dirs():
    os.makedirs("results/raw", exist_ok=True)
    os.makedirs("results/meta", exist_ok=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, help="Name of the LLM used, e.g., GPT-4, Claude-3, Gemini")
    parser.add_argument("--samples", type=int, default=3, help="Responses per prompt")
    parser.add_argument("--operator", default=None, help="Your initials")
    args = parser.parse_args()

    operator = args.operator or getpass.getuser()
    ensure_dirs()
    prompts = read_prompts(PROMPTS_FILE)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_path = f"results/raw/{args.model.replace(' ','_').lower()}_{ts}.jsonl"
    meta_path = f"results/meta/session_{ts}.json"

    session_meta = {
        "timestamp_utc": ts,
        "model": args.model,
        "operator": operator,
        "prompts_file": PROMPTS_FILE,
        "samples_per_prompt": args.samples,
        "mode": "manual_paste"
    }
    with open(meta_path, "w", encoding="utf-8") as m:
        json.dump(session_meta, m, indent=2)

    print(f"\nSession started for model: {args.model}")
    print(f"Outputs will be saved to: {out_path}\n")

    with open(out_path, "w", encoding="utf-8") as out:
        for p_idx, prompt in enumerate(prompts, start=1):
            print("="*80)
            print(f"PROMPT {p_idx}")
            print("-"*80)
            print(prompt[:1200] + ("..." if len(prompt) > 1200 else ""))
            print("-"*80)

            for s in range(1, args.samples + 1):
                input(f"\nOpen {args.model}, paste the prompt, get the response, then press Enter to paste it here...")
                print(f"Paste RESPONSE for prompt {p_idx}, sample {s}. Finish with a single line that says: END")
                lines = []
                while True:
                    try:
                        line = input()
                    except EOFError:
                        break
                    if line.strip() == "END":
                        break
                    lines.append(line)
                response_text = "\n".join(lines)

                record = {
                    "timestamp_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "model": args.model,
                    "operator": operator,
                    "prompt_index": p_idx,
                    "prompt_text": prompt,
                    "sample_index": s,
                    "response_text": response_text
                }
                out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
                print(f"Saved sample {s} for prompt {p_idx}.")

    print("\nAll done. Logs written.")
    print("Next: git add results/raw results/meta && git commit && git push")

if __name__ == "__main__":
    main()
