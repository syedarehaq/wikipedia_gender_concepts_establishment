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
## imported from custom helper library accompanying this project
from helpers.chroniclingamerica import ChronAm
# %%
output_code = "03_01_01"

# %%
## Load the alexander streets concpets created by Laura
df_concepts = pd.read_csv("../input/derived/03_00_01_phrases_filtered_20201124_with_alternative.csv", keep_default_na=False)

alex_street_concept_name_to_concept_id = df_concepts.set_index("concept_from_alex_street").to_dict()["concept_id"]
alex_street_concept_name_to_dash_separated_concept_name = df_concepts.set_index("concept_from_alex_street").to_dict()["alternative_phrase"]

#chron_am_search = requests.get("http://chroniclingamerica.loc.gov/search/pages/results/?proxtext=%s&proxdistance=2&format=json" %(search_phrase)).json()
all_chronam_docs_file = open("../output/untracked/%s_all_docs.json" %(output_code),"a", encoding="utf-8")
all_chronam_doc_ids = set()
## chronicling america concept search
## Testing dog concept

##
counter = 0
for search_phrase,dash_seprated_search_phrase in alex_street_concept_name_to_dash_separated_concept_name.items():
    counter +=1
    if counter % 100 == 0:
        print("%d left out of %d concepts" %(counter,len(alex_street_concept_name_to_concept_id)))
    print(search_phrase)
    current_phrase_doc_ids_all = set()
    ## First we will work with the regular non-dash separated concept
    fetcher = ChronAm(search_phrase,language="eng",proxdistance=2)
    current_phrase_doc_file = open("../output/untracked/%s_current_phrase_%s_docs.json" %(output_code, alex_street_concept_name_to_concept_id[search_phrase]),"a", encoding="utf-8")
    for result in fetcher.fetch():
        if result["id"] not in all_chronam_doc_ids:
            all_chronam_doc_ids.add(result["id"])
            json.dump(result,all_chronam_docs_file, ensure_ascii=False)
            all_chronam_docs_file.write("\n")
        if result["id"] not in current_phrase_doc_ids_all:
            current_phrase_doc_ids_all.add(result["id"])
            json.dump(result,current_phrase_doc_file, ensure_ascii=False)
            current_phrase_doc_file.write("\n")
    ## Then we will work with the alternate search phrase that is dash separated
    ## This time we will only append current doc if the id is not already in the current doc
    if dash_seprated_search_phrase:
    ## If we have a non empty search phrase, if it is empty e.g. ""
    ## It will return with all the chronam docs with 870726*20 pages
        fetcher = ChronAm(dash_seprated_search_phrase,language="eng",proxdistance=2)
        for result in fetcher.fetch():
            if result["id"] not in all_chronam_doc_ids:
                all_chronam_doc_ids.add(result["id"])
                json.dump(result,all_chronam_docs_file, ensure_ascii=False)
                all_chronam_docs_file.write("\n")
            if result["id"] not in current_phrase_doc_ids_all:
                current_phrase_doc_ids_all.add(result["id"])
                json.dump(result,current_phrase_doc_file, ensure_ascii=False)
                current_phrase_doc_file.write("\n")
        current_phrase_doc_file.close()
all_chronam_docs_file.close()