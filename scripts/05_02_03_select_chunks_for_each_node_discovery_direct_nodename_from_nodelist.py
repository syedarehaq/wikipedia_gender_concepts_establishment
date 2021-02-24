# -*- coding: utf-8 -*-

"""
Summary:
    In this script I am creating 47 chunks of files assigned
    to each one of the single nodes I will be using in discvery
    to run the search process in wikipedia
Input:
    None
Output
    It will create a text file for each of the 47 nodes,
    newline separated, containing the input file they 
    will work on
"""
from collections import defaultdict
import glob
from os.path import basename
import os
import argparse

# %%
# %%
parser = argparse.ArgumentParser(
        description="Script to crete list files containing concepts, for each discovery node that it will process",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-C','--corpus', help="just the name of the target corpus file that laura created, example: 'brown_phrases_oneword'" )
args = parser.parse_args()

# %%
output_code = "05_02_03"

base_fname = args.corpus
chunks_directory = f"../input/derived/chunked_files/{base_fname}/*"
filenames = glob.glob(chunks_directory)

chunks = sorted([basename(x) for x in filenames])
## I will be working on 47 specific disvoery nodes
#discovery_nodenames = ["c3%d"%x for x in range(178,224+1)]
discovery_nodenames = []
with open("./discovery_cluster/available_nodelist.txt","r") as f:
    for line in f:
        discovery_nodenames.append(line.strip())
nodenum_to_filelist = defaultdict(list)
counter = 0
total_discovery_nodes = 47

while chunks:
    nodenum_to_filelist[counter%total_discovery_nodes].append(chunks.pop().split(".")[0])
    counter += 1
output_basedir = f"../input/derived/discovery_input_for_each_node/{base_fname}"
os.mkdir(output_basedir)
for current_node, fnames in nodenum_to_filelist.items():
    with open(f"{output_basedir}/{discovery_nodenames[current_node]}.txt","w") as f:
        for fname in fnames:
            f.write(fname+"\n")