#!/bin/bash -x

[[ -n "${DB_URI}" ]] && /root/wait-for-it.sh ${DB_URI}

[[ ! -f initSchema.completed ]] && schematool -dbType mysql -initSchema && touch initSchema.completed

hive --service metastore
