USER_SETTINGS = {
    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
    "mappings": {
        "properties": {
            "age": {"type": "integer"},
            "email": {"type": "keyword"},
            "name": {"type": "text"},
        }
    },
}


BLOG_SETTINGS = {
    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
    "mappings": {
        "properties": {
            "title": {"type": "string"},
            "body": {"type": "string"},
            "user_id": {"type": "string", "index": "not_analyzed"},
            "created": {
                "type": "date",
                "format": "strict_date_optional_time||epoch_millis",
            },
        }
    },
}

SETTINGS = {"users": USER_SETTINGS, "blog": BLOG_SETTINGS}
