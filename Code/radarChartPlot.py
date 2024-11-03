
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

data = pd.read_csv('result.csv', encoding='utf-8')
def create_radar_chart(player1_data, player2_data, attributes, player1_name, player2_name):
    num_vars = len(attributes)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    player1_stats = player1_data[attributes].values.flatten().tolist()
    player1_stats += player1_stats[:1]
    ax.plot(angles, player1_stats, linewidth=1, linestyle='solid', label=player1_name)
    ax.fill(angles, player1_stats, alpha=0.25)

    player2_stats = player2_data[attributes].values.flatten().tolist()
    player2_stats += player2_stats[:1]
    ax.plot(angles, player2_stats, linewidth=1, linestyle='solid', label=player2_name)
    ax.fill(angles, player2_stats, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)

    plt.title(f"Comparison between {player1_name} and {player2_name}")
    plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

    plt.show()

parser = argparse.ArgumentParser(description="Radar chart comparison between two players.")
parser.add_argument("--p1", type=str, required=True, help="Name of the first player")
parser.add_argument("--p2", type=str, required=True, help="Name of the second player")
parser.add_argument("--Attribute", type=str, required=True, help="Comma-separated list of attributes to compare")

args = parser.parse_args()

player1_name = args.p1
player2_name = args.p2
attributes = [attr.strip() for attr in args.Attribute.split(",")]

player1_data = data[data["Player"] == player1_name]
player2_data = data[data["Player"] == player2_name]

if player1_data.empty or player2_data.empty:
    print("One or both players not found in the dataset. Please check the names.")
else:
    create_radar_chart(player1_data, player2_data, attributes, player1_name, player2_name)
