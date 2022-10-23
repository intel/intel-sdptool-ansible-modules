#!/usr/bin/env bash

cwd="$(readlink -f "$(dirname "$0")")"

cd /tmp/
pip install pexpect
rm -rf /tmp/devel.tar.gz
rm -rf /tmp/ansible-devel

echo "Downloading Ansible devel package"
wget install https://github.com/ansible/ansible/archive/devel.tar.gz 2>/dev/null

echo "Extracting Ansible devel package"
tar -xvf devel.tar.gz > /dev/null 2>&1

source /tmp/ansible-devel/hacking/env-setup

cd "$cwd"

echo "Running Sanity Tests"
if ansible-test sanity --docker default -v --color; then
    echo "Sanity Test Completed"
else
    echo "Sanity Test Failed"
    exit 1
fi

echo "Running Unit Tests"
if ansible-test units --docker default -v --color; then
    echo "Unit Test Completed"
else
    echo "Unit Test Failed"
    exit 1
fi

echo "Running Integration Tests"
if ansible-test integration -v --color; then
    echo "Integration Test Completed"
else
    echo "Integration Test Failed"
    exit 1
fi
