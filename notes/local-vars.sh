#!/usr/bin/env bash

greet() {
    local name=$1  # local keeps variable inside function
    echo "Hello, $name!"
}

greet "Alice"
greet "Bob"
