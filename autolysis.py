import os
import pandas as pd # type: ignore
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from subprocess import run
import sys
import subprocess

# Constants
GPT4_MINI_API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDE0NzVAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.VqMP1WNW5f7OqHkwrDTkabWnLwGIXcurXQtqrCAs_6I"  # Replace with your API key
OUTPUT_DIR = "."  # Current directory
SAMPLE_SIZE = 50  # Number of rows to send to LLM
IMAGE_SIZE = (6, 6)  # For low-detail images
DPI = 50  # Low DPI for cost-effective visuals

# Ensure dependencies
try:
    from tabulate import tabulate
except ImportError:
    print("Installing 'tabulate' module...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
    from tabulate import tabulate


# Functions
def send_request_to_llm(prompt):
    """
    Sends a prompt to GPT-4 Mini using HTTP and returns the response.
    """
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

    response = requests.post(GPT4_MINI_API_URL, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    response_data = response.json()
    return response_data["choices"][0]["message"]["content"]


def write_readme(summary, charts, llm_insights, output_dir):
    """
    Create a README.md file with analysis results, embedding charts as images.
    """
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:  # Ensure UTF-8 encoding
        f.write("# Dataset Analysis Report\n\n")
        f.write("## Summary Statistics\n")
        f.write(summary.to_markdown() + "\n\n")
        f.write("## Insights from LLM\n")
        f.write(llm_insights + "\n\n")
        f.write("## Visualizations\n")
        for chart in charts:
            image_name = os.path.basename(chart)
            f.write(f"### {image_name}\n")
            f.write(f"![Visualization]({image_name})\n\n")  # Embed image in markdown

    return readme_path



def get_sample_analysis(data):
    """
    Extract a sample of the data and send it to LLM for insights.
    """
    sample_data = data.sample(n=SAMPLE_SIZE).to_csv(index=False)

    prompt = f"""
I have a sample dataset with the following rows:
{sample_data}

Can you provide insights, patterns, or interesting observations from this dataset?
Please ensure your response is concise yet detailed.
"""
    return send_request_to_llm(prompt)



def perform_analysis(data, output_dir):
    """
    Perform data analysis including correlation analysis, regression, and visualizations.
    Returns a summary dataframe and a list of generated chart file paths.
    """
    summary = data.describe(include="all")  # Summary statistics

    # Select numeric columns for correlation analysis
    numeric_data = data.select_dtypes(include=["number"])
    correlations = numeric_data.corr()  # Correlation matrix

    charts = []

    # Save correlation heatmap
    if not correlations.empty:
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlations, annot=True, fmt=".2f", cmap="coolwarm")
        correlation_path = os.path.join(output_dir, "correlation_heatmap.png")
        plt.savefig(correlation_path)
        plt.close()
        charts.append(correlation_path)

    # Example scatterplot for first two numeric columns
    numeric_cols = numeric_data.columns
    if len(numeric_cols) >= 2:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=data[numeric_cols[0]], y=data[numeric_cols[1]])
        scatter_path = os.path.join(output_dir, "scatterplot.png")
        plt.savefig(scatter_path)
        plt.close()
        charts.append(scatter_path)

    return summary, charts


    # Example scatterplot for first two numeric columns
    numeric_cols = data.select_dtypes(include=["number"]).columns
    if len(numeric_cols) >= 2:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=data[numeric_cols[0]], y=data[numeric_cols[1]])
        scatter_path = os.path.join(output_dir, "scatterplot.png")
        plt.savefig(scatter_path)
        plt.close()
        charts.append(scatter_path)

    return summary, charts



def write_readme(summary, charts, llm_insights, output_dir):
    """
    Create a README.md file with analysis results.
    """
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, "w") as f:
        f.write("# Dataset Analysis Report\n\n")
        f.write("## Summary Statistics\n")
        f.write(summary.to_markdown() + "\n\n")
        f.write("## Insights from LLM\n")
        f.write(llm_insights + "\n\n")
        f.write("## Visualizations\n")
        for chart in charts:
            image_name = os.path.basename(chart)
            f.write(f"### {image_name}\n")
            f.write(f"![Visualization]({image_name})\n\n")  # Embeds the image in markdown

    return readme_path


def push_to_github(output_dir):
    """
    Push results to a GitHub repository.
    """
    run(["git", "add", "."], cwd=output_dir)
    run(["git", "commit", "-m", "Updated analysis results"], cwd=output_dir)
    run(["git", "push"], cwd=output_dir)


# Main Function
def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load dataset
    data_path = "dataset.csv"  # Replace with your dataset file path
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"{data_path} not found.")
    data = pd.read_csv(data_path)

    # Perform analysis
    summary, charts = perform_analysis(data, OUTPUT_DIR)

    # Get LLM insights
    print("Sending sample data to LLM for insights...")
    llm_insights = get_sample_analysis(data)

    # Write README
    print("Writing README...")
    readme_path = write_readme(summary, charts, llm_insights, OUTPUT_DIR)

    # Push to GitHub
    print("Pushing results to GitHub...")
    push_to_github(OUTPUT_DIR)

    print(f"Analysis complete. Results saved to {readme_path}.")


if __name__ == "__main__":
    main()
