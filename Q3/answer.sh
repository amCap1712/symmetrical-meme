#!/usr/bin/env bash

set -e

curl -L -s http://amfiindia.com/spages/NAVAll.txt | cut -s -d ';' -f 4,5 | cat > schemes.tsv

# whether the data should be stored in TSV or JSON depends on the end consumers.
# tsv is more human readable and very simple to explore as it can be directly opened in excel.
# if the data is to be served over an API, JSON might be more a suitable data format.
