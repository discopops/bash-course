#!/usr/bin/env bash

name=$1

case "$name" in
    d*|D*)  # Starts with d or D
        echo "Name starts with D: $name"
        ;;
    *son)  # Ends with 'son'
        echo "Name ends with 'son': $name"
        ;;
    [Jj]ohn)  # John or john
        echo "Hello, John!"
        ;;
    *)
        echo "Hello, $name!"
        ;;
esac
