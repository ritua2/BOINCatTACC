"""
BASICS

List of all tags, some of which contain subtags.
"""

tags = {
    "ASTRONOMY":[],
    "BIOLOGY":["GENETICS"],
    "CHEMISTRY":[],
    "COMPUTER_SCIENCE":["ARTIFICIAL_INTELLIGENCE"],
    "ENGINEERING":["STRUCTURES"],
    "GPU":[],
    "MATERIALS SCIENCE":[],
    "MATHEMATICS":[],
    "MEDICINE":[],
    "MISCELLANEOUS":[],
    "PHYSICS":["QUANTUM", "THERMODYNAMICS"]
}

# TACC Images have a predetermined tag
TACCIM = {
    "carlosred/autodock-vina:latest": {"BIOLOGY": []}, 
    "carlosred/bedtools:latest": {"BIOLOGY": ["GENETICS"]},
    "carlosred/blast:latest": {"BIOLOGY": ["GENETICS"]}, 
    "carlosred/bowtie:built": {"BIOLOGY": ["GENETICS"]},
    "carlosred/gromacs:latest": {"CHEMISTRY": []}, 
    "carlosred/htseq:latest": {"COMPUTER SCIENCE": []},
    "carlosred/mpi-lammps:latest": {"CHEMISTRY": []}, 
    "carlosred/namd-cpu:latest": {"CHEMISTRY": []},
    "saumyashah/opensees:latest": {"ENGINEERING": ["STRUCTURES"]}, 
    "carlosred/gpu:cuda": {"GPU": []}
 }
 