# Hadoop, Hive, Presto and Minio on Docker

Docker Compose for running Hadoop, Hive, Minio and Presto in Docker.

Compared to [`startburstdata/presto-minio`](https://github.com/starburstdata/presto-minio), this fork does not use high-level Docker images for Hadoop and Presto.

See also [`minio/presto-minio`](https://github.com/minio/presto-minio).

The configuration for Hive metastore is based on [this repository](https://github.com/treeverse/blog-presto-local).

Hadoop+Hive configuration is based on [this Dockerfile from Hive](https://github.com/prestodb/docker-images/blob/master/prestodb/hive3.1-hive/Dockerfile).

Presto configuration is based on the [official documentation](https://prestodb.io/docs/current/installation/deployment.html).

## Resources

- [Interactive SQL query with Apache Presto on MinIO Cloud Storage](https://blog.min.io/interactive-sql-query-with-presto-on-minio-cloud-storage/)
- [HCatalog](https://cwiki.apache.org/confluence/display/Hive/HCatalog)
- [Hive Metastore: Why It's Still Here and What Can Replace it?](https://lakefs.io/hive-metastore-why-its-still-here-and-what-can-replace-it/)
- [Quick Guide for running Presto Locally on S3](https://lakefs.io/the-quick-guide-for-running-presto-locally-on-s3/)
- [`blog-presto-local`](https://github.com/treeverse/blog-presto-local): The accompanying repository

##  Running full stack

Run `docker-compose build && docker-compose up --abort-on-container-exit`.

Docker Compose publishes the following ports:

- Minio Browser: [`http://127.0.0.1:9001/`](http://localhost:9001).
- Presto WebUI: [`http://127.0.0.1:8080/`](http://localhost:8080)

Use `docker-compose exec presto /usr/local/bin/presto` to connect to Presto (see usage below).

## Usage

First create a table in the Hive metastore. Note that the location `s3a://customer-data-text/` points to data that's been mounted to the Minio container.

Run `docker-compose exec hive hive` and create a table:

```
hive> use default;
hive> create external table customer_text(id string, fname string, lname string) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE location 's3a://customer-data-text/';
hive> select * from customer_text;
```

Next, query the data from Presto. Run `docker-compose exec presto /usr/local/bin/presto` and make queries:

```
presto> use minio.default;

presto:default> select * from customer_text;
 id | fname | lname 
----+-------+-------
 5  | Bob   | Jones 
 6  | Phil  | Brune 
(2 rows)

# FIXME: This fails for some reason due to Hadoop timeout?
presto:default> show tables;
     Table     
---------------  
 customer_text 
(2 rows)
```

Next, create a new table via Presto and copy the CSV data into ORC format. Before this, make a new bucket in Minio named `customer-data-orc`.

```
presto:default> create table customer_orc(id varchar,fname varchar,lname varchar) with (format = 'ORC', external_location = 's3a://customer-data-orc/');
CREATE TABLE

presto:default> insert into customer_orc select * from customer_text;
INSERT: 2 rows

presto:default> select * from customer_orc;
 id | fname | lname 
----+-------+-------
 5  | Bob   | Jones 
 6  | Phil  | Brune
```

### Parquet

```
hive> create external table customer_text(id string, fname string, lname string) STORED AS PARQUET location 's3a://parquet/'
```

## Python

Install dependencies:

```bash
$ pip install -r requirements.txt
```

Generate data:

```bash
$ python generate_data.py
```

Read data from Pandas:

```bash
$ python read.py
```

## Docker

### Build Presto image

```
docker build -f prestodb/Dockerfile . -t prestodb:latest
```

### Build Hadoop+Hive image

Customize the start-up by modifying [`hive/files`](./hive/files), especially `root/setup.sh`.

Build:

```
docker build -f hive/Dockerfile -t hive:latest .
```

Run:

```
docker run --rm -p 9083:9083 -p 10000:10000 -p 1180:1180 hive:latest
```

Enter beeline shell:

```bash
docker exec -it CONTAINER_NAME beeline
```

In Beeline shell, connect to Hive2:

```
beeline> !connect jdbc:hive2://localhost:10000 '' ''
```