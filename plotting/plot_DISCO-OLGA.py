import json
import numpy as np
import matplotlib.pyplot as plt

# job_ids = [(True, [993820, 993819, 993817, 993816], 'random'),
#            (True, [994030, 994026, 994024, 994014], 'acousticbrainz'),
#            (True, [994051, 994050, 994048, 994046], 'clap'), 
#            (True, [994062, 994057, 994056, 994052], 'moods-themes'),
#            (True, [994079, 994078, 994073, 994072], 'acousticbrainz_clap'),
#            (True, [994132, 994128, 994127, 994102], 'acousticbrainz_moods-themes'),
#            (True, [994154, 994149, 994144, 994143], 'clap_moods-themes'),
#            (True, [997437, 997436, 997435, 997434], 'acousticbrainz_clap_moods-themes')]

job_ids = [(True, [[993820, 997793, 997811],
                   [993819, 997787, 997810],
                   [993817, 997776, 997808],
                   [993816, 997760, 997807]], 'random'),
           (True, [[994030, 997991, 998438],
                   [994026, 997977, 998392],
                   [994024, 997973, 998351],
                   [994014, 997857, 998311]], 'acousticbrainz'),
           (True, [[994051, 998539, 1000660], 
                   [994050, 998538, 1000652],
                   [994048, 998537, 1000659],
                   [994046, 998536, 1000648]], 'clap'), 
           (True, [[994062, 1000664, 1000668],
                   [994057, 1000663, 1000667],
                   [994056, 1000662, 1000666],
                   [994052, 1000661, 1000665]], 'moods-themes'),
           (True, [[994079, 1000672, 1000677],
                   [994078, 1000671, 1000676],
                   [994073, 1000670, 1000675],
                   [994072, 1000669, 1000674]], 'acousticbrainz_clap'),
           (True, [[994132, 1000681, 1000706],
                   [994128, 1000680, 1000705],
                   [994127, 1000679, 1000704],
                   [994102, 1000678, 1000700]], 'acousticbrainz_moods-themes'),
           (True, [[994154, 1000722, 1000733],
                   [994149, 1000721, 1000730],
                   [994144, 1000720, 1000729],
                   [994143, 1000719, 1000728]], 'clap_moods-themes'),
           (True, [[997437, 1000741, 1000749],
                   [997436, 1000739, 1000748],
                   [997435, 1000738, 1000747],
                   [997434, 1000736, 1000746]], 'acousticbrainz_clap_moods-themes')]

path = '../jobs/DISCO-OLGA_eval/'
split = 'val'

ndcgs = np.zeros((8, 4, 3))
for i in range(4):
  for j in range(8):
    if not job_ids[j][0]:
      continue
    for k in range(3):
      with open(f"{path}{str(job_ids[j][1][i][k])}.out", "r") as f:
        eval_lines = []
        for ln in f:
          if ln.startswith(f"{split}:"):
            eval_lines.append(ln)
        json_rep = json.loads(eval_lines[-1][(len(split) + 1):].replace("'", '"'))
        ndcgs[j][i][k] = json_rep['ndcg']
scores = np.mean(ndcgs, -1).T
stds = np.std(ndcgs, -1).T

gnn_layers = [0, 1, 2, 3]
feature_types = [] 
for item in job_ids:
  if item[0]:
    feature_types.append(item[2])

n_bars = len(feature_types)
bar_width = 0.8 / n_bars

r = [np.arange(len(gnn_layers))]
for i in range(n_bars - 1):
  r.append([x + bar_width for x in r[i]])

plt.figure(figsize=(12, 6))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange']
for i in range(n_bars):
  plt.bar(r[i], scores[:, i], yerr=stds[:, i], color=colors[i], width=bar_width, edgecolor='grey', label=feature_types[i])

plt.xlabel('Number of GNN layers', fontweight='bold')
plt.ylabel('NDCG@200', fontweight='bold')
plt.xticks([r + (n_bars - 1.0) / 2.0 * bar_width for r in range(len(gnn_layers))], gnn_layers)

plt.legend()
plt.show()
