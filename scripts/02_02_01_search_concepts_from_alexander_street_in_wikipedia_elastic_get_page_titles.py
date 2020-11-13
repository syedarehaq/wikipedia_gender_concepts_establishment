# -*- coding: utf-8 -*-

"""
Summary:
    In this script we will read all the concpets that are coming from
    alexander street and search in how many titles of wikipedia they appear
    and in how many article text they appear
Input:
    The filtered concept list
    ../input/raw/phrases_filtered_20201112_laura_rebekah.csv
Output
    It will create a json for each of the concept and put corresponding page titles
    and last revision data
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
output_code = "02_02_01"

# %%
## Load the alexander streets concpets created by Laura
df_concepts = pd.read_csv("../input/raw/phrases_filtered_20201112_laura_rebekah.csv")

alex_street_concepts = df_concepts["concept_from_alex_street"].values
### For testing
#alex_street_concepts = ["labor unionism among negros","aaa program","acme art"] ## It is here for debugging purpose

df_concept_appearence_count = pd.DataFrame(columns=["concept_from_alex_street",
    "count_unique_wiki_article_text_appeared_in",
    "count_unique_wiki_article_title_appeared_in",
    "count_unique_alexander_street_docs_appeared_in"])

dict_text_search_fields_to_df_column = {
    "text":"count_unique_wiki_article_text_appeared_in",
    "page_title":"count_unique_wiki_article_title_appeared_in"
}

for text_search_field in dict_text_search_fields_to_df_column:
    concept_to_wiki_title_docs = dict()
    for concept in tqdm(alex_street_concepts):
        concept_to_wiki_title_docs[concept] = list()
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
            nest["span_multi"]["match"]["fuzzy"][text_search_field]["value"]=token
            nest["span_multi"]["match"]["fuzzy"][text_search_field]["fuzziness"]="AUTO" # https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#fuzziness
            span_doc['span_near']['clauses'].append(json.loads(json.dumps(nest)))
        query["bool"]["must"].append(span_doc)

        query_doc = dict()
        query_doc["query"] = query
        query_doc["_source"] = ["page_title","page_id","timestamp"] # Here the timestamp is the last revision timestamp
        res = requests.post(url="http://localhost:9200/wikipedia-20200820/_search", json= query_doc)
        ## if res.ok is True then
        ## The res object has a json that looks like below
        """
        {'count': 2,
         '_shards': {'total': 1, 'successful': 1, 'skipped': 0, 'failed': 0}}
        """
        if res.ok:
            result_doc = res.json()
            for hit in result_doc["hits"]["hits"]:
                concept_to_wiki_title_docs[concept].append(hit["_source"])
    #df_concept_appearence_count = df_concept_appearence_count.append(count_doc, ignore_index=True)
    with open("../output/%s_alex_street_concept_to_wiki_pagetitles_of_searched_%s.json" %(output_code,text_search_field),"w", encoding="utf-8") as f:
        json.dump(concept_to_wiki_title_docs, f, ensure_ascii=False)


## Later to collect the page title etc.
#res = requests.post(url="http://localhost:9200/wikipedia-20200820/_search", json = query_doc)

