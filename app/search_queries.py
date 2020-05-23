from abc import ABC

from elasticsearch_dsl import Document, Mapping
from elasticsearch_dsl.search import Search


class Blog(Document):
    class Meta:
        mapping = Mapping.from_es("blog")
        index = "blog"


class User(Document):
    class Meta:
        mapping = Mapping.from_es("user")
        index = "user"


class SearchClass(ABC):
    @staticmethod
    def search(*, document: Document, sort, limit, offset, **kwargs):
        s = document.search()

        # TODO: Define search criteria
        if sort:
            s = SearchClass._sort_helper(s, sort, kwargs)

        s = SearchClass._pagination_helper(s, limit, offset)

        return s

    @staticmethod
    def _sort_helper(s, sort, categories):
        """    
        To specify sorting order, use the .sort() method:
        
        s = Search().sort(
            'category',
            '-title',
            {"lines" : {"order" : "asc", "mode" : "avg"}}
        )
        
        It accepts positional arguments which can be either strings or dictionaries. String value is a field name, optionally prefixed by the - sign to specify a descending order.
        """
        pass

    @staticmethod
    def _pagination_helper(s, limit, offset):
        """
        Pagination
        To specify the from/size parameters, use the Python slicing API:

        s = s[10:20]
        # {"from": 10, "size": 10}
        If you want to access all the documents matched by your query you can use the scan method which uses the scan/scroll elasticsearch API:

        for hit in s.scan():
            print(hit.title)
        
        Note that in this case the results won't be sorted.
        """
        return s[offset : offset + limit]


class ProprietarySearch(SearchClass):
    @staticmethod
    def user_search(*args, **kwargs):
        s = super(ProprietarySearch, ProprietarySearch).search(
            # TODO: Define search here
            document=User
        )
        if kwargs.get("name"):
            s = s.query("fuzzy", name=kwargs.get("name"))
        return s.index("users")

    @staticmethod
    def blog_search(*args, **kwargs):
        s = super(ProprietarySearch, ProprietarySearch).search(
            # TODO: Define search here
            document=Blog
        )
        if kwargs.get("title"):
            s = s.query("fuzzy", title=kwargs.get("title"))
        return s.index("blog")


es_queries = {
    "users": ProprietarySearch.user_search,
    "blog": ProprietarySearch.blog_search,
}
