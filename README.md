# Presto & Minio on Docker

Hadoop+Hive configuration is based on [this Dockerfile from Hive](https://github.com/prestodb/docker-images/blob/master/prestodb/hive3.1-hive/Dockerfile).

Presto configuration is based on the [official documentation](https://prestodb.io/docs/current/installation/deployment.html).

Compared to the original repository, this fork does not use high-level Docker images for Hadoop and Presto.

##  Running full stack

Run `docker-compose up --abort-on-container-exit`.

Minio Browser: [`http://127.0.0.1:9001/`](http://localhost:9001).
Presto WebUI: [`http://127.0.0.1:8080/`](http://localhost:8080)
HDFS: [`http://localhost:9870`](http://localhost:9870)

Use `docker exec -it presto presto-cli` to connect to Presto.

## Usage

First create a table in the Hive metastore. Note that the location `'s3a://customer-data-text/'` points to data that already exists in the Minio container.

Run `docker exec -it hadoop-master hive`. 

```bash
hive> use default;
hive> create external table customer_text(id string, fname string, lname string) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE location 's3a://customer-data-text/';
hive> select * from customer_text;
```

Next let's query the data from Presto. Run `docker exec -it presto /usr/local/bin/presto`

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

Next, let's create a new table via Presto and copy the CSV data into ORC format. Before you do that, make a new bucket in Minio named `customer-data-orc`.

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