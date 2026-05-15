import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from networkx.algorithms.community import girvan_newman
import itertools

# ═══════════════════════════════════════════════════════════════
#              SOCIAL NETWORK ANALYSIS — ASSIGNMENT 2
#         Q1: Graph Metrics  |  Q2: Community Detection
# ═══════════════════════════════════════════════════════════════

# ── 1. LOAD DATASET ───────────────────────────────────────────
df = pd.read_csv("classroom_dataset.csv")
G  = nx.from_pandas_edgelist(df, source="Source", target="Target")

print("=" * 58)
print("       SOCIAL NETWORK ANALYSIS — ASSIGNMENT 2")
print("=" * 58)

print(f"\n── Dataset Loaded ──")
print(f"  Nodes  : {G.number_of_nodes()}")
print(f"  Edges  : {G.number_of_edges()}")
print(f"  Nodes  : {list(G.nodes())}")

# ── 2. Q1 — GRAPH METRICS ─────────────────────────────────────
print("\n" + "=" * 58)
print("  Q1 — GRAPH METRICS")
print("=" * 58)

# Degree
degree_dict  = dict(G.degree())
print("\n── Degree of Each Node ──")
print(f"  {'Node':<12} {'Degree':>8}")
print(f"  {'────':<12} {'──────':>8}")
for node, deg in sorted(degree_dict.items(), key=lambda x: -x[1]):
    print(f"  {node:<12} {deg:>8}  {'█' * deg}")

# Clustering Coefficient
local_clust  = nx.clustering(G)
avg_clust    = nx.average_clustering(G)
print("\n── Clustering Coefficient ──")
print(f"  {'Node':<12} {'Local CC':>10}")
print(f"  {'────':<12} {'────────':>10}")
for node, val in sorted(local_clust.items(), key=lambda x: -x[1]):
    print(f"  {node:<12} {val:>10.4f}  {'█' * int(val * 10)}")
print(f"\n  ★ Average Clustering Coefficient : {avg_clust:.4f}")

# Density
density = nx.density(G)
print(f"  ★ Graph Density                  : {density:.4f}")

# Other metrics
print(f"\n── Additional Metrics ──")
print(f"  Average Degree       : {sum(degree_dict.values())/G.number_of_nodes():.4f}")
print(f"  Network Diameter     : {nx.diameter(G)}")
print(f"  Avg Path Length      : {nx.average_shortest_path_length(G):.4f}")
print(f"  Is Connected         : {nx.is_connected(G)}")

# ── 3. Q2 — GIRVAN-NEWMAN ─────────────────────────────────────
print("\n" + "=" * 58)
print("  Q2 — GIRVAN-NEWMAN COMMUNITY DETECTION")
print("=" * 58)

# Edge betweenness
edge_bw = nx.edge_betweenness_centrality(G)
print("\n── Top Edge Betweenness (edges removed first) ──")
print(f"  {'Edge':<28} {'Betweenness':>12}")
print(f"  {'────':<28} {'───────────':>12}")
for edge, val in sorted(edge_bw.items(), key=lambda x: -x[1])[:6]:
    print(f"  {str(edge):<28} {val:>12.4f}")

# Run Girvan-Newman
comp       = girvan_newman(G)
all_levels = []
for level in itertools.islice(comp, 4):
    all_levels.append([sorted(c) for c in level])

# Print all levels
print("\n── Communities at Each Split Level ──")
for i, communities in enumerate(all_levels):
    print(f"\n  Level {i+1} → {len(communities)} communities:")
    for j, comm in enumerate(communities):
        print(f"    Group {j+1}: {', '.join(comm)}")

# Best partition
best = all_levels[2]
modularity = nx.community.modularity(G, best)
print(f"\n  ✔ Best Partition  : Level 3 → {len(best)} communities")
print(f"  ✔ Modularity Score: {modularity:.4f}")

# Node → community map
node_comm = {}
for idx, comm in enumerate(best):
    for node in comm:
        node_comm[node] = idx

# Edge analysis
intra = sum(1 for u,v in G.edges() if node_comm[u] == node_comm[v])
inter = G.number_of_edges() - intra
print(f"\n── Edge Analysis ──")
print(f"  Intra-community edges : {intra}")
print(f"  Inter-community edges : {inter}")
print(f"  Intra/Total ratio     : {intra}/{G.number_of_edges()} = {intra/G.number_of_edges():.2f}")

# ── 4. ALL VISUALIZATIONS ─────────────────────────────────────
print("\n" + "=" * 58)
print("  Generating all visualizations...")
print("=" * 58)

COLORS = ["#E74C3C","#2ECC71","#3498DB","#F39C12","#9B59B6"]
layout = nx.spring_layout(G, seed=42)
node_sizes = [300 + degree_dict[n] * 120 for n in G.nodes()]

fig, axes = plt.subplots(2, 3, figsize=(20, 12))
fig.suptitle("SNA Assignment 2 — Classroom Network Analysis",
             fontsize=16, fontweight="bold", y=1.01)

# ── Plot 1: Basic Graph ───────────────────────────────────────
ax = axes[0][0]
ax.set_title("Graph Structure", fontsize=12, fontweight="bold")
nx.draw_networkx_edges(G, layout, ax=ax, edge_color="#AAAAAA", width=1.5, alpha=0.7)
nx.draw_networkx_nodes(G, layout, ax=ax, node_size=node_sizes,
                       node_color="#4A90D9", alpha=0.9)
nx.draw_networkx_labels(G, layout, ax=ax, font_size=8,
                        font_color="white", font_weight="bold")
ax.set_axis_off()
ax.text(0.5,-0.04, f"Nodes: {G.number_of_nodes()}  Edges: {G.number_of_edges()}  (size = degree)",
        transform=ax.transAxes, ha="center", fontsize=9, color="gray")

# ── Plot 2: Clustering Heatmap ────────────────────────────────
ax = axes[0][1]
ax.set_title("Clustering Coefficient Heatmap", fontsize=12, fontweight="bold")
clust_vals = [local_clust[n] for n in G.nodes()]
sc = nx.draw_networkx_nodes(G, layout, ax=ax, node_size=node_sizes,
                             node_color=clust_vals, cmap=plt.cm.YlOrRd,
                             vmin=0, vmax=1, alpha=0.95)
nx.draw_networkx_edges(G, layout, ax=ax, edge_color="#CCCCCC", width=1.2, alpha=0.6)
nx.draw_networkx_labels(G, layout, ax=ax, font_size=8, font_weight="bold")
plt.colorbar(sc, ax=ax, shrink=0.7).set_label("Clustering Coefficient", fontsize=9)
ax.set_axis_off()
ax.text(0.5,-0.04, f"Avg Clustering = {avg_clust:.4f}",
        transform=ax.transAxes, ha="center", fontsize=9, color="gray")

# ── Plot 3: Degree Distribution ───────────────────────────────
ax = axes[0][2]
ax.set_title("Degree Distribution", fontsize=12, fontweight="bold")
nodes_s  = sorted(degree_dict, key=lambda x: -degree_dict[x])
degs_s   = [degree_dict[n] for n in nodes_s]
bcolors  = plt.cm.Blues([0.4 + 0.6*d/max(degs_s) for d in degs_s])
bars = ax.bar(nodes_s, degs_s, color=bcolors, edgecolor="white", linewidth=0.8)
for bar, deg in zip(bars, degs_s):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
            str(deg), ha="center", fontsize=8, fontweight="bold")
ax.set_xlabel("Student", fontsize=10)
ax.set_ylabel("Degree", fontsize=10)
ax.tick_params(axis="x", rotation=45, labelsize=8)
ax.set_ylim(0, max(degs_s)+2)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.spines[["top","right"]].set_visible(False)
ax.text(0.5,-0.22, f"Density = {density:.4f}",
        transform=ax.transAxes, ha="center", fontsize=9, color="gray")

# ── Plot 4: Original Graph (Q2 before) ───────────────────────
ax = axes[1][0]
ax.set_title("Original Graph\n(before community detection)", fontsize=12, fontweight="bold")
nx.draw_networkx_edges(G, layout, ax=ax, edge_color="#BBBBBB", width=1.5, alpha=0.8)
nx.draw_networkx_nodes(G, layout, ax=ax, node_size=600,
                       node_color="#4A90D9", alpha=0.9)
nx.draw_networkx_labels(G, layout, ax=ax, font_size=8,
                        font_color="white", font_weight="bold")
ax.set_axis_off()

# ── Plot 5: Community Detection ───────────────────────────────
ax = axes[1][1]
ax.set_title(f"Girvan-Newman Communities\n({len(best)} communities detected)",
             fontsize=12, fontweight="bold")
node_color_map = [COLORS[node_comm[n]] for n in G.nodes()]
intra_edges    = [(u,v) for u,v in G.edges() if node_comm[u]==node_comm[v]]
inter_edges    = [(u,v) for u,v in G.edges() if node_comm[u]!=node_comm[v]]
nx.draw_networkx_edges(G, layout, edgelist=inter_edges, ax=ax,
                       edge_color="#CCCCCC", width=1.0, alpha=0.5, style="dashed")
nx.draw_networkx_edges(G, layout, edgelist=intra_edges, ax=ax,
                       edge_color="#444444", width=2.2, alpha=0.8)
nx.draw_networkx_nodes(G, layout, ax=ax, node_size=650,
                       node_color=node_color_map, alpha=0.95)
nx.draw_networkx_labels(G, layout, ax=ax, font_size=8,
                        font_color="white", font_weight="bold")
patches = [mpatches.Patch(color=COLORS[i],
           label=f"G{i+1}: {', '.join(best[i])}") for i in range(len(best))]
ax.legend(handles=patches, loc="upper center",
          bbox_to_anchor=(0.5,-0.05), fontsize=7.5, ncol=1)
ax.set_axis_off()
ax.text(0.5,-0.22, f"Modularity = {modularity:.4f}",
        transform=ax.transAxes, ha="center", fontsize=9, color="gray")

# ── Plot 6: Community Size Bar Chart ─────────────────────────
ax = axes[1][2]
ax.set_title("Community Sizes", fontsize=12, fontweight="bold")
glabels = [f"Group {i+1}" for i in range(len(best))]
gsizes  = [len(c) for c in best]
gcolors = [COLORS[i] for i in range(len(best))]
bars = ax.bar(glabels, gsizes, color=gcolors, edgecolor="white",
              linewidth=1.5, width=0.5)
for bar, size, comm in zip(bars, gsizes, best):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1,
            str(size), ha="center", fontsize=11, fontweight="bold")
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()/2,
            "\n".join(comm), ha="center", va="center",
            fontsize=7, color="white", fontweight="bold")
ax.set_ylabel("Number of Students", fontsize=10)
ax.set_ylim(0, max(gsizes)+2)
ax.grid(axis="y", alpha=0.3, linestyle="--")
ax.spines[["top","right"]].set_visible(False)
ax.text(0.5,-0.12,
        f"Intra: {intra}  |  Inter: {inter}  |  Modularity: {modularity:.4f}",
        transform=ax.transAxes, ha="center", fontsize=8, color="gray")

plt.tight_layout()
plt.savefig("sna_assignment2_output.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n  ✔ All 6 plots saved as: sna_assignment2_output.png")
print("  ✔ Screenshot the terminal + plot window for your report!")
print("=" * 58)