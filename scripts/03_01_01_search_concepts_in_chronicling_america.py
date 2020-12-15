# -*- coding: utf-8 -*-

"""
Summary:
    In this script we will read all the concpets that are coming from
    alexander street and search in how many titles of wikipedia they appear
    and in how many article text they appear. This time we have made sure some
    of the concepts are hyphen separaated e.g. "anti-lynching" instead of
    "antilynching"
Input:
    The filtered concept list
    ../input/raw/phrases_filtered_20201124_with_alternative.csv
Output
    It will create a json for each of the concept and put corresponding page titles
    in two files titled
    ../output/02_03_01_alex_street_concept_to_wiki_pagetitles_of_searched_text.json
    ../output/02_03_01_alex_street_concept_to_wiki_pagetitles_of_searched_page_title.json
"""

import json
from collections import Counter, defaultdict
import csv
import pandas as pd
import requests
import pprint
from tqdm import tqdm
# %%
output_code = "03_01_01"

# %%
## Load the alexander streets concpets created by Laura
df_concepts = pd.read_csv("../input/raw/phrases_filtered_20201124_with_alternative.csv", keep_default_na=False)

alex_street_concepts_to_dash_separated_concept = df_concepts.set_index("concept_from_alex_street").to_dict()["alternative_phrase"]

#chron_am_search = requests.get("http://chroniclingamerica.loc.gov/search/pages/results/?proxtext=%s&proxdistance=2&format=json" %(search_phrase)).json()
all_docs_file = open("../output/%s_all_docs.json" %(output_code),"a", encoding="utf-8")
all_doc_ids = set()
## chronicling america concept search
search_phrases = ["dog","worlds student christian federation conference"]
for search_phrase in search_phrases:
    chron_am_search = requests.get("http://chroniclingamerica.loc.gov/search/pages/results/?proxtext=%s&format=json" %(search_phrase)).json()
    print("Current serach phrase %s, with %d results" %(search_phrase,chron_am_search["totalItems"]))
    current_phrase_doc_file = open("../output/%s_current_phrase_%s_docs.json" %(output_code, "_".join(search_phrase.strip().split())),"a", encoding="utf-8")
    for result in chron_am_search["items"]:
        if result["id"] not in all_doc_ids:
            print(result)
            all_doc_ids.add(result["id"])
            json.dump(result,all_docs_file, ensure_ascii=False)
            all_docs_file.write("\n")
        json.dump(result,current_phrase_doc_file, ensure_ascii=False)
        current_phrase_doc_file.write("\n")
    current_phrase_doc_file.close()
all_docs.close()