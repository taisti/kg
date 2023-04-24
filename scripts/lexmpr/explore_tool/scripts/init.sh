#!/bin/bash

echo "Required python >= 3.7"
if ! test -f venv; then
	python3 -m venv venv
fi
source venv/bin/activate

if test -d LexMapr; then
	rm -rf LexMapr
fi
git clone https://github.com/taisti/LexMapr.git
pip3 install ./LexMapr