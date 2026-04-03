import pandas as pd

def detect_anomalies(file_path):
    df = pd.read_csv(file_path)

    if 'elapsed' not in df.columns:
        print("Invalid JMeter result file")
        return

    mean = df['elapsed'].mean()
    std = df['elapsed'].std()

    threshold = mean + (2 * std)

    anomalies = df[df['elapsed'] > threshold]

    print(f"\n🚨 Anomalies Found: {len(anomalies)}")
    print(anomalies[['timeStamp', 'elapsed', 'label']])

    return anomalies

if __name__ == "__main__":
    detect_anomalies("../results/raw/results.jtl")