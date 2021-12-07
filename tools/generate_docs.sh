#!/bin/bash

# remove
rm -rf docs/*

# create
for filename in $(find . -type f -name "*.py" -print); do
    # file data
    f="$(basename -- $filename .py)"
    parentdir="$(dirname "$filename")"

    # docs save paths and names
    folder="docs/${parentdir:1}"
    file="$folder/$f"

    if [ "$f" != "__init__" ]; then
        echo "Processing: $filename"
        mkdir -p $folder
        python3 -m pdoc $filename > $file.md
    fi
done
