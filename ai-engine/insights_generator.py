import pandas as pd
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_insights(file_path):
    df = pd.read_csv(file_path)

    avg = df['elapsed'].mean()
    p95 = df['elapsed'].quantile(0.95)
    error_rate = (df['success'] == False).mean() * 100

    prompt = f"""
    Analyze performance test results:

    Avg Response Time: {avg}
    P95 Response Time: {p95}
    Error Rate: {error_rate}%

    Provide:
    1. System health
    2. Possible bottlenecks
    3. Recommendations
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    insights = response['choices'][0]['message']['content']

    with open("../results/ai_report.txt", "w") as f:
        f.write(insights)

    print("\n✅ AI Insights Generated")

if __name__ == "__main__":
    generate_insights("../results/raw/results.jtl")