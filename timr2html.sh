#!/bin/sh

pandoc --smart -f markdown -t html5 timr.md > timr.html
cat timr.html | pbcopy
open timr.html
