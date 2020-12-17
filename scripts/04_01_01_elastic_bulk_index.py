# -*- coding: utf-8 -*-

"""
Summary:
    In this script we will read all the concpets that are coming from
    alexander street and create a newline separated json doc for each
    concpet that concpets all the chronicling america news that contains
    the phrase. It also creates a file that contains all the possible
    unique news that we gatherd from all these concpets into one single
    blob of file
Input:
    The filtered concept list
    ../input/raw/phrases_filtered_20201124_with_alternative.csv
Output
    It will create a json for each of the concept and put corresponding page titles
    in two files titled
    ../output/03_01_01_alex_street_concept_to_wiki_pagetitles_of_searched_text.json
    ../output/03_01_01_alex_street_concept_to_wiki_pagetitles_of_searched_page_title.json
"""
import json
import pandas as pd
import requests
import argparse
## imported from custom helper library accompanying this project
from helpers.Elasticsearch_Bulk_Indexing import ElasticBulk

# %%
output_code = "04_01_01"


# %%
parser = argparse.ArgumentParser(
        description="API to search Chronicling America",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('index_name', help='Name of the elastic search index')
parser.add_argument('-y', '--year', type=int, help='Max year')
args = parser.parse_args()

# %%
## Load the alexander streets concpets created by Laura
df_concepts = pd.read_csv("../input/derived/03_00_01_phrases_filtered_20201124_with_alternative.csv", keep_default_na=False)
