import json
import numpy as np
import matplotlib.pyplot as plt

# dataset = 'OLGA'
dataset = 'DISCO-OLGA'
# split = 'val'
split = 'test'
plot_by = 'layers'
# plot_by = 'feature'

gnn_layers = [0, 1, 2, 3, 4]

if dataset == 'OLGA':
  path = '../jobs/OLGA_eval/'
  job_ids = [(True, [[991490, 1000758, 1000766],
                    [991489, 1000757, 1000765],
                    [991488, 1000756, 1000764],
                    [991481, 1000754, 1000762],
                    [1002585, 1002630, 1002631]], 'random'),
            (True, [[991504, 1000781, 1001002],
                    [991500, 1000780, 1000903],
                    [991499, 1000779, 1000902],
                    [991498, 1000778, 1000901],
                    [1002634, 1002680, 1002694]], 'acousticbrainz'),
            (True, [[991520, 1001714, 1002061],
                    [991518, 1001402, 1002060],
                    [991516, 1001068, 1002059],
                    [991514, 1001067, 1002058],
                    [1002699, 1002700, 1002701]], 'clap'),
            (True, [[991529, 1002427, 1002580],
                    [991528, 1002424, 1002577],
                    [991525, 1002419, 1002575],
                    [991524, 1002413, 1002574],
                    [1002702, 1002703, 1002704]], 'acousticbrainz, clap' if plot_by == 'layers' else 'acousticbrainz\nclap')]
else:
  path = '../jobs/DISCO-OLGA_eval/'
  job_ids = [(True, [[993820, 997793, 997811],
                    [993819, 997787, 997810],
                    [993817, 997776, 997808],
                    [993816, 997760, 997807],
                    [1002739, 1002758, 1002768]], 'random'),
            (True, [[994030, 997991, 998438],
                    [994026, 997977, 998392],
                    [994024, 997973, 998351],
                    [994014, 997857, 998311],
                    [1002770, 1002777, 1002784]], 'acousticbrainz'),
            (True, [[994051, 998539, 1000660], 
                    [994050, 998538, 1000652],
                    [994048, 998537, 1000659],
                    [994046, 998536, 1000648],
                    [1002807, 1002809, 1002811]], 'clap'), 
            (True, [[994062, 1000664, 1000668],
                    [994057, 1000663, 1000667],
                    [994056, 1000662, 1000666],
                    [994052, 1000661, 1000665],
                    [1002813, 1002821, 1002827]], 'moods-themes'),
            (True, [[994079, 1000672, 1000677],
                    [994078, 1000671, 1000676],
                    [994073, 1000670, 1000675],
                    [994072, 1000669, 1000674],
                    [1002830, 1002837, 1002848]], 'acousticbrainz, clap' if plot_by == 'layers' else 'acousticbrainz\nclap'),
            (True, [[994132, 1000681, 1000706],
                    [994128, 1000680, 1000705],
                    [994127, 1000679, 1000704],
                    [994102, 1000678, 1000700],
                    [1002933, 1002938, 1002943]], 'acousticbrainz, moods-themes' if plot_by == 'layers' else 'acousticbrainz\nmoods-themes'),
            (True, [[994154, 1000722, 1000733],
                    [994149, 1000721, 1000730],
                    [994144, 1000720, 1000729],
                    [994143, 1000719, 1000728],
                    [1002951, 1002960, 1002971]], 'clap, moods-themes' if plot_by == 'layers' else 'clap\nmoods-themes'),
            (True, [[997437, 1000741, 1000749],
                    [997436, 1000739, 1000748],
                    [997435, 1000738, 1000747],
                    [997434, 1000736, 1000746],
                    [1002973, 1002977, 1002983]], 'acousticbrainz, clap, moods-themes' if plot_by == 'layers' else 'acousticbrainz\nclap\nmoods-themes')]


num_feature_combs = 0
for item in job_ids:
  if item[0]:
    num_feature_combs += 1

ndcgs = np.zeros((num_feature_combs, len(gnn_layers), 3))
for i in range(len(gnn_layers)):
  cur_feature_idx = 0
  for j in range(len(job_ids)):
    if not job_ids[j][0]:
      continue
    for k in range(3):
      with open(f"{path}{str(job_ids[j][1][gnn_layers[i]][k])}.out", "r") as f:
        eval_lines = []
        for ln in f:
          if ln.startswith(f"{split}:"):
            eval_lines.append(ln)
        json_rep = json.loads(eval_lines[-1][(len(split) + 1):].replace("'", '"'))
        ndcgs[cur_feature_idx][i][k] = json_rep['ndcg']
    cur_feature_idx += 1
scores = np.mean(ndcgs, -1).T if plot_by == 'layers' else np.mean(ndcgs, -1)
stds = np.std(ndcgs, -1).T if plot_by == 'layers' else np.std(ndcgs, -1)

feature_types = [] 
for item in job_ids:
  if item[0]:
    feature_types.append(item[2])

plt.figure(figsize=(12, 6))
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange']
if plot_by == 'layers':
  bar_width = 0.8 /len(feature_types) 
  r = [np.arange(len(gnn_layers))]
  for i in range(len(feature_types)- 1):
    r.append([x + bar_width for x in r[i]])

  for i in range(len(feature_types)):
    plt.bar(r[i], scores[:, i], yerr=stds[:, i], color=colors[i], width=bar_width, edgecolor='grey', label=feature_types[i])

  plt.xlabel('Number of Graph layers')
  plt.xticks([r + (len(feature_types) - 1.0) / 2.0 * bar_width for r in range(len(gnn_layers))], gnn_layers)
  plt.title(f'{dataset} Dataset')
else:
  bar_width = 0.8 /len(gnn_layers) 
  r = [np.arange(len(feature_types))]
  for i in range(len(gnn_layers)- 1):
    r.append([x + bar_width for x in r[i]])

  labels = [f'{str(layers)} Graph Layers' for layers in gnn_layers]
  for i in range(len(gnn_layers)):
    plt.bar(r[i], scores[:, i], yerr=stds[:, i], color=colors[i], width=bar_width, edgecolor='grey', label=labels[i])

  plt.xlabel('Feature Type')
  plt.xticks([r + (len(gnn_layers) - 1.0) / 2.0 * bar_width for r in range(len(feature_types))], feature_types)
  plt.title(f'{dataset} Dataset')

plt.ylabel('NDCG@200')
plt.gca().set_facecolor((0.92, 0.92, 0.92))
plt.gca().grid(axis='y', color='white', linewidth=2.0)
plt.gca().set_axisbelow(True)
plt.legend()
plt.tight_layout()

plt.ylim([0.0, 0.42])
# plt.show()

# save plot
plt.savefig(f'plot_{dataset}_by_{plot_by}_moods-themes.png')

