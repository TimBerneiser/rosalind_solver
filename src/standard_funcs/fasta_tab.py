"""
Author : Tim Berneiser
Date   : 2024-06-01
Purpose: Functions for the fasta tab
"""

from typing import List, Dict
import pandas as pd


# --------------------------------------------------
def find_consensus(seqs_list: List[str]) -> str:
    """ Find the consensus sequecnce """

    seqs_df = pd.DataFrame(seqs_list)

    profile_matrix = seqs_df.apply(lambda x: x.value_counts()).fillna(0).astype(int)

    consensus = profile_matrix.apply(lambda x: x.idxmax()).to_string(header=False, index=False).split('\n')

    return ''.join(consensus)