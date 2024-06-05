"""
Author : Tim Berneiser
Date   : 2024-05-27
Purpose: Functions for handling fastx files
"""

from typing import Dict, List
import os
import statistics
from tabulate import tabulate
from Bio import SeqIO


# --------------------------------------------------
def guess_format(filename: str) -> str:
    """ Guess the file format from extension """

    fasta_ext = ['fasta', 'fa', 'fna', 'faa']
    fastq_ext = ['fq', 'fastq']
    handle = filename.split('.')[-1]

    if handle in fasta_ext:
        return 'fasta'

    if handle in fastq_ext:
        return 'fastq'

    return ''


# --------------------------------------------------
def extract_seqs(files: List[str]) -> Dict[str, str]:
    """ Extract sequences from list of fastx files """

    sequences = {}
    for fh in files:
        if seqs:= [rec for rec in SeqIO.parse(fh, guess_format(fh))]:
            sequences.update({seq.id: str(seq.seq) for seq in seqs})

    return sequences


# --------------------------------------------------
def write_to_fasta(seq_list: Dict[str, str], fname: str, out_dir: str = 'temp') -> None:
    """ Write sequences to fasta files """

    if not os.path.exists(f'./{out_dir}'):
        os.makedirs(f'./{out_dir}')

    with open(f'./{out_dir}/{fname}.fasta', 'wt') as new_fasta:
        for id in seq_list:
            new_fasta.write(f'>{id}\n{seq_list[id]}\n')


# --------------------------------------------------
def list_seqinfo(files: List[str], tablefmt='simple'):

    seqs_info = []

    for fh in files:
        name = os.path.basename(fh)
        if seqs:= [rec for rec in SeqIO.parse(fh, guess_format(fh))]:
            min_len = min([len(str(seq.seq)) for seq in seqs])
            max_len = max([len(str(seq.seq)) for seq in seqs])
            avg_len = statistics.fmean([len(str(seq.seq)) for seq in seqs])
            num_seqs = len(seqs)
            seqs_info.append((name, num_seqs, avg_len, min_len, max_len))
        else:
            seqs_info.append((name, 0, 0, 0.00, 0))

    headers = ['name', 'num_seqs', 'avg_len', 'min_len', 'max_len']
    
    return tabulate(seqs_info, headers=headers, tablefmt=tablefmt, floatfmt='.2f')
