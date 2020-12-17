#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

import requests


class ElasticBulk(object):
    """Class for indexing documents in bulk"""

    def __init__(self, host, index, doc_type="_doc", session=requests.session(), bulk_size=1000):
        """Instantiates an ElasticBulk object, sets default values

        Args:
            host (str): Elasticsearch host url. Example: ``http://localhost:9200``.
            index (str): Elasticsearch index name. Example: ``my_index``.
            doc_type (str): Elasticsearch document type. Example: ``_doc``.
            session (:obj:`Session`, optional): Http request session object.
                If not provided, creates a new session object.
            bulk_size (int, optional): Bulk operation size. Default: ``1000``.
        """
        self.session = session if session else requests.session()
        self.bulk_url = f'{host}/{index}/{doc_type}/_bulk'
        self.bulk_size = bulk_size
        self.headers = {'Content-Type': 'application/x-ndjson'}
    
    def upload_bulk(self, generator_fn):
        """Uploads documents in bulk

        Args:
            "generator_fn (:func:): A generator function for pulling data
        """
        docs = list()
        entries = 0

        for doc in generator_fn():
            docs.append({"index": {}})
            docs.append(doc)
            entries += 1

            if entries % self.bulk_size == 0:
                bulk_data = "\n".join(json.dumps(s) for s in docs) + "\n"
                response = self.session.post(url=self.bulk_url, data=bulk_data, headers=self.headers)
                response.raise_for_status()
                docs.clear()

        if entries % self.bulk_size != 0:
            bulk_data = "\n".join(json.dumps(s) for s in docs) + "\n"
            response = self.session.post(url=self.bulk_url, data=bulk_data, headers=self.headers)
            response.raise_for_status()
            docs.clear()

        return True
