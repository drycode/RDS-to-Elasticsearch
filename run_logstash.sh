#!/bin/bash
# TODO: You'll need to alias the default logstash command or update this file

# TODO: You'll need the dev.env file to generate the appropriate environment configurations

# TODO: Run multiple logstash pipelines
python app/config.py
source dev_env.sh

first_arg=$(echo $1 | tr '[:upper:]' '[:lower:]')

if [[ ${first_arg} == "debug" ]]; then
    logstash --log.level=info -r -f ls_confs/debug/update_es_dev.conf
elif [[ ${first_arg} == "fresh" ]]; then
    logstash --log.level=error -r -f ls_confs/fresh_pull/fresh_pull_index.conf
elif [[ ${first_arg:0:2} == "update" ]]; then
    logstash --log.level=error -r -f ls_confs/update_insert/update_insert_index.conf
elif [[ ${first_arg:0:2} == "delete" ]]; then
    logstash --log.level=error -r -f ls_confs/delete/delete_index.conf
elif [[ ${first_arg} == "pipeline" ]]; then
    logstash  --path.settings=ls_settings
else
    echo "Please pass a valid flag."
fi