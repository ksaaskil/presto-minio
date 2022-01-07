#!/bin/bash -x

[[ -n "${DB_URI}" ]] && wait-for-it.sh ${DB_URI}

# Sleep just in case MariaDB is not ready to accept connections
echo "Sleeping for 10 seconds..."
sleep 10

echo "Checking if schema has been initialized..."
[[ ! -f initSchema.completed ]] && schematool -dbType mysql -initSchema && touch initSchema.completed

echo "Starting Hive metastore..."
hive --service metastore
