"""
Author : Tim Berneiser
Date   : 2024-05-27
Purpose: Functions for handling fastx files
"""
from typing import Dict, List, TextIO
from Bio import SeqIO
import os


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
def extract_seqs(files: List[TextIO], extension: str) -> Dict[str, str]:
    """ Extract sequences from list of fasta files """

    for fh in files:
        if seqs:= [rec for rec in SeqIO.parse(fh, extension)]:
            sequences = {seq.id: str(seq.seq) for seq in seqs}

    return sequences


# --------------------------------------------------
def write_to_fasta(seq_list: Dict[str, str], fname: str, out_dir: str = 'temp') -> None:
    """ Write sequences to fasta files """

    if not os.path.exists(f'./{out_dir}'):
        os.makedirs(f'./{out_dir}')

    with open(f'./{out_dir}/{fname}.fasta', 'wt') as new_fasta:
        for id in seq_list:
            new_fasta.write(f'>{id}\n{seq_list[id]}\n')
