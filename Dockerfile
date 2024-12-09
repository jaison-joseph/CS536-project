FROM opennetworking/mn-stratum:20.12

# Update sources and install both iperf3 and python3
RUN echo "deb http://archive.debian.org/debian stretch main" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list && \
    echo "Acquire::Check-Valid-Until \"false\";" > /etc/apt/apt.conf.d/100debconf && \
    apt-get -o Acquire::AllowInsecureRepositories=true update && \
    apt-get --allow-unauthenticated install -y \
    python3 \
    python3-pip \
    d-itg \
    openvswitch-switch \
    openvswitch-common \
    kmod

# Create OVS directories and initialize
RUN mkdir -p /var/run/openvswitch && \
    mkdir -p /var/log/openvswitch && \
    mkdir -p /etc/openvswitch

# Create a more robust startup script
RUN echo '#!/bin/bash\n\
if [ ! -f /etc/openvswitch/conf.db ]; then\n\
    ovsdb-tool create /etc/openvswitch/conf.db /usr/share/openvswitch/vswitch.ovsschema\n\
fi\n\
ovsdb-server --remote=punix:/var/run/openvswitch/db.sock \
    --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
    --pidfile --detach\n\
ovs-vsctl --no-wait init\n\
ovs-vswitchd --pidfile --detach\n\
ovs-vsctl set-manager ptcp:6640\n\
mn "$@"\n' > /entrypoint.sh && \
chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]