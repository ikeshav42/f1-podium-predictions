"""Draw the podium card for a race from a predictions csv.

usage: python make_card.py predictions/brazil_2026.csv "Brazilian GP 2026" "subtitle" images/brazil_podium_card.png
"""
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch

BG, FG, MUTED, RED, GREY = '#14161a', '#f2f3f5', '#9aa0a6', '#F04747', '#4a4f57'
TEAMS = {'Red Bull Racing': 'Red Bull', 'Haas F1 Team': 'Haas'}
NAMES = {'RUS': 'Russell', 'NOR': 'Norris', 'VER': 'Verstappen', 'LEC': 'Leclerc', 'ANT': 'Antonelli',
         'HAM': 'Hamilton', 'LAW': 'Lawson', 'HAD': 'Hadjar', 'PIA': 'Piastri', 'HUL': 'Hulkenberg',
         'BEA': 'Bearman', 'ALO': 'Alonso', 'ALB': 'Albon', 'SAI': 'Sainz', 'GAS': 'Gasly'}

csv_path, title, subtitle, out_path = sys.argv[1:5]


def pct(p):
    return f'{int(p * 100 + 0.5)}%'

top = pd.read_csv(csv_path).head(6)
first, second, third = top.iloc[0], top.iloc[1], top.iloc[2]

plt.rcParams['font.family'] = 'DejaVu Sans'
fig = plt.figure(figsize=(10.8, 10.8), dpi=100, facecolor=BG)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 10.8)
ax.set_ylim(0, 10.8)
ax.axis('off')

ax.text(0.6, 10.0, title, color=FG, fontsize=30, fontweight='bold')
ax.text(0.6, 9.5, subtitle, color=MUTED, fontsize=17)

base = 3.7
steps = [('P2', second, 0.9, 2.4), ('P1', first, 3.9, 3.4), ('P3', third, 6.9, 1.8)]
for label, row, x, height in steps:
    ax.add_patch(FancyBboxPatch((x, base), 3.0, height, boxstyle='round,pad=0,rounding_size=0.08',
                                fc=RED if label == 'P1' else GREY, ec='none'))
    ax.text(x + 1.5, base + height - 0.75, label, color=FG, fontsize=34, fontweight='bold', ha='center')
    ax.text(x + 1.5, base + height - 1.35, pct(row.podium_chance), color=FG, fontsize=20, ha='center')
    ax.text(x + 1.5, base + height + 0.55, NAMES.get(row.driver, row.driver), color=FG, fontsize=23, fontweight='bold', ha='center')
    ax.text(x + 1.5, base + height + 0.15, TEAMS.get(row.team_name, row.team_name),
            color=MUTED, fontsize=15, ha='center')

ax.text(5.4, 2.45, 'Podium chance = estimated probability of finishing in the top 3', color=MUTED,
        fontsize=13, ha='center')
rest = '  ·  '.join(f"{NAMES.get(r.driver, r.driver)} {pct(r.podium_chance)}" for r in top.iloc[3:6].itertuples())
ax.text(5.4, 1.85, f'Next in line:  {rest}', color=FG, fontsize=15, ha='center')
ax.text(5.4, 0.4, 'Data: OpenF1, Jolpica', color=GREY, fontsize=12, ha='center')

fig.savefig(out_path, facecolor=BG)
