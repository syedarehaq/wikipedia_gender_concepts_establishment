#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

class ElasticScroll(object):
    """Manages scroll contexts for elasticsearch scroll queries.
    Args:
        host (str): Elasticsearch host url. Example: ``http://localhost:9200``.
        index (str): Elasticsearch index name. Example: ``my_index``.
        session (:obj:`Session`, optional): Http request session object.
            If not provided, creates a new session object.
        scroll_ctx (str, optional): Scroll context time. Default: ``1m``.
        scroll_size (int, optional): Scroll page size. Default: ``20``.

    Example:
    query = {
        "match": {
            "page_title": {
                 "query": "documentation"
                }
            }
        }
 
    for _id, _doc in ElasticScroll('http://localhost:9200', 'wikipedia-20200820', scroll_size=5).scroll(source = ["page_title"],query=query):
        print(f'{_id}:\n{json.dumps(_doc, indent=2)}')
        break 

    """

    def __init__(self, host, index, session=requests.session(), scroll_ctx='1m', scroll_size=20):
        self.session = session if session else requests.session()
        self.scroll_ctx = scroll_ctx
        self.scroll_ids = {}
        self.setup_url = f'{host}/{index}/_search?scroll={scroll_ctx}&size={scroll_size}'
        self.scroll_url = f'{host}/_search/scroll'
    
    def scroll(self, source = None, query={'match_all': {}}):
        """A generator function to scroll trhough all documents from an index.
        Args:
            query (:obj:`dict`, optional): Elasticsearch query json.
                Default: ``{'match_all': {}}``.
        
        Yields:
            id (str): ``_id`` from Elasticsearch ``hit`` object.
            doc (:obj:`dict`): ``_source`` from Elasticsearch ``hit`` object.
        
        Raises:
            requests.exceptions.HTTPError: If Elasticsearch REST client sends an error.
        """
        if not source:
            queries = [{'sort': ['_doc'], 'query': query}, {'scroll': self.scroll_ctx}]
        else:
            queries = [{'sort': ['_doc'], 'query': query, "_source": source}, {'scroll': self.scroll_ctx}]
        #queries = [{'sort': ['_doc'], 'query': query}, {'scroll': self.scroll_ctx}]
        urls = [self.setup_url, self.scroll_url]
        #print(queries)
        has_scroll_ctx = False
        while True:
            proxies = {
                'http': None,
                'https': None,
            }
            response = self.session.post(url=urls[has_scroll_ctx], json=queries[has_scroll_ctx], proxies=proxies)
            response.raise_for_status()
            json_data = response.json()
            scroll_id, has_scroll_ctx = json_data.get('_scroll_id'), True
            self.scroll_ids[scroll_id] = True
            if len(json_data['hits']['hits']) == 0: break
            for hit in json_data['hits']['hits']: yield hit['_id'], hit['_source']
            queries[has_scroll_ctx]['scroll_id'] = scroll_id
        
        self.session.delete(url=urls[1], json={'scroll_id': list(self.scroll_ids.keys())})
        self.scroll_ids.clear()

