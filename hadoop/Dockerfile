
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    python3 \
    openssh-server \
    openssh-client \
    curl \
    ca-certificates \
    procps \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV PATH="${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:${PATH}"

RUN curl -fsSL \
    https://downloads.apache.org/hadoop/common/hadoop-3.5.0/hadoop-3.5.0.tar.gz \
    -o /tmp/hadoop.tar.gz \
    && curl -fsSL \
    https://downloads.apache.org/hadoop/common/hadoop-3.5.0/hadoop-3.5.0.tar.gz.sha512 \
    -o /tmp/hadoop.sha512 \
    && sed -n 's/^SHA512 (.*) = //p' /tmp/hadoop.sha512 \
    | awk '{print $1 "  /tmp/hadoop.tar.gz"}' \
    | sha512sum -c - \
    && mkdir -p /opt/hadoop \
    && tar -xzf /tmp/hadoop.tar.gz -C /opt/hadoop --strip-components=1 \
    && rm /tmp/hadoop.tar.gz /tmp/hadoop.sha512

RUN echo "export JAVA_HOME=${JAVA_HOME}" >> \
    /opt/hadoop/etc/hadoop/hadoop-env.sh

RUN useradd -m -s /bin/bash hadoop \
    && mkdir -p /run/sshd /home/hadoop/.ssh /data/input /data/output \
    && chmod 700 /home/hadoop/.ssh \
    && chown -R hadoop:hadoop /home/hadoop /data

RUN printf 'PasswordAuthentication no\nPubkeyAuthentication yes\nAllowUsers hadoop\n' \
    > /etc/ssh/sshd_config.d/datamart.conf

RUN hadoop version

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D", "-e"]

