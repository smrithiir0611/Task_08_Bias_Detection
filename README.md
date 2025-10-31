# Task_08_Bias_Detection
Controlled experiment testing bias and framing effects in LLM-generated narratives using WNBA 2018–2022 data. 

This project explores how framing and context affect LLM-generated data narratives.  
Using WNBA performance data, I will test whether changing prompts — such as positive vs. negative framing or mentioning demographics — leads to measurable bias in model outputs.

## Objectives
- To design and execute controlled experiments to test for framing, demographic, and confirmation bias.
- To compare outputs from multiple LLMs (e.g., GPT-4, Claude).
- To analyze differences quantitatively and qualitatively.
- To document bias patterns and mitigation strategies.

## Structure
- `experiment_design.py`: Creates prompt variations.
- `run_experiment.py`: Runs LLM queries and logs outputs.
- `analyze_bias.py`: Quantitative and sentiment analysis.
- `validate_claims.py`: Compares model statements with real data.
- `prompts/`: Prompt templates.
- `results/`: Collected LLM responses.
- `analysis/`: Charts, tables, and reports.

## How to Run
1. Clone the repository.
2. Run `experiment_design.py` to generate prompt sets.
3. Use `run_experiment.py` to collect responses.
4. Analyze results with `analyze_bias.py`.
5. Validate findings using `validate_claims.py`.



