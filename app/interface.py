import logging
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections

from config import Config
from index_settings import SETTINGS
from testdata import test_queries


class ElasticSearchInterface:
    es = (
        connections.create_connection(hosts=[Config.ELASTICSEARCH_URL])
        if Config.ELASTICSEARCH_URL
        else None
    )

    if not es.ping():
        print("DEBUG: Trouble connecting to the ES Cluster")
        logging.basicConfig(level=logging.ERROR)

    @classmethod
    def create_index(cls, index_name):
        created = False
        try:
            if not cls.es.indices.exists(index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                cls.es.indices.create(index=index_name, body=SETTINGS[index_name])
                print("Created Index")
            created = True
        except Exception as ex:
            print(str(ex))
        finally:
            return created

    @classmethod
    def refresh_index(cls, index_name=None):
        """
        # TODO: If an index exists, but you would like to recreate the mappings
        # Will delete all contents in that index
        """
        if index_name:
            cls.delete_index(index_name)
            cls.create_index(index_name)
        else:
            for index in SETTINGS.keys():
                cls.delete_index(index)
                cls.create_index(index)

    @classmethod
    def delete_index(cls, index_name):
        if cls.es.indices.exists(index_name):
            cls.es.indices.delete(index=index_name)

    @classmethod
    def query_index(cls, s):
        response = s.execute()
        return response

    @classmethod
    def query_multiple_indices(cls):
        pass

    @staticmethod
    def transform_response(response):
        # TODO: Configure response to conform to frontend?
        return response
