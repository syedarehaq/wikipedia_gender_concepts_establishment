# -*- coding: utf-8 -*-

"""
Summary:
    In this script we are creating some systematic chunks of concepts
    to parralelilze our search efforts
Input:
    The filtered concept list
    ../input/raw/phrases_filtered_20201124_with_alternative.csv
Output
    It will create a json for each of the concept and put corresponding page titles
    in two files titled
    ../output/03_01_01_alex_street_concept_to_wiki_pagetitles_of_searched_text.json
    ../output/03_01_01_alex_street_concept_to_wiki_pagetitles_of_searched_page_title.json
"""
import pandas as pd
from collections import Counter
import numpy as np
import xxhash

# %%
xxhash_seed = 42
output_code = "05_01_01"

base_fname_min3 = "phrases3_min3_20201217" # phrases2_min2_20201217
df_concepts_min3 = pd.read_csv("../input/raw/%s.csv" %base_fname_min3, keep_default_na=False)

min3_all_concepts = set(df_concepts_min3["concept_from_alex_street"].values)

## First we will count the number of concepts that belong to n-gram
Counter([len(concept.split()) for concept in min3_all_concepts])
max_concept_length_min3 = 5
## Counter({1: 7164, 3: 792, 2: 4605, 5: 17, 4: 110})

## So we will create a group of 1,2,3,4,5 grams in files of max size 100
## We will keep a counter that creates a priority of the file

## Copied from: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

## For the filename lets start with the concept length then the chunk number
single_chunk_size = 100

for phrase_length in reversed(range(1,max_concept_length_min3+1)):
    current_lengthed_phrases = [phrase for phrase in min3_all_concepts if len(phrase.strip().split())==phrase_length]
    for chunk_num,phrases_in_current_chunk in enumerate(chunks(current_lengthed_phrases,single_chunk_size)):
        df = pd.DataFrame(phrases_in_current_chunk,columns = ["concept_from_alex_street"])
        df["concept_id"] = df["concept_from_alex_street"].apply(lambda x: str(xxhash.xxh32(x,seed=xxhash_seed).intdigest()))
        df = df[["concept_id","concept_from_alex_street"]]
        df.to_csv("../input/derived/chunked_files/%s_conceptsize_%d_chunknum_%d.csv" %(base_fname_min3,phrase_length,chunk_num),index=False)


## Now we will put the extra concepts from min2_v2 in newer sperate chunks
base_fname_min2 = "phrases2_min2_20201217"
df_concepts_min2 = pd.read_csv("../input/raw/%s.csv" %base_fname_min2, keep_default_na=False)
min2_all_concepts = set(df_concepts_min2["concept_from_alex_street"].values)
Counter([len(concept.split()) for concept in min2_all_concepts])
## Counter({1: 12977, 2: 14958, 4: 503, 5: 94, 3: 2954})
## So we have max 5 length concepts again
max_concept_length_min2 = 5

extra_concpets_from_min2 = min2_all_concepts - min3_all_concepts
for phrase_length in reversed(range(1,max_concept_length_min2+1)):
    current_lengthed_phrases = [phrase for phrase in extra_concpets_from_min2 if len(phrase.strip().split())==phrase_length]
    for chunk_num,phrases_in_current_chunk in enumerate(chunks(current_lengthed_phrases,single_chunk_size)):
        df = pd.DataFrame(phrases_in_current_chunk,columns = ["concept_from_alex_street"])
        df["concept_id"] = df["concept_from_alex_street"].apply(lambda x: str(xxhash.xxh32(x,seed=xxhash_seed).intdigest()))
        df = df[["concept_id","concept_from_alex_street"]]
        df.to_csv("../input/derived/chunked_files/%s_conceptsize_%d_chunknum_%d.csv" %(base_fname_min2,phrase_length,chunk_num),index=False)
