#!/usr/bin/env bash

while getopts "n:a:v" opt; do
    case $opt in
        n) name=$OPTARG ;;
        a) age=$OPTARG ;;
        v) verbose=true ;;
        \?) echo "Invalid option: -$OPTARG" >&2; exit 1 ;;
    esac
done

echo "Name: ${name:-not set}"
echo "Age: ${age:-not set}"
echo "Verbose: ${verbose:-false}"
