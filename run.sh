#!/usr/bin/env bash
set -e

SCRIPT_PATH=`dirname $0`
ES_DIR=$SCRIPT_PATH/elasticsearch

if ls $ES_DIR/elasticsearch-5.4.0.tar.gz; then
    echo "Found ElasticSearch, skip install"
else
    echo "Downloading ElasticSearch"
    mkdir -p $ES_DIR
    pushd $ES_DIR
    wget --continue https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.4.0.tar.gz
    tar xf elasticsearch-5.4.0.tar.gz
    elasticsearch-5.4.0/bin/elasticsearch-plugin install analysis-icu
    popd
fi

echo "Starting ElasticSearch"
$ES_DIR/elasticsearch-5.4.0/bin/elasticsearch
