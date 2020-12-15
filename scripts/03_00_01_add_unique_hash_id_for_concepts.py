# -*- coding: utf-8 -*-

"""
Summary:
    Add hash id for each of the concepts
Input:
    The filtered concept list
    ../input/raw/phrases_filtered_20201124_with_alternative.csv
Output
    A file created with unique hash id from the concpet name
    ../input/derived/03_00_01_phrases_filtered_20201124_with_alternative.csv
"""
import pandas as pd
import xxhash
## imported from custom helper library accompanying this project
from helpers.chroniclingamerica import ChronAm
# %%
output_code = "03_00_01"

# %%
## Load the alexander streets concpets created by Laura
fname="phrases_filtered_20201124_with_alternative"
df_concepts = pd.read_csv("../input/raw/%s.csv" %fname, keep_default_na=False)
df_concepts["concept_id"] = df_concepts["concept_from_alex_street"].apply(lambda x: str(xxhash.xxh32(x,seed=42).intdigest()))
df_concepts = df_concepts[["concept_id",
    "concept_from_alex_street",
    "alternative_phrase",
    "phrase_code"]]
df_concepts.to_csv("../input/derived/%s_%s.csv" %(output_code,fname),index=False)