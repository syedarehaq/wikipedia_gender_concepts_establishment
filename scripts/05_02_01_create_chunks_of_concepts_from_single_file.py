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
output_code = "05_02_01"

## If the column name is None then there is no 
## header. Otherwise we have a header name of the
## column we wish to use
concept_column_name = None

# %%
## Load the concpets created by Laura
base_fname = "brown_phrases" # phrases2_min2_202011217
if not concept_column_name:
    ## We do not have a header
    df_concepts = pd.read_csv(f"../input/raw/{base_fname}.csv", keep_default_na=False, header = None)
    concepts_to_search_for = df_concepts[0].values
else:
    df_concepts = pd.read_csv(f"../input/raw/{base_fname}.csv", keep_default_na=False)
    concepts_to_search_for = df_concepts[concept_column_name].values

## First we will count the number of concepts that belong to n-gram
concept_count_by_ngram_length = Counter([len(concept.split()) for concept in concepts_to_search_for])
min_concept_lenth = min(concept_count_by_ngram_length)
max_concept_length = max(concept_count_by_ngram_length)
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

for phrase_length in reversed(range(min_concept_lenth,max_concept_length+1)):
    current_lengthed_phrases = [phrase for phrase in concepts_to_search_for if len(phrase.strip().split())==phrase_length]
    for chunk_num,phrases_in_current_chunk in enumerate(chunks(current_lengthed_phrases,single_chunk_size)):
        df = pd.DataFrame(phrases_in_current_chunk,columns = ["concept"])
        df["concept_id"] = df["concept"].apply(lambda x: str(xxhash.xxh32(x,seed=xxhash_seed).intdigest()))
        df = df[["concept_id","concept"]]
        df.to_csv(f"../input/derived/chunked_files/{base_fname}/{base_fname}_conceptsize_{phrase_length}_chunknum_{chunk_num}.csv",index=False)