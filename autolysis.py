# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests",
#   "argparse",
#   "pandas",
#   "matplotlib",
#   "seaborn",
#   "tabulate",
#   "scikit-learn",
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
from sklearn.linear_model import LinearRegression # type: ignore
from sklearn.cluster import KMeans # type: ignore

# Constants
GPT4o_MINI_API_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
API_KEY = os.environ["AIPROXY_TOKEN"]
OUTPUT_DIR = "."  # Current directory
SAMPLE_SIZE = 50  # Number of rows to send to LLM
IMAGE_SIZE = (6, 6)  # For low-detail images
DPI = 50  # Low DPI for cost-effective visuals


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
    if 'monthlyCost' in response_data:
        print(f"Monthly Cost: {response_data['monthlyCost']}")
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


def perform_regression(data, x_col, y_col, output_dir):
    X = data[[x_col]].dropna()
    y = data[y_col].dropna()
    
    if X.empty or y.empty:
        return None

    model = LinearRegression()
    model.fit(X, y)
    prediction = model.predict(X)

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=X[x_col], y=y)
    plt.plot(X[x_col], prediction, color='red', label="Regression Line")
    plt.title(f"Linear Regression: {x_col} vs {y_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.legend()
    plt.tight_layout()
    regression_path = os.path.join(output_dir, "regression_plot.png")
    plt.savefig(regression_path, bbox_inches='tight')
    plt.close()

    return regression_path


def perform_clustering(data, n_clusters, output_dir):
    numeric_data = data.select_dtypes(include=["number"]).dropna()
    if numeric_data.empty:
        return None

    model = KMeans(n_clusters=n_clusters, n_init=10)
    clusters = model.fit_predict(numeric_data)

    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=numeric_data.iloc[:, 0], y=numeric_data.iloc[:, 1], hue=clusters, palette="viridis")
    plt.title(f"KMeans Clustering (k={n_clusters})")
    plt.xlabel(numeric_data.columns[0])
    plt.ylabel(numeric_data.columns[1])
    plt.tight_layout()
    cluster_path = os.path.join(output_dir, "cluster_plot.png")
    plt.savefig(cluster_path, bbox_inches='tight')
    plt.close()

    return cluster_path


def perform_analysis(data, output_dir):
    summary = data.describe(include="all")
    numeric_data = data.select_dtypes(include=["number"])
    correlations = numeric_data.corr()

    charts = []

    if not correlations.empty:
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlations, annot=True, fmt=".2f", cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "correlation_heatmap.png"), bbox_inches='tight')
        plt.close()
        charts.append("correlation_heatmap.png")

    numeric_cols = numeric_data.columns
    if len(numeric_cols) >= 2:
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=data[numeric_cols[0]], y=data[numeric_cols[1]])
        plt.title(f"Scatterplot: {numeric_cols[0]} vs {numeric_cols[1]}")
        plt.xlabel(numeric_cols[0])
        plt.ylabel(numeric_cols[1])
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "scatterplot.png"), bbox_inches='tight')
        plt.close()
        charts.append("scatterplot.png")

    regression_path = perform_regression(data, numeric_cols[0], numeric_cols[1], output_dir)
    if regression_path:
        charts.append("regression_plot.png")

    cluster_path = perform_clustering(data, 3, output_dir)
    if cluster_path:
        charts.append("cluster_plot.png")

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
    write_readme(summary, charts, llm_insights, OUTPUT_DIR)

    print("Analysis complete.")

if __name__ == "__main__":
    main()
