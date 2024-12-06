import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import subprocess

# Set your GPT-4 Mini endpoint
GPT4_MINI_API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDE0NzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.VqMP1WNW5f7OqHkwrDTkabWnLwGIXcurXQtqrCAs_6I"


def send_request_to_llm(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    }
    response = requests.post(GPT4_MINI_API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]

def get_dataset_context(data):
    columns_info = data.dtypes.to_dict()
    num_rows = len(data)

    prompt = f"""
    I have a dataset with {num_rows} rows. Here are the columns and their data types:
    {columns_info}

    Based on this metadata:
    1. What could this dataset represent?
    2. What types of analyses should I perform to understand this data better?
    3. What visualizations might be useful?
    Respond concisely.
    """
    return send_request_to_llm(prompt)

def perform_local_analysis(data, output_dir):
    summary = data.describe(include="all").transpose()
    summary_path = os.path.join(output_dir, "summary.csv")
    summary.to_csv(summary_path)

    charts = []
    numeric_columns = data.select_dtypes(include=["number"]).columns
    for col in numeric_columns[:2]:  # Generate only 2 charts
        plt.figure(figsize=(6, 4))
        data[col].hist(color="skyblue", edgecolor="black")
        chart_path = os.path.join(output_dir, f"{col}.png")
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.savefig(chart_path, dpi=50)
        plt.close()
        charts.append(chart_path)
    return summary, charts

def refine_analysis_with_llm(summary, charts):
    summary_csv = summary.to_csv(index=True)

    prompt = f"""
    I performed the following analyses on the dataset:
    Summary statistics:
    {summary_csv}

    Visualizations:
    - {', '.join(charts)}

    What additional insights or suggestions can you provide based on this analysis?
    """
    return send_request_to_llm(prompt)

def commit_and_push_to_github(commit_message):
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Changes pushed to GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python autolysis.py <dataset.csv>")
        sys.exit(1)

    input_csv = sys.argv[1]
    if not os.path.isfile(input_csv):
        print(f"File not found: {input_csv}")
        sys.exit(1)

    data = pd.read_csv(input_csv)
    output_dir = os.getcwd()

    print("Sending dataset metadata to GPT-4 Mini for context...")
    context = get_dataset_context(data)
    print("LLM Suggestions:\n", context)

    print("Performing local analysis...")
    summary, charts = perform_local_analysis(data, output_dir)

    print("Refining analysis with GPT-4 Mini...")
    final_story = refine_analysis_with_llm(summary, charts)

    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write(final_story)
        f.write("\n\n## Visualizations\n")
        for chart in charts:
            f.write(f"![{os.path.basename(chart)}]({os.path.basename(chart)})\n")
    print(f"Analysis complete. Results saved to {readme_path}")

    print("Committing changes to GitHub...")
    commit_and_push_to_github("Automated analysis results added.")

if __name__ == "__main__":
    main()
