"""
Author : Tim Berneiser
Date   : 2024-05-27
Purpose: Functions for manipulating DNA sequences
"""

from typing import Dict, List, Tuple
import re
import sys
from itertools import zip_longest
import pandas as pd


# --------------------------------------------------
def is_DNA(sequence: str) -> bool:
    """ Checks if string is DNA """

    for base in sequence.upper():
        if base not in ['A', 'T', 'C', 'G']:
            return False

    return True


# --------------------------------------------------
def is_RNA(sequence: str) -> bool:
    """ Checks if string is RNA """

    for base in sequence.upper():
        if base not in ['A', 'U', 'C', 'G']:
            return False

    return True


# --------------------------------------------------
def is_NA(sequence: str) -> bool:
    """" Checks if string is DNA or RNA"""

    for base in sequence.upper():
        if base not in ['A', 'T', 'U', 'C', 'G']:
            return False

    return True

# --------------------------------------------------
def count_bases(sequence: str) -> Dict[str, int]:
    """ Count bases in string """

    counter = {}

    for base in sequence:
        if base.upper() in counter.keys():
            counter[base.upper()]+=1
        else:
            counter[base.upper()]=1

    return counter


# --------------------------------------------------
def transcribe(seq: str) -> str:
    """ Transcribe DNA to RNA """

    return re.sub('t', 'u', re.sub('T', 'U', seq))


# --------------------------------------------------
def get_revc(seq: str) -> str:
    """ Reverse complement to a sequence """

    revc = ''
    trans = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G',
             'a': 't', 't': 'a', 'g': 'c', 'c': 'g'}

    for base in seq[::-1]:
        if base not in trans.keys():
            sys.exit(f'Found "{base}" in sequence. Please enter a valid DNA sequence.')
        else:
            revc+=trans[base]

    return revc


# --------------------------------------------------
def get_gc(sequence: str) -> float:
    """ Get GC content of a sequence """

    gc_count = sequence.upper().count('G') + sequence.upper().count('C')

    if gc_count == 0:
        return 0

    return 100*gc_count/len(sequence)


# --------------------------------------------------
def get_hamming(seq1: str, seq2: str) -> int:
    """ Compute Hamming distance """

    return sum((1 for c1, c2 in zip_longest(seq1, seq2) if c1 != c2))


# --------------------------------------------------
def translate(sequence: str, stop=False, shift=0) -> str:
    """ Translates an RNA or DNA sequence """

    sequence = sequence.upper()

    if sequence.find('T'):
        sequence = re.sub('t', 'u', re.sub('T', 'U', sequence))

    codon_table = {
        "UUU" : "F", "CUU" : "L", "AUU" : "I", "GUU" : "V",
        "UUC" : "F", "CUC" : "L", "AUC" : "I", "GUC" : "V",
        "UUA" : "L", "CUA" : "L", "AUA" : "I", "GUA" : "V",
        "UUG" : "L", "CUG" : "L", "AUG" : "M", "GUG" : "V",
        "UCU" : "S", "CCU" : "P", "ACU" : "T", "GCU" : "A",
        "UCC" : "S", "CCC" : "P", "ACC" : "T", "GCC" : "A",
        "UCA" : "S", "CCA" : "P", "ACA" : "T", "GCA" : "A",
        "UCG" : "S", "CCG" : "P", "ACG" : "T", "GCG" : "A",
        "UAU" : "Y", "CAU" : "H", "AAU" : "N", "GAU" : "D",
        "UAC" : "Y", "CAC" : "H", "AAC" : "N", "GAC" : "D",
        "UAA" : "*", "CAA" : "Q", "AAA" : "K", "GAA" : "E",
        "UAG" : "*", "CAG" : "Q", "AAG" : "K", "GAG" : "E",
        "UGU" : "C", "CGU" : "R", "AGU" : "S", "GGU" : "G",
        "UGC" : "C", "CGC" : "R", "AGC" : "S", "GGC" : "G",
        "UGA" : "*", "CGA" : "R", "AGA" : "R", "GGA" : "G",
        "UGG" : "W", "CGG" : "R", "AGG" : "R", "GGG" : "G"
    }

    codons = [sequence[i:i+3] for i in range(shift, len(sequence), 3) if len(sequence[i:i+3])==3]

    aas = [codon_table.get(codon) for codon in codons]

    if '*' in aas and stop:
        return ''.join(aas[:aas.index('*')])

    return ''.join(aas)


# --------------------------------------------------
def get_kmers(sequence: str, k: int) -> List[str]:
    """ Get all k-mers in sequence """

    return [sequence[i:i+k] for i in range(len(sequence)-k+1)]


# --------------------------------------------------
def find_motifs(sequence, motif):
    """ Find all positions where motif occurs """

    if motif == '':
        return []
    return [index for index, kmer in enumerate(get_kmers(sequence, len(motif))) if kmer==motif]


# --------------------------------------------------
def get_consensus(seqs: List[str]) -> str:
    """ Get the consensus sequence """

    seqs_list = []

    if not seqs or not seqs[0]:
        return ''

    for seq in seqs:
        bases = [base for index, base in enumerate(seq.upper())]
        seqs_list.append(bases)

    seqs_df = pd.DataFrame(seqs_list)

    profile_matrix = seqs_df.apply(lambda x: x.value_counts()).fillna(0).astype(int)

    profile_matrix = profile_matrix.apply(lambda x: x.idxmax())

    return ''.join(profile_matrix.to_string(header=False, index=False).split('\n'))


# --------------------------------------------------
def get_graphs(sequences: Dict[str, str], overlap: int) -> List[Tuple[str, str]]:
    """ Make graphs """

    graphs = list(tuple())

    seqs = [(id, sequences[id][0:overlap], sequences[id][-overlap:])
            for id in sequences]

    for i in range(len(seqs)):
        for j in range(len(seqs)):
            if i!= j and seqs[i][2] == seqs[j][1]:
                graphs.append((seqs[i][0], seqs[j][0]))

    return graphs


# --------------------------------------------------
def test_is_xNA() -> None:
    """ Test is_DNA, is_RNA, is_NA """

    assert is_DNA('ASDKJB') == False
    assert is_DNA('') == True
    assert is_DNA('CGACGGACTTAGU') == False
    assert is_DNA('CGACGAATACCCG') == True

    assert is_RNA('ASDKJB') == False
    assert is_RNA('') == True
    assert is_RNA('CGACGGACUUAGU') == True
    assert is_RNA('CGACGAATACCCG') == False
    
    assert is_NA('ASDKJB') == False
    assert is_NA('') == True
    assert is_NA('CGACGGACUUAGU') == True
    assert is_NA('CGACGAATACCCG') == True


# --------------------------------------------------
def test_count_bases() -> None:
    """ Test count_bases """

    assert not count_bases('')
    assert count_bases('AAA') == {'A': 3}
    assert count_bases('BbB') == {'B': 3}
    assert count_bases('ABC') == {'A': 1, 'B': 1, 'C': 1}
    assert count_bases('ABCaBC') == {'A': 2, 'B': 2, 'C': 2}
    assert count_bases('ABCDEFG') == {'A':1, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1}
    assert count_bases('AABbbCAA') == {'A': 4, 'B': 3, 'C': 1}


# --------------------------------------------------
def test_transcribe() -> None:
    """ Test transcribe """

    assert transcribe('') == ''
    assert transcribe('12hd!§483') == '12hd!§483'
    assert transcribe('ABCDEFG') == 'ABCDEFG'
    assert transcribe('ATTCATA') == 'AUUCAUA'
    assert transcribe('AaTtCcTtU') == 'AaUuCcUuU'
    assert transcribe('TTTtTT') == 'UUUuUU'
    assert transcribe('UT') == 'UU'


# --------------------------------------------------
def test_get_revc() -> None:
    """ Test reverse_seq """

    assert get_revc('') == ''
    assert get_revc('ACTG') == 'CAGT'
    assert get_revc('AAAA') == 'TTTT'
    assert get_revc('atTgC') == 'GcAat'
    assert get_revc('AttA') == 'TaaT'
    assert get_revc('aTTa') == 'tAAt'


# --------------------------------------------------
def test_get_gc() -> None:
    """ Test get_gc """

    assert get_gc('GGCC') == 100
    assert get_gc('GCTA') == 50
    assert get_gc('') == 0
    assert get_gc('AATT') == 0
    assert get_gc('actg') == 50
    assert get_gc('AaTtcGgTATTa') == 25


# --------------------------------------------------
def test_get_hamming() -> None:
    """ Test get_hamm """

    assert get_hamming('', '') == 0
    assert get_hamming('A-A', 'ATA') == 1
    assert get_hamming('AACC', 'AA') == 2
    assert get_hamming('ACGCAACG', 'CGAGCCGA') == 8
    assert get_hamming('AACCGGCCAA', 'ACCGGCCAAT') == 5


# --------------------------------------------------
def test_translate() -> None:
    """ Tests translate """

    assert(translate('AAC')) == 'N'
    assert(translate('ACCUGACGG')) == 'T*R'
    assert(translate('ACCUGACGG', stop=True)) == 'T'
    assert(translate('ACCUGACGGGC')) == 'T*R'
    assert(translate('AACCUGACGGGC', shift=1)) == 'T*R'


# --------------------------------------------------
def test_get_kmers() -> None:
    """ Test get_kmers """

    assert get_kmers('ABCDEFG', 3) == ['ABC', 'BCD', 'CDE', 'DEF', 'EFG']
    assert get_kmers('ABCDEFG', 2) == ['AB', 'BC', 'CD', 'DE', 'EF', 'FG']
    assert get_kmers('', 3) == []


# --------------------------------------------------
def test_get_consensus() -> None:
    """ Test get_consensus """

    assert get_consensus(['ABC', 'ABC', 'ABC', 'ABB']) == 'ABC'
    assert get_consensus([]) == ''
    assert get_consensus(['', '']) == ''
    assert get_consensus(['ABC', 'BCD', 'ACD', 'abc', 'abc']) == 'ABC'


# --------------------------------------------------
def test_find_motifs() -> None:
    """ Test find_motifs """

    assert find_motifs('ABCDEFGABC', '') == []
    assert find_motifs('ABCDEFGABC', 'ABC') == [0, 7]
    assert find_motifs('ABCDEFGABC', 'ZZ') == []
    assert find_motifs('', 'ABCDEFG') == []
