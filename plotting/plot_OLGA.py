import json
import numpy as np
import matplotlib.pyplot as plt

random = [989395, 989399, 989393, 989392]
acousticbrainz = [989404, 989411, 989402, 989401]
clap = [989421, 989422, 989417, 989414]
acousticbrainz_clap = [989570, 989539, 989538, 989442]

path = '../jobs/OLGA_eval/'

random_ndcgs = []
acousticbrainz_ndcgs = []
clap_ndcgs = []
acousticbrainz_clap_ndcgs = []
for i in range(4):
  with open(f"{path}{str(random[i])}.out", "r") as f:
    val_lines = []
    for ln in f:
      if ln.startswith("val:"):
        val_lines.append(ln)
    json_rep = json.loads(val_lines[-1][4:].replace("'", '"'))
    random_ndcgs.append(json_rep['ndcg'])

  with open(f"{path}{str(acousticbrainz[i])}.out", "r") as f:
    val_lines = []
    for ln in f:
      if ln.startswith("val:"):
        val_lines.append(ln)
    json_rep = json.loads(val_lines[-1][4:].replace("'", '"'))
    acousticbrainz_ndcgs.append(json_rep['ndcg'])

  with open(f"{path}{str(clap[i])}.out", "r") as f:
    val_lines = []
    for ln in f:
      if ln.startswith("val:"):
        val_lines.append(ln)
    json_rep = json.loads(val_lines[-1][4:].replace("'", '"'))
    clap_ndcgs.append(json_rep['ndcg'])

  with open(f"{path}{str(acousticbrainz_clap[i])}.out", "r") as f:
    val_lines = []
    for ln in f:
      if ln.startswith("val:"):
        val_lines.append(ln)
    json_rep = json.loads(val_lines[-1][4:].replace("'", '"'))
    acousticbrainz_clap_ndcgs.append(json_rep['ndcg'])

scores = np.array([random_ndcgs, acousticbrainz_ndcgs, clap_ndcgs, acousticbrainz_clap_ndcgs]).T

gnn_layers = [0, 1, 2, 3]
feature_types = ['random', 'acousticbrainz', 'clap', 'acousticbrainz_clap']

n_bars = len(feature_types)

# Set the width of each bar
bar_width = 0.2

# Positions of the bars on the x-axis
r1 = np.arange(len(gnn_layers))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [x + bar_width for x in r3]

# Create the bar plots
plt.figure(figsize=(10, 6))

plt.bar(r1, scores[:, 0], color='b', width=bar_width, edgecolor='grey', label=feature_types[0])
plt.bar(r2, scores[:, 1], color='g', width=bar_width, edgecolor='grey', label=feature_types[1])
plt.bar(r3, scores[:, 2], color='r', width=bar_width, edgecolor='grey', label=feature_types[2])
plt.bar(r4, scores[:, 3], color='c', width=bar_width, edgecolor='grey', label=feature_types[3])

# Add xticks on the middle of the group bars
plt.xlabel('Number of GNN layers', fontweight='bold')
plt.ylabel('Score', fontweight='bold')
plt.xticks([r + bar_width for r in range(len(gnn_layers))], gnn_layers)

# Add legend
plt.legend()

# Show the plot
plt.show()
