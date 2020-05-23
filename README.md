# Logstash Connector POC
_This repo is being used to proof out logstash and it's ability to assist in replicating an RDS database in Elasticsearch_

## Installations
 - [Elasticsearch][ES_URL]
 - [Logstash][]
 - [JDBC Driver][jdbc-driver-installation]

## Development Setup
 - Setup Python 3 virtual environment and install dependencies
 - Store a [dev.env][envs] file at the root of your project with the following configurations
 - Configure an alias in your shell profile such that `logstash` executes the `logstash` program on your machine. Example: `alias logstash=/usr/local/bin/logstash`

 ## Environment Configuration
 _You'll need to contribute a local file with the following configurations. This file will be used to populate your environment when calling `app/config.py` explicitly or when running the `run_logstash.sh` file._
 ```sh
    ELASTICSEARCH_URL=""
    RDS_PASSWORD=""
    RDS_USERNAME=""
    JDBC_DRIVER_LIBRARY=""
    JDBC_CONNECTION_STRING=""
    SQL_DB_NAME=""
    JDBC_DRIVER_CLASS=""
```

## Running the Logstash Project

The entrypoint for this project is `run_logstash.sh`. If you step through the file you will notice it's doing a few things. 
 - `python app/config.py` is called, which parses your `dev.env` file and produces a `dev_env.sh` file, which will export all your variables to your primary shell process
 - `source dev_env.sh` sources the aforementioned file.
 - `logstash` comes with a `-r` flag which watches for changes in the `.conf` file which configures the pipeline. This is useful for debugging purposes.
 - The `-f` flag is used as an identifier that the next argument will be the path the configuration file. 

 _Things to note:_ 
 - If running a pipeline who's output is an elasticsearch instance, make sure elasticsearch is up and running. 

## Python Elasticsearch interface
_Primary manual interface for interacting with Elasticsearch._
 - Mappings for each index are created in the `index_settings.py`  
 - Calling `python app/interface.py` will instantiate the mappings in the Elasticsearch instance for each defined index in `index_settings.py`
 - `search.py` will eventually be used to query against the Elasticsearch instance

## Pipeline Configurations
_Each ls_conf file is a different [pipeline configuration][ls_conf] for use with Logstash._

Each logstash.conf file is made up of 3 parts: input, filter, and output. The `*_dev.conf` files are a workaround in which the output dumps the results to a json file for quicker development, preventing the need to query an elasticsearch index. 

##### input
 - used to establish a connection with a database
 - establishes a secure connection with the database via the JDBC (Java Database Connector)
 - runs a query against the database (queries stored in `sql_scripts`)
 
##### filter
 - parses and configures results of the input query and prepares them for delivery to the output

##### output
 - establishes a secure connection with the outbound database via the JDBC 
 - there are also various textual output streams that can be used

For more detail, checkout the logstash docs, specifically: 
 - [JDBC Input Plugin][jdbc-input-plugin]
 - [Filter Aggregate Plugin][filter-aggregate]

_Note the inline comments for more information..._

```sh
input {
    # Connection to the jdbc connector. Each ${var} is picked up from the shell environment
  jdbc {
    jdbc_driver_library => "${JDBC_DRIVER_LIBRARY}"
    jdbc_connection_string => "${JDBC_CONNECTION_STRING}"
    jdbc_driver_class => "${JDBC_DRIVER_CLASS}"
    jdbc_user => "${RDS_USERNAME}"
    jdbc_password => "${RDS_PASSWORD}"
    # Path to the sql query to be executed and consequently mapped to elasticsearch
    statement_filepath => "sql_scripts/update_index.sql"
  }
}

filter {
    # Assumes a jsonified RDS query response from
    json{
      id => "id"
      source => "rows"
      remove_field => "rows"
    }
} 
output {
    # ES configuration. Notice there are no mappings here. Mappings are configured by the python interface as of now
  elasticsearch {
    document_id => "%{task_id}"
    document_type => "index"
    index => "indexs"
    codec => "json"
    hosts => "${ELASTICSEARCH_URL}"
  }
}

```

## Other Resources 
 - Aggregate
    - [Aggregate and Index Data into Elasticsearch using Logstash, JDBC – Experiences Unlimited](https://sanaulla.info/2017/10/27/aggregate-and-index-data-into-elasticsearch-using-logstash-jdbc/)
 
 - Mapping
    - [Mapping | Elasticsearch Reference 7.6 | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping.html#mapping-limit-settings)

 - Indexing
    - [General recommendations | Elasticsearch Reference 7.6 | Elastic](https://www.elastic.co/guide/en/elasticsearch/reference/current/general-recommendations.html)
    - [Four ways to index relational data in Elasticsearch – Voormedia](https://voormedia.com/blog/2014/06/four-ways-to-index-relational-data-in-elasticsearch)



 [ES_URL]: https://www.elastic.co/elasticsearch/?ultron=[EL]-[B]-[AMER]-US+CA-Exact&blade=adwords-s&Device=c&thor=elasticsearch%20install&gclid=Cj0KCQiAtOjyBRC0ARIsAIpJyGPa567p95L6DMerKt8Zf3Blm-ld_M6UWNLl6Zh0ll-aWRvHXe4ld2YaApmWEALw_wcB

 [envs]: #markdown-header-environment-configuration

 [ls_conf]: https://www.elastic.co/guide/en/logstash/current/configuration.html

 [jdbc-input-plugin]: https://www.elastic.co/guide/en/logstash/current/plugins-inputs-jdbc.html

 [filter-aggregate]: https://www.elastic.co/guide/en/logstash/current/plugins-filters-aggregate.html

 [jdbc-driver-installation]: https://www.microsoft.com/en-us/download/details.aspx?id=100855

 [logstash]: 