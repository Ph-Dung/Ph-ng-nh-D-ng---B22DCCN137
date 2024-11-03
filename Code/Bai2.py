import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('result.csv')
df['Min'] = df['Min'].str.replace(',', '').astype(int)

numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

top_bottom_players = {}

for col in numeric_columns:
    top_3 = df.nlargest(3, col)[['Player', col]]
    bottom_3 = df.nsmallest(3, col)[['Player', col]]
    top_bottom_players[col] = {
        'Top 3': top_3.to_dict(orient='records'),
        'Bottom 3': bottom_3.to_dict(orient='records')
    }

for stat, players in top_bottom_players.items():
    print(f"\n{stat} - Top 3:")
    for player in players['Top 3']:
        print(f"{player['Player']}: {player[stat]}")

    print(f"\n{stat} - Bottom 3:")
    for player in players['Bottom 3']:
        print(f"{player['Player']}: {player[stat]}")


team_stats = df[numeric_columns].groupby(df['Team']).agg(['median', 'mean', 'std'])
team_stats.columns = ['_'.join(col).strip() for col in team_stats.columns.values]
team_stats.to_csv('results2.csv')

highest_teams = {}
for stat in team_stats.columns:
    highest_teams[stat] = team_stats[stat].idxmax()

for stat, team in highest_teams.items():
    print(f"Đội bóng có {stat.replace('_', ' ')} cao nhất là: {team}")

mean_columns = [col for col in team_stats.columns if 'mean' in col]
best_team = team_stats[mean_columns].mean(axis=1).idxmax()
print(f"\nĐội bóng có phong độ tốt nhất giải Ngoại hạng Anh mùa 2023-2024 là: {best_team}")

numeric_data = df.select_dtypes(include=['float64', 'int64'])
total_histograms = len(numeric_data.columns)
num_figures = 87
hist_per_fig = max(1, total_histograms // num_figures + 1)
for fig_index in range(num_figures):
    num_plots = min(hist_per_fig, total_histograms - fig_index * hist_per_fig)
    if num_plots <= 0:
        break
    fig, axes = plt.subplots(num_plots, 1, figsize=(12, 6 * num_plots))
    if not isinstance(axes, np.ndarray):
        axes = [axes]
    for i in range(num_plots):
        col = numeric_data.columns[fig_index * hist_per_fig + i]
        axes[i].hist(numeric_data[col].dropna(), bins=20, color='skyblue', edgecolor='black')
        axes[i].set_title(f'Histogram of {col}', fontsize=16)
        axes[i].set_xlabel(col, fontsize=14)
        axes[i].set_ylabel('Frequency', fontsize=14)
        axes[i].grid(axis='y', alpha=0.75)
    plt.subplots_adjust(hspace=0.5)
    plt.tight_layout(pad=2.0)
    plt.savefig(f'histograms_page_{fig_index + 1}.png')
    plt.close(fig)
