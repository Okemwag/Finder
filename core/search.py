from elasticsearch import Elasticsearch


def search(query):
    es = Elasticsearch()
    res = es.search(index="my-index", body={"query": {"match": {"title": query}}})
    return res['hits']['hits']

    