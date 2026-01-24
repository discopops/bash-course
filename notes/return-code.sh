#!/usr/bin/env bash

check_file() {
    if [[ -f $1 ]]; then
        echo "File exists: $1"
        return 0  # Success
    else
        echo "File not found: $1"
        return 1  # Failure
    fi
}

check_file "hello.sh"
echo "Return code: $?"

check_file "nonexistent.txt"
echo "Return code: $?"
