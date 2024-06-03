"""
Author : Tim Berneiser
Date   : 2024-06-03
Purpose: Creating overlap graph with Graphviz
"""

from typing import Tuple, List, Dict
from Bio import SeqIO
from graphviz import Digraph


# --------------------------------------------------
def list_overlaps(sequences: Dict[str, str], overlap) -> List[Tuple[str, str]]:
    """ List overlapping sequences """

    seqs = [(id, sequences[id][0:overlap], sequences[id][-overlap:])
            for id in sequences]

    graphs = list(tuple())

    for i in range(len(seqs)):
        for j in range(len(seqs)):
            if i!= j and seqs[i][2] == seqs[j][1]:
                graphs.append((seqs[i][0], seqs[j][0]))

    return graphs


# --------------------------------------------------
def visualize_graphs(graphs: List[Tuple[str, str]]):
    """ Visualize graph structure from overlaps """

    graphed = Digraph()

    for seq1, seq2 in graphs:
        graphed.node(seq1)
        graphed.node(seq2)
        graphed.edge(seq1, seq2)

    return graphed
