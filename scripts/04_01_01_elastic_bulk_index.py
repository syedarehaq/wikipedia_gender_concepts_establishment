# -*- coding: utf-8 -*-

"""
Summary:
    This is a helper file to store contents of a newline delimited json
    file into an elastic search index
Input:
    read the argparse, it takes three arguments
    write python 04_01_01_elastic_bulk_index.py --help
Output
    Puts the contents of a newline delimited json files
    into an elasticsearch object
"""
import json
import requests
import argparse
## imported from custom helper library accompanying this project
from helpers.Elasticsearch_Bulk_Indexing import ElasticBulk

# %%
output_code = "04_01_01"


# %%
parser = argparse.ArgumentParser(
        description="Script to bulk insert a newline separated json file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i','--index', help='Name of the elastic search index')
parser.add_argument('-p', '--port', type=int, help='elasticsearch port in localhost')
parser.add_argument('-f', '--filename', help='a newline delimited json file')
## See python argparse default vs const
## https://stackoverflow.com/questions/24272228/default-value-of-commandline-parameters-when-no-value-is-provided?noredirect=1&lq=1
parser.add_argument("-b", "--bulksize", type=int, help="size of the bulk operation", nargs="?", default=1000, const=1000)
args = parser.parse_args()

# %%
# Load the json file and yield it to elastic bulk insert
es_bulk = ElasticBulk(f"http://localhost:{args.port}", f"{args.index}", bulk_size=args.bulksize)

def lazy_read_file_line_by_line():
    with open(args.filename,"r") as f:
        for line in f:
            yield line

es_bulk.upload_bulk(generator_fn=lazy_read_file_line_by_line)