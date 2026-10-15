import pandas as pd
import numpy as np


def process_benchmark_logs(file_path):
    # Load the CSV file
    df = pd.read_csv(file_path)

    # Drop rows where the prompt might be missing
    df = df.dropna(subset=['PROMPT'])

    # Categorize queries into Short and Long based on the < 100 character rule from bench2.py
    df['Type'] = np.where(df['PROMPT'].str.len() < 100, 'Short', 'Long')

    # Filter out error rows where TTFT or T/s is -1
    valid_df = df[(df['TTFT'] > 0) & (df['T/s'] > 0)]

    results = []

    # Group by the model name
    for model, group in valid_df.groupby('MODEL'):
        # 1. Average T/s across ALL valid queries
        avg_tps = group['T/s'].mean()

        # 2. Average TTFT separated by Short and Long queries
        short_ttft = group[group['Type'] == 'Short']['TTFT'].mean()
        long_ttft = group[group['Type'] == 'Long']['TTFT'].mean()

        # 3. Total time of testing per model
        # (Using the original df so we only count valid execution time, excluding error placeholders)
        total_time = df[(df['MODEL'] == model) & (df['TOTAL TIME'] > 0)]['TOTAL TIME'].sum()

        results.append({
            'Model': model,
            'Avg T/s (Overall)': round(avg_tps, 2),
            'Avg TTFT (Short)': round(short_ttft, 3),
            'Avg TTFT (Long)': round(long_ttft, 3),
            'Total Test Time (s)': round(total_time, 2)
        })

    # Convert to DataFrame and sort by T/s for readability
    summary_df = pd.DataFrame(results).sort_values(by='Total Test Time (s)', ascending=False)
    return summary_df


# Process both your RX 9070 XT and RTX 3060 files
amd_results = process_benchmark_logs("Vulkan_AMD_Radeon_RX_9070_XT.csv")
nvidia_results = process_benchmark_logs("Vulkan_NVIDIA_GeForce_RTX_3060.csv")

print("--- AMD Radeon RX 9070 XT Results ---")
print(amd_results.to_string(index=False))
amd_results.to_csv("amd.csv")
nvidia_results.to_csv("nvidia.csv")

print("\n--- NVIDIA GeForce RTX 3060 Results ---")
print(nvidia_results.to_string(index=False))