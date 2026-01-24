#!/usr/bin/env bash

# Check if a file exists
if [[ -f "hello.sh" ]]; then
    echo "hello.sh is a file"
fi

# Check if a directory exists
if [[ -d "test-folder" ]]; then
    echo "test-folder is a directory"
fi
