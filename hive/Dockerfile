# See https://github.com/prestodb/docker-images/blob/master/prestodb/hive3.1-hive/Dockerfile
FROM openjdk:8-jre

RUN apt-get update
RUN apt-get install -y wget python less

ARG HADOOP_VERSION=3.1.2
ARG HIVE_VERSION=3.1.2

ARG HADOOP_BINARY_PATH=https://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz
ARG HIVE_BINARY_PATH=https://dlcdn.apache.org/hive/hive-$HIVE_VERSION/apache-hive-$HIVE_VERSION-bin.tar.gz

RUN curl -o /tmp/hadoop.tar.gz --url $HADOOP_BINARY_PATH && \
    tar xzf /tmp/hadoop.tar.gz --directory /opt && mv /opt/hadoop-$HADOOP_VERSION /opt/hadoop

RUN curl -o /tmp/hive.tar.gz --url $HIVE_BINARY_PATH && \
    tar xzf /tmp/hive.tar.gz --directory /opt && mv /opt/apache-hive-${HIVE_VERSION}-bin /opt/hive

ARG MYSQL_CONNECTOR_VERSION=8.0.13
ARG AWS_SDK_VERSION=1.11.906
RUN mkdir /opt/hive/auxlib && \
    curl -o /opt/hive/auxlib/mysql-connector-java-$MYSQL_CONNECTOR_VERSION.jar https://repo1.maven.org/maven2/mysql/mysql-connector-java/$MYSQL_CONNECTOR_VERSION/mysql-connector-java-$MYSQL_CONNECTOR_VERSION.jar && \
    curl -o /opt/hive/auxlib/aws-java-sdk-core-$AWS_SDK_VERSION.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-core/$AWS_SDK_VERSION/aws-java-sdk-core-$AWS_SDK_VERSION.jar && \
    curl -o /opt/hive/auxlib/aws-java-sdk-s3-$AWS_SDK_VERSION.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/$AWS_SDK_VERSION/aws-java-sdk-s3-$AWS_SDK_VERSION.jar

RUN apt-get install -y mariadb-server supervisor

ENV HADOOP_HOME=/opt/hadoop
ENV HIVE_HOME=/opt/hive
ENV HADOOP_CLASSPATH=${HADOOP_HOME}/share/hadoop/tools/lib/*
ENV PATH=${HIVE_HOME}/bin:${HADOOP_HOME}/bin:${PATH}

COPY ./hive/files /

# Run setup script
RUN /root/setup.sh

# HDFS port
EXPOSE 9000 9870

# HIVE Metastore port
EXPOSE 9083 10000

EXPOSE 1180

CMD /root/entrypoint.sh
