# -*- coding: utf-8 -*-

"""
Summary:
    In this script we will read a list of concepts and search the number of page
    titles they appeared in and also the number of page contents they appeared
    in. If there is a dash in a concpet we remove the dash and replace by white
    and then create the search token from the whitespaces
Input:
    A concpet list and the column which contains the concepts
    e.g. 
    ../input/raw/brown_phrases.csv
Output
    It will create a json for each of the concept and put corresponding counts
    in two files titled
    ../output/02_04_01_corpus_name_concept_to_wiki_pagetitles_of_searched_text.json
    ../output/02_04_01_corpus_name_concept_to_wiki_pagetitles_of_searched_page_title.json
"""

import json
from collections import Counter, defaultdict
import csv
import pandas as pd
import requests
import pprint
from tqdm import tqdm
## imported from custom helper library accompanying this project
from helpers.elastic_scroll import ElasticScroll

# %%
output_code = "02_04_02"
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
    print(f"Currently running {text_search_field}")
    with open(f"../output/untracked/{output_code}_{base_fname}_to_wiki_pagetitles_of_searched_{text_search_field}.json", "a", encoding="utf-8") as f:     
        for concept in tqdm(concepts_to_search_for):
            #print("current broad concept", dash_separated_concept)
            concept_to_wiki_title_docs = dict()
            if "-" in concept:
                concept = concept.replace("-"," ").strip()
            concept_to_wiki_title_docs["concept"] = concept
            concept_to_wiki_title_docs["count_wikipedia_pages_appeared_in"] = 0
            alternate_concepts = [] ## This time we have some alternative dash separated concepts
            alternate_concepts.append(concept)
            ## Checking if a concept has das in it
            ## Some example: encouraging self-help
            
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
                
                ## In case of count, we do not need a source
                #source = ["page_title"] #,"page_id","timestamp"] # Here the timestamp is the last revision timestamp
                
                query_doc["query"] = query
                
                for _id, _doc in ElasticScroll('http://localhost:9200', 'wikipedia-20200820', scroll_size=9999).scroll(source = source,query=query):
                    concept_to_wiki_title_docs["wikipedia_page_titles_appeared_in"].add(_doc["page_title"])
            concept_to_wiki_title_docs["wikipedia_page_titles_appeared_in"] = list(concept_to_wiki_title_docs["wikipedia_page_titles_appeared_in"])
            ## We are appending each concpet as a newline delimnited json
            json.dump(concept_to_wiki_title_docs, f, ensure_ascii=False)
            f.write("\n")