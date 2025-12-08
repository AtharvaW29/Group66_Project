#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./efficient.sh <input_file_path> <output_file_path>" >&2
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: Input file '$1' not found" >&2
    exit 1
fi


if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed or not in PATH" >&2
    exit 1
fi


python3 efficient.py "$1" "$2"

EXIT_CODE=$?

exit $EXIT_CODE