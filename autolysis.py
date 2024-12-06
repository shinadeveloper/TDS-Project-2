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
GPT4_MINI_API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
API_KEY = os.environ["AIPROXY_TOKEN"] # Replace with your API key
OUTPUT_DIR = "."  # Current directory
SAMPLE_SIZE = 50  # Number of rows to send to LLM
IMAGE_SIZE = (6, 6)  # For low-detail images
DPI = 50  # Low DPI for cost-effective visuals


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


def get_sample_analysis(data):
    """
    Extract a sample of the data and send it to LLM for insights and storytelling.
    """
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


def write_readme(summary, charts, llm_insights, output_dir):
    """
    Create a README.md file with analysis results, embedding charts as images.
    """
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
            f.write(f"![Visualization]({image_name})\n\n")  # Embed image in markdown

    return readme_path


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Analyze a CSV file and generate a report.")
    parser.add_argument("csv_file", help="Path to the CSV file to analyze")
    args = parser.parse_args()

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load dataset with encoding handling
    if not os.path.exists(args.csv_file):
        raise FileNotFoundError(f"{args.csv_file} not found.")
    
    try:
        data = pd.read_csv(args.csv_file, encoding="utf-8")
    except UnicodeDecodeError:
        print("UTF-8 decoding failed. Trying 'ISO-8859-1' encoding.")
        data = pd.read_csv(args.csv_file, encoding="ISO-8859-1")
    
    # Perform analysis
    summary, charts = perform_analysis(data, OUTPUT_DIR)

    # Get LLM storytelling insights
    print("Sending sample data to LLM for insights and storytelling...")
    llm_insights = get_sample_analysis(data)

    # Write README
    print("Writing README...")
    readme_path = write_readme(summary, charts, llm_insights, OUTPUT_DIR)

    print(f"Analysis complete. Results saved to {readme_path}.")


if __name__ == "__main__":
    main()
