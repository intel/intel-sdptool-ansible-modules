#!/usr/bin/env bash

cwd="$(readlink -f "$(dirname "$0")")"
parent_dir="$(dirname "$cwd")"

cd "$parent_dir"
virtualenv venv
source venv/bin/activate
pip install https://github.com/ansible/ansible/archive/devel.tar.gz --disable-pip-version-check
pip install pexpect

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
