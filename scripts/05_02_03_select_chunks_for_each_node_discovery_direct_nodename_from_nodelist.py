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
discovery_nodenames = ['c3119',
 'c3178',
 'c3179',
 'c3180',
 'c3181',
 'c3182',
 'c3183',
 'c3184',
 'c3185',
 'c3186',
 'c3187',
 'c3188',
 'c3190',
 'c3191',
 'c3192',
 'c3193',
 'c3194',
 'c3195',
 'c3196',
 'c3197',
 'c3198',
 'c3199',
 'c3200',
 'c3201',
 'c3202',
 'c3203',
 'c3204',
 'c3205',
 'c3206',
 'c3207',
 'c3208',
 'c3209',
 'c3210',
 'c3211',
 'c3212',
 'c3213',
 'c3214',
 'c3215',
 'c3216',
 'c3217',
 'c3218',
 'c3219',
 'c3220',
 'c3221',
 'c3222',
 'c3223',
 'c3224']

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