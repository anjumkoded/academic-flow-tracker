# Plot Visual - Fixed Typography & Layout Spacing
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(8, 4.2), facecolor='#0B0C10')
ax.set_facecolor('#11131A')

weeks_labels = [f"W{i}" for i in range(1, 21)]
valid_x = []
valid_y = []

for i in range(1, 21):
    val = data[str(i)]
    if val is not None:
        valid_x.append(f"W{i}")
        valid_y.append(val)

# Ambient Baseline at 150
ax.axhline(y=150, color='#F87171', linestyle=':', linewidth=1.2, alpha=0.6, label='Baseline (150)')

if valid_x:
    ax.plot(
        valid_x, valid_y, 
        marker='o', markersize=6, markerfacecolor='#818CF8', markeredgecolor='#FFFFFF', markeredgewidth=1.2,
        color='#6366F1', linewidth=2.5, 
        label='Flow Horizon'
    )
    for x_val, y_val in zip(valid_x, valid_y):
        ax.annotate(
            f"{int(y_val)}", (x_val, y_val), 
            textcoords="offset points", 
            xytext=(0, 9), ha='center', 
            fontfamily='sans-serif', fontweight='700', fontsize=9, color='#FFFFFF'
        )

# Y-Axis & X-Axis Spacing Fixes
ax.set_ylim(0, 330)
ax.set_xlim(-0.8, 19.8)
ax.set_xticks(range(20))

# Show x-axis labels with proper padding & alternate step or smaller font for mobile
ax.set_xticklabels(weeks_labels, color='#9CA3AF', fontsize=7.5, fontweight='600')
ax.tick_params(axis='x', pad=6)
ax.tick_params(axis='y', colors='#6B7280', labelsize=8)

# Clean minimalist borders
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)

ax.grid(True, linestyle='--', alpha=0.08, color='#FFFFFF')

# High-contrast, clean legend positioned at the top right to avoid overlap
ax.legend(
    loc='upper right', 
    frameon=True, 
    facecolor='#161822', 
    edgecolor='rgba(255, 255, 255, 0.1)', 
    labelcolor='#E0E2EC', 
    fontsize=8.5,
    prop={'weight': '600', 'size': 8.5}
)

plt.tight_layout()

# Render Chart
st.pyplot(fig)
