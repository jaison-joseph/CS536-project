#!/bin/bash

# Check if in the omnet container
if ! command -v omnetpp &> /dev/null; then
    echo "Error: OMNeT++ not found. Are you inside the OMNeT++ container?"
    exit 1
fi

# Get current directory for later output
CURRENT_DIR=$(pwd)

# Install git if not present
if ! command -v git &> /dev/null; then
    echo "Installing git..."
    apt-get update && apt-get install -y git
fi

# Clone and build INET
echo "Cloning INET..."
git clone https://github.com/inet-framework/inet.git
cd inet
git checkout -b v3.6.7 v3.6.7

echo "Building INET..."
. /root/omnetpp/bin/setenv
make makefiles
make 

echo "INET installation complete!"
echo "INET is installed at: $CURRENT_DIR/inet"