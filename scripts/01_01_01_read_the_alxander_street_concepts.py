# -*- coding: utf-8 -*-

"""
Summary:
    In this script we are reading the concepts file provided by Laura.
    Laura asked me to ignore all the bigrams and try to see what uni-gram
    bi-gramas, tri-grams and n grams are meaningful and is searchable to 
    wikipedia concepts
Input:
    The phrases file provided by Laura
    ../input/raw/phrases1.json
Output
    It will create a csv
"""

import json
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import csv

# %%
output_code = "01_01_01"

# %%
## Load the alexander streets concpets created by Laura
with open("../input/raw/phrases1.json", "r") as f:
    phrases = json.load(f)

def get_ngram_size(string):
    return len(string.split())
# %%
## First read all the unique non-unigrams and count them
## Actually we added unigrams too, just to make sure we do 
## miss any important unigram
count = 0
concept_count = defaultdict(int)
for doc_id, list_of_concepts in phrases.items():
    count += 1
    ## Some of the concepts are 
    ## floating point nan objects
    ## we are avoiding them
    ## example, '3566024': nan,
    if type(list_of_concepts) != float:
        ## We will put all the concepts that are not unigram
        ## count their incidence

        ## Example concepts: "delinquent negro girls", "delinquent black girls"
        all_concepts = [concept for concept,val in list_of_concepts if get_ngram_size(concept) > 0]
        for concept in all_concepts:
        	concept_count[concept] += 1 

## A concept "negro trail blazers" is in wikipedia which get redirected to Delilah Beasley

## Draw a histogram of concept count:
counter_dict = concept_count
fig,ax = plt.subplots(figsize = (30,5))
val, count = zip(*sorted(Counter(counter_dict.values()).items()))
ax.bar(range(len(val)),count,color='#0504aa', alpha=0.7)
xticks = range(len(val))
ax.set_xticks(xticks)
ax.set_xticklabels(val,rotation=90, fontsize=5)
ax.set_ylabel("Number of unique such n-grams")
ax.set_xlabel("Number of times an n-gram appeared as a concpet in Alexander Street dataset")
#ax.set_xlim(0.4,len(val)+1.5)
#ax.set_ylim(0,sorted(count, reverse = True)[1]+1) ## Taking the second max of the count values as the ylim
ax.grid(axis="y", alpha = 0.5)
#ax.set_title("Ranking coming from %s" %rank_type)
plt.savefig("../figures/%s_ngram_appearence_in_diff_docs_histogram_all.png" %(output_code), dpi = 150)
plt.show()


## We can see that a major portion of the concepts happened only once in the 
## whole list of concepts.
## Lets print the concept list and their counts in descending order
writelines = []
writelines.append(["concept", "number_of_alexander_street_docs_appeared_in"])
writelines.extend(sorted(concept_count.items(), key = lambda x: x[1], reverse=True))
with open("../output/%s_alex_street_concept_appearence_count_descending.csv" %output_code, "w") as f:
    writer = csv.writer(f)
    writer.writerows(writelines)