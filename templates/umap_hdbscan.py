#!/usr/bin/env python

import numpy as np
import umap
import matplotlib.pyplot as plt
from sklearn import decomposition
import random
import pandas as pd
import hdbscan

df = pd.read_csv("$kmer_freqs", delimiter="\t")

#UMAP
motifs = [x for x in df.columns.values if x not in ["read", "length"]]
X = df.loc[:,motifs]
X_embedded = umap.UMAP(n_neighbors=15, min_dist=0.1, verbose=2).fit_transform(X)

df_umap = pd.DataFrame(X_embedded, columns=["D1", "D2"])
umap_out = pd.concat([df["read"], df["length"], df_umap], axis=1)

#HDBSCAN
X = umap_out.loc[:,["D1", "D2"]]
umap_out["bin_id"] = hdbscan.HDBSCAN(min_cluster_size=int($params.min_cluster_size), cluster_selection_epsilon=int($params.cluster_sel_epsilon)).fit_predict(X)

#PLOT
plt.figure(figsize=(20,20))
plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=umap_out["bin_id"], cmap='Spectral', s=1)
plt.xlabel("UMAP1", fontsize=18)
plt.ylabel("UMAP2", fontsize=18)
plt.gca().set_aspect('equal', 'datalim')
plt.title("Projecting " + str(len(umap_out['bin_id'])) + " reads. " + str(len(umap_out['bin_id'].unique())) + " clusters generated by HDBSCAN", fontsize=18)

for cluster in np.sort(umap_out['bin_id'].unique()):
    read = umap_out.loc[umap_out['bin_id'] == cluster].iloc[0]
    plt.annotate(str(cluster), (read['D1'], read['D2']), weight='bold', size=14)

plt.savefig('hdbscan.output.png')
umap_out.to_csv("hdbscan.output.tsv", sep="\t", index=False)
