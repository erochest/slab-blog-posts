#!/bin/sh

pandoc --smart -f markdown -t html5 timr.md | ./fix_code.py > timr.html
cat timr.html | pbcopy
open timr.html
