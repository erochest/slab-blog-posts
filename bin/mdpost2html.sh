#!/bin/bash

SRC="$1"
DEST=${SRC%.md}.html

pandoc --smart -f markdown -t html5 $SRC | ./fix_code.py > $DEST
cat $DEST | pbcopy
open $DEST
