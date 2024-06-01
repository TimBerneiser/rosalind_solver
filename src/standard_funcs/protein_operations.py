"""
Author : Tim Berneiser
Date   : 2024-06-01
Purpose: Functions for handling proteins
"""

from typing import Dict, List, Tuple


# --------------------------------------------------
def get_protein_mass(sequence: str) -> float:
    """ Get protein mass """

    aa_masses = {'A': 71.03711, 'C': 103.00919, 'D': 115.02694, 'E': 129.04259,
                 'F': 147.06841, 'G': 57.02146, 'H': 137.05891, 'I': 113.08406,
                 'K': 128.09496, 'L': 113.08406, 'M': 131.04049, 'N': 114.04293,
                 'P': 97.05276, 'Q': 128.05858, 'R': 156.10111, 'S': 87.03203,
                 'T': 101.04768, 'V': 99.06841, 'W': 186.07931, 'Y': 163.06333}

    weight = 0

    for aa in sequence.upper():
        weight += aa_masses[aa]

    return weight


# --------------------------------------------------
def test_get_protein_mass() -> None:
    """ Test get_protein_mass """

    assert f'{get_protein_mass("SKADYEK"):.3f}' == '821.392'