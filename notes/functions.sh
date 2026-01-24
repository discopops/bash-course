#!/usr/bin/env bash

my_function() {
    echo "Hello from my function!"
    echo "First argument: $1"
}

# Call the function
my_function "test"
my_function "another test"
