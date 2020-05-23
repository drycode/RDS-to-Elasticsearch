import argparse
from pprint import pprint

from interface import ElasticSearchInterface
from search_queries import es_queries
from testdata import QUERIES

es_client = ElasticSearchInterface()


def search(args):
    query = es_queries[args.index](QUERIES[args.query_id])
    pprint(es_client.query_index(query))


def refresh(args):
    if args.index:
        es_client.refresh_index(args.index)
    else:
        es_client.refresh_index()
    print("Index refreshed.")


cli = argparse.ArgumentParser(
    description="A simple cli tool for use with the Elasticsearch cluster."
)

subparsers = cli.add_subparsers(
    title="subcommands", description="valid subcommands", help="sub-command-help"
)

search_parser = subparsers.add_parser(
    "search", help="Must enter a valid index and query key to search."
)

search_parser.add_argument(
    "-i", "--index", type=str, help="Given index to process a query on.", required=True
)
search_parser.set_defaults(func=search)


refresh_parser = subparsers.add_parser(
    "refresh", help="Must enter a valid index and query key to search."
)
refresh_parser.add_argument(
    "-i", "--index", type=str, help="Given index to process a query on.", required=True
)
refresh_parser.set_defaults(func=refresh)

args = cli.parse_args()
args.func(args)
