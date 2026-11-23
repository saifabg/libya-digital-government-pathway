"""Figure: Readiness-gated digital government pathway for Libya (framework/fig_framework.png).

Run from the study folder:  python -I code/07_framework_figure.py
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

os.makedirs('framework', exist_ok=True)
plt.rcParams.update({'font.family': 'Arial'})
fig, ax = plt.subplots(figsize=(11, 6.4))
ax.set_xlim(0.3, 11.2); ax.set_ylim(0, 6.4); ax.axis('off')

stages = [
    ('Stage 1', 'Foundations', ['Reconciled civil registry', 'National digital identity (LY-DNID)', 'Data exchange between agencies', 'E-payment', 'Data-protection and e-transactions law', 'Secure government web estate']),
    ('Stage 2', 'Quick-win services', ['4-5 high-volume services', 'fully online end to end', 'e.g. company registration, tax,', 'electricity payment, civil-status', 'extracts, birth certificates', 'Back office redesigned first']),
    ('Stage 3', 'Scale and include', ['Extend to remaining services', 'Assisted digital channels', '(banks, post offices,', 'municipal service houses)', 'Delivery to the door', 'Once-only data reuse']),
]
x0, w, gap = 0.55, 2.95, 0.55
for i, (tag, title, items) in enumerate(stages):
    x = x0 + i * (w + gap)
    ax.add_patch(FancyBboxPatch((x, 1.55), w, 3.2, boxstyle='round,pad=0.02,rounding_size=0.08', fc='white', ec='black', lw=1.3))
    ax.text(x + w / 2, 4.45, tag, ha='center', fontsize=9, color='#444444')
    ax.text(x + w / 2, 4.12, title, ha='center', fontsize=11.5, fontweight='bold')
    for k, it in enumerate(items):
        ax.text(x + 0.15, 3.68 - k * 0.33, ('• ' if not it[0].islower() and not it.startswith('(') else '   ') + it, fontsize=8.6, va='center')
    if i < len(stages) - 1:
        gx = x + w + gap / 2
        ax.add_patch(FancyArrowPatch((x + w + 0.03, 3.15), (x + w + gap - 0.03, 3.15), arrowstyle='-|>', mutation_scale=14, color='black', lw=1.2))
        ax.text(gx, 3.42, f'Gate {i + 1}', ha='center', fontsize=8, fontweight='bold')

# Stage 0 band
ax.add_patch(FancyBboxPatch((0.55, 5.0), 9.95, 0.95, boxstyle='round,pad=0.02,rounding_size=0.08', fc='#d9d9d9', ec='black', lw=1.3))
ax.text(5.52, 5.68, 'Stage 0  Governance compact', ha='center', fontsize=11.5, fontweight='bold')
ax.text(5.52, 5.2, 'One lead body with a legal mandate and a protected multi-year budget  •  common standards agreed' + chr(10) + 'across administrations  •  an IT lead and an e-government committee in every ministry',
        ha='center', va='center', fontsize=8.4, linespacing=1.3)
# Stage 4 band
ax.add_patch(FancyBboxPatch((0.55, 0.35), 9.95, 0.95, boxstyle='round,pad=0.02,rounding_size=0.08', fc='#efefef', ec='black', lw=1.3))
ax.text(5.52, 1.03, 'Stage 4  Measure and learn (continuous)', ha='center', fontsize=11.5, fontweight='bold')
ax.text(5.52, 0.56, 'Published service KPIs  •  annual portal audit (12 services, criteria C1–C12)  •  compliance audits' + chr(10) + 'of agencies  •  UN Online Services Index tracked as an outcome, not the target',
        ha='center', va='center', fontsize=8.4, linespacing=1.3)
# feedback arrow
ax.add_patch(FancyArrowPatch((10.78, 0.85), (10.78, 5.45), arrowstyle='-|>', mutation_scale=13, color='#555555', lw=1.1))
ax.text(10.95, 3.15, 'feedback', rotation=90, ha='center', va='center', fontsize=8, color='#555555')
fig.savefig(os.path.join('framework', 'fig_framework.png'), dpi=300, bbox_inches='tight')
print('saved framework/fig_framework.png')
