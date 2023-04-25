#!/bin/bash
# convert tsv to csv
sed 's/\t/,/g' "$1" > "$2"