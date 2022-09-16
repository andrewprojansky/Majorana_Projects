# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 10:44:42 2022
Edited/Expanded on Fri Sep 16 2:36 2022
original @author: jogib
editing/expanding @author: andrewprojansky
"""

import networkx as nx
import itertools
import numpy as np
import matplotlib.pyplot as plt
import math

#%%
pauli = {
    "I": np.array(np.mat("1,0;0,1")),
    "Z": np.array(np.mat("1,0;0,-1")),
    "X": np.array(np.mat("0,1;1,0")),
    "Y": np.array(1j * np.mat("0,-1;1,0")),
}
#%%
# init all the tensors
n=2
lis = ["X", "Y", "Z", "I"]
combos = itertools.product(lis, repeat=n)
names = ["".join(x for x in i) for i in combos]
#%%


def anticommute_check(A, B):
    ch_arr = []
    for i in range(len(A)):
        a_t = pauli[A[i]]
        b_t = pauli[B[i]]
        check = np.dot(a_t, b_t) + np.dot(b_t, a_t)
        ch_arr.append(not np.any(check))
    return np.count_nonzero(ch_arr) % 2


def gen_graph(n=2):
    lis = ["X", "Y", "Z", "I"]
    combos = itertools.product(lis, repeat=n)
    d = {i: "".join(j for j in x) for i, x in enumerate(combos)}
    G = nx.empty_graph(len(d.values()))
    G = nx.relabel_nodes(G, d)
    # add edges
    for i in itertools.combinations(list(d.values()), 2):

        A = i[0]
        B = i[1]
        if anticommute_check(A, B):
            G.add_edge(i[0], i[1], **{"color": "tab:blue", "width": 0.05})
    return G


#%%
G = gen_graph(n)
G.remove_node("".join("I" for i in range(n)))

#%%
pos = nx.spring_layout(G)
fig, ax = plt.subplots(figsize=(16, 16))
node_opts = {"node_size": 500, "node_color": "w", "edgecolors": "k", "linewidths": 2.0}
nx.draw_networkx_nodes(G, pos, **node_opts)
nx.draw_networkx_labels(G, pos, font_size=10)
nx.draw_networkx_edges(G, pos, width=0.2)

def comm_check(clique, paulis):
    
    print("clique:")
    print(clique)
    l = []
    for p in names:
        i = 0
        for c in clique: 
            if anticommute_check(p,c) == 0:
                i+=1
        if i == len(clique):
            l.append(p)
    print("items which commute with all")
    print(l)
    
    l = l[0:len(l)]
    print('anti-commuting sets that commute with clique')
    for k in range(3, len(l)+1):
        subsets = findsubsets(l,k)
        for sset in subsets:
            q = 0
            subsubsets = findsubsets(sset, 2)
            for sssets in subsubsets:
                q = q + anticommute_check(sssets[0], sssets[1])
            if q == math.factorial(len(sset))/(math.factorial(len(sset)-2)*2):
                print(sset)
            
    print("")
    
def findsubsets(s, n):
    return list(map(list, itertools.combinations(s, n)))

for i in nx.find_cliques(G):
    if len(i) == (2*n+1):
        for j in range(2, 2*n+2):
            subsets = findsubsets(i, j)
            for sets in subsets:
                comm_check(sets, names)
