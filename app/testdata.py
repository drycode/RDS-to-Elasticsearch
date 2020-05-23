from collections import namedtuple
from time import time
from pprint import pprint

UserQuery = namedtuple("UserQuery", "name email age")
BlogQuery = namedtuple(
    "BlogQuery", "title body user_id created", defaults=[None, None, None, None]
)

user_query1 = UserQuery(name="John Smith", email="jsmith@gmail.com", age=34)
blog_query1 = BlogQuery(user_id="jsmith123")
QUERIES = {"u1": user_query1, "b1": blog_query1}

if __name__ == "__main__":
    """
    For quick testing...
    """
    from interface import ElasticSearchInterface

    es_client = ElasticSearchInterface()
    from search_queries import ProprietarySearch

    for query in QUERIES:
        if isinstance(query, UserQuery):
            s = ProprietarySearch.user_search(**query._asdict())
        else:
            s = ProprietarySearch.blog_search(**query._asdict())
        start = time()
        response = es_client.query_index(s)
        end = time()
        print(f"Response Time: {(end - start) * 1000}")
        print(f"Total Hits: {response.hits.total.value}")
        pprint([hit["_source"]["item"] for hit in response.to_dict()["hits"]["hits"]])
        print()
