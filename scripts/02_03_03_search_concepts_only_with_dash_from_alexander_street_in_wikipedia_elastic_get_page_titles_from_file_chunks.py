# -*- coding: utf-8 -*-

"""
Summary:
    In this script we will read all the concpets that are coming from
    alexander street and search in how many titles of wikipedia they appear
    and in how many article text they appear. This time we have made sure some
    of the concepts are hyphen separaated e.g. "anti-lynching" instead of
    "antilynching". We are getting only the dash separated concepts rather than
    02_03_01, where we have botht the non dash sperated and dash separated concepts
Input:
    The filtered concept list
    ../input/raw/phrases3_min3_202011217.csv or
    ../input/raw/phrases2_min2_202011217
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
import argparse
## imported from custom helper library accompanying this project
from helpers.elastic_scroll import ElasticScroll

import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# %%
parser = argparse.ArgumentParser(
        description="Script to bulk insert a newline separated json file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i','--input', help='name of the chunked file that contains the phrases that it will be looking for')
parser.add_argument('-c','--corpus', help='name of the corpus that the phrases are coming from')
args = parser.parse_args()
# %%
file_basenames = [args.input]
corpus_name = args.corpus
# %%
output_code = "02_03_03"

# %%
## Load the alexander streets concpets created by Laura
# base_fname = "phrases3_min3_20201217" # phrases2_min2_20201217
# phrase_lengths_this_turns = [3,4,5]
# max_chunk_nums = {
#     "phrases3_min3_20201217":{
#         1:71,
#         2:46,
#         3:7,
#         4:1,
#         5:0,
#     },
#     "phrases2_min2_20201217":{
#         1:58,
#         2:103,
#         3:21,
#         4:3,
#         5:0,
#     }
# }

# for phrase_length in phrase_lengths_this_turns:
#     for chunk_num in range(max_chunk_nums[base_fname][phrase_length]+1):
#         file_basenames.append("%s_conceptsize_%d_chunknum_%d" %(base_fname,phrase_length,chunk_num))

for chunked_file_basename in file_basenames:
    #print(chunked_file_basename)
    df_concepts = pd.read_csv(f"/work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/input/derived/chunked_files/{corpus_name}/{chunked_file_basename}.csv", keep_default_na=False)

    alex_street_dash_separated_concepts = df_concepts["concept"].values

    # ### For testing
    # alex_street_concepts_to_dash_separated_concept = {
    #     "czechoslovak immigrants": "czecho-slovak immigrants",
    #     "dyer antilynching bill": "dyer anti-lynching bill"
    # }
    # ### Test Output inside text search only (with alternate dash separation):
    # {"concept": "czechoslovak immigrants", "wikipedia_page_titles_appeared_in": ["List of people from Yonkers, New York", "Joseph Plavcan", "Maryland", "Belinda Bencic", "Disputanta, Virginia", "Patrick Mohr", "Yonkers, New York", "CSPS", "Western Fraternal Life Association", "Jon Ledecky", "Kerem Maharal", "Friedrich Hecker", "Stephen Furdek", "Andrei Cherny", "Timeline of Baltimore in the 19th century", "Dancer in the Dark", "History of Saint Paul, Minnesota", "Ester, Alaska", "Brookside, Alabama", "Robert Maxwell", "Wild Mary Sudik", "Jim Puplava", "Fenar Ahmad", "Pinky and Perky", "Joe Manchin", "Joan McGuire Mohr", "Leonard Paulu"]}
    # {"concept": "dyer antilynching bill", "wikipedia_page_titles_appeared_in": ["Mary Landrieu", "Florence Kelley", "Lynching in the United States", "Silent Parade", "William Monroe Trotter", "Dyer Bill", "Presidency of Warren G. Harding", "Jessie Daniel Ames", "National Conference on Lynching", "Lynching of Irving and Herman Arthur", "Negro Sanhedrin", "George Edmund Haynes", "Sherman Minton", "Bill Dyer Anti-Lynching Bill", "Leonidas C. Dyer", "Death of Shedrick Thompson", "May 1918 lynchings", "James Weldon Johnson", "Hatton W. Sumners", "Martin C. Ansorge", "Harry M. Wurzbach", "Anti-lynching movement", "John Albert Williams", "Dyer Anti-Lynching Bill", "Alice Dunbar Nelson", "Caleb R. Layton", "Bertha G. Higgins", "John Steuart Curry", "Joseph I. France", "List of landmark African-American legislation", "Lynching", "Alice Mary Robertson", "History of St. Louis", "Moore's Ford lynchings", "William Borah", "May 1919", "Lee Slater Overman", "Walter Francis White", "Warren G. Harding"]}
    # ### Test Output (without alternate dash separation):
    # {"concept": "czechoslovak immigrants", "wikipedia_page_titles_appeared_in": ["List of people from Yonkers, New York", "Joseph Plavcan", "Maryland", "Belinda Bencic", "Patrick Mohr", "Yonkers, New York", "Western Fraternal Life Association", "Jon Ledecky", "Kerem Maharal", "Andrei Cherny", "Dancer in the Dark", "Ester, Alaska", "Brookside, Alabama", "Robert Maxwell", "Wild Mary Sudik", "Jim Puplava", "Fenar Ahmad", "Pinky and Perky", "Joe Manchin", "Leonard Paulu"]}
    # {"concept": "dyer antilynching bill", "wikipedia_page_titles_appeared_in": []}

    dict_text_search_fields_to_df_column = {
        "text":"count_unique_wiki_article_text_appeared_in",
        "page_title":"count_unique_wiki_article_title_appeared_in"
    }

    for text_search_field in dict_text_search_fields_to_df_column:
        print("Currently running %s" %text_search_field)
        with open(f"/work/nelsongroup/haque.s/chroniclingamerica/wikipedia_gender_concepts_establishment/output/untracked/chunked_output/{corpus_name}/searched_in_{text_search_field}/{output_code}_{chunked_file_basename}_found_in_wikipedia_{text_search_field}.json","a", encoding="utf-8") as f:     
            for dash_separated_concept in alex_street_dash_separated_concepts:
                print("%s" %dash_separated_concept)
                concept_to_wiki_title_docs = dict()
                concept_to_wiki_title_docs["concept"] = dash_separated_concept
                concept_to_wiki_title_docs["wikipedia_page_titles_appeared_in"] = set()
                alternate_concepts = [] ## This time we have some alternative dash separated concepts
                if dash_separated_concept:
                    alternate_concepts.append(dash_separated_concept)
                    alternate_concepts.append(dash_separated_concept.replace("-"," ").strip())
                for concept in alternate_concepts:
                    #print("current alternate concept", concept)
                    ## First I will convert the whole phrase into string and the lower and split it
                    ## then I will remove all the leading and trailing whitespace from the individual
                    ## tokens
                    concept_tokens = map(lambda x: x.strip(), str(concept).lower().strip().split())

                    ## Now building elasticsearch fuzzy match query
                    ## Refs
                    ## https://stackoverflow.com/questions/38816955/elasticsearch-fuzzy-phrases
                    ## https://stackoverflow.com/questions/53652765/elastic-search-match-phrase-fuzziness
                    nested_dict = lambda: defaultdict(nested_dict)
                    query=dict()
                    query["bool"] = dict()
                    query["bool"]["must"] = []
                    ## We are filtering for only namespace 0 which 
                    ## is about the articles only
                    query["bool"]["filter"] = [
                        {
                            "term":{
                                "ns":0
                            }
                        },
                        # {
                        #     "range":{
                        #         "timestamp":{
                        #             "gte": "2020-01-01"
                        #         }
                        #     }
                        # }
                    ]
                    span_doc = nested_dict()
                    span_doc["span_near"]["clauses"]=list()
                    span_doc["span_near"]["slop"]="1"
                    span_doc["span_near"]["in_order"]="true"

                    for token in concept_tokens:
                        nest = nested_dict()
                        nest["span_multi"]["match"]["fuzzy"][text_search_field]["value"]=token.strip()
                        nest["span_multi"]["match"]["fuzzy"][text_search_field]["fuzziness"]="AUTO" # https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#fuzziness
                        span_doc['span_near']['clauses'].append(json.loads(json.dumps(nest)))
                    query["bool"]["must"].append(span_doc)
                    
                    source = ["page_title"] #,"page_id","timestamp"] # Here the timestamp is the last revision timestamp
                    
                    for _id, _doc in ElasticScroll('http://localhost:9200', 'wikipedia-20200820', scroll_size=5000).scroll(source = source,query=query):
                        concept_to_wiki_title_docs["wikipedia_page_titles_appeared_in"].add(_doc["page_title"])
                concept_to_wiki_title_docs["wikipedia_page_titles_appeared_in"] = list(concept_to_wiki_title_docs["wikipedia_page_titles_appeared_in"])
                ## We are appending each concpet as a newline delimnited json
                json.dump(concept_to_wiki_title_docs, f, ensure_ascii=False)
                f.write("\n")