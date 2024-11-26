FROM opennetworking/mn-stratum:20.12

# Update sources and install both iperf3 and python3
RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list && \
    echo "Acquire::Check-Valid-Until \"false\";" > /etc/apt/apt.conf.d/100debconf && \
    apt-get -o Acquire::AllowInsecureRepositories=true update && \
    apt-get --allow-unauthenticated install -y \
    iperf3 \
    python3 \
    python3-pip \
    d-itg 