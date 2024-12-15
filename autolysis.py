# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "argparse",
#   "pandas",
#   "matplotlib",
#   "seaborn",
#   "tabulate",
# ]
# ///


import os
import sys
import argparse
import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore
import requests  # type: ignore
import json
from tabulate import tabulate  # type: ignore

# Constants
GPT4o_MINI_API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
VISION_API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/images"
API_KEY = os.environ["AIPROXY_TOKEN"] 
OUTPUT_DIR = "."  # Current directory
SAMPLE_SIZE = 50  # Number of rows to send to LLM
IMAGE_SIZE = (6, 6)  # For low-detail images
DPI = 100  

def analyze_image(image_path):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    files = {
        "file": open(image_path, "rb")
    }

    params = {
        "detail": "low"
    }

    response = requests.post(VISION_API_URL, headers=headers, files=files, data=params)
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")
    return response.json()

def send_request_to_llm(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a data analysis assistant."},
            {"role": "user", "content": prompt},
        ],
    }

    response = requests.post(GPT4o_MINI_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]


def get_sample_analysis(data):
    sample_data = data.sample(n=SAMPLE_SIZE).to_csv(index=False)
    prompt = f"""
I have a dataset sample as follows:
{sample_data}

Please provide the following:
1. Describe this dataset as a story (structure, purpose, and context).
2. Summarize the analysis performed (e.g., correlation, visualization).
3. Highlight the key insights discovered.
4. Discuss the implications of these findings and what actions can be taken based on them.
"""
    return send_request_to_llm(prompt)


def perform_analysis(data, output_dir):
    summary = data.describe(include="all")  # Summary statistics

    numeric_data = data.select_dtypes(include=["number"])
    correlations = numeric_data.corr()

    charts = []

    if not correlations.empty:
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlations, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.xlabel("Features")
        plt.ylabel("Features")
        plt.tight_layout()
        correlation_path = os.path.join(output_dir, "correlation_heatmap.png")
        plt.savefig(correlation_path, dpi=DPI)
        plt.close()
        charts.append(correlation_path)

    numeric_cols = numeric_data.columns
    if len(numeric_cols) >= 2:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=data[numeric_cols[0]], y=data[numeric_cols[1]])
        plt.title(f"Scatterplot: {numeric_cols[0]} vs {numeric_cols[1]}")
        plt.xlabel(numeric_cols[0])
        plt.ylabel(numeric_cols[1])
        plt.tight_layout()
        scatter_path = os.path.join(output_dir, "scatterplot.png")
        plt.savefig(scatter_path, dpi=DPI)
        plt.close()
        charts.append(scatter_path)

    return summary, charts


def write_readme(summary, charts, llm_insights, output_dir):
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("# Dataset Analysis Report\n\n")
        f.write("## Summary Statistics\n")
        f.write(summary.to_markdown() + "\n\n")
        f.write("## Insights from LLM\n")
        f.write(llm_insights + "\n\n")
        f.write("## Visualizations\n")
        for chart in charts:
            image_name = os.path.basename(chart)
            f.write(f"### {image_name}\n")
            f.write(f"![Visualization]({image_name})\n\n")

    return readme_path


def main():
    parser = argparse.ArgumentParser(description="Analyze a CSV file and generate a report.")
    parser.add_argument("csv_file", help="Path to the CSV file to analyze")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not os.path.exists(args.csv_file):
        raise FileNotFoundError(f"{args.csv_file} not found.")

    try:
        data = pd.read_csv(args.csv_file, encoding="utf-8")
    except UnicodeDecodeError:
        print("UTF-8 decoding failed. Trying 'ISO-8859-1' encoding.")
        data = pd.read_csv(args.csv_file, encoding="ISO-8859-1")

    summary, charts = perform_analysis(data, OUTPUT_DIR)

    llm_insights = get_sample_analysis(data)
    readme_path = write_readme(summary, charts, llm_insights, OUTPUT_DIR)

    print(f"Analysis complete. Results saved to {readme_path}.")


if __name__ == "__main__":
    main()
