#!/bin/bash
# get first argument, get config json file, run lexmapr, replace tabs into comma
# to have csv output format on stdout
FILE_NAME=$1
lexmapr "$FILE_NAME" -c conf/lex_mapr.json