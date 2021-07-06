#!/usr/bin/env bash

echo "Removing Installed Collection"
rm -rf /root/.ansible/collections/ansible_collections/intel/sdptool

echo "Adding Intel(R) SDP Tool plugin to Collection"
cwd="$(readlink -f "$(dirname "$0")")"
mkdir -p /root/.ansible/collections/ansible_collections/intel

cp -r "$cwd" /root/.ansible/collections/ansible_collections/intel/sdptool
