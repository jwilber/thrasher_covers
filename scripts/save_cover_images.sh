#!/bin/bash

# download Thrasher magazine covers and save them to data/cover_images/

set -o errexit
set -o pipefail

{
    read
    while IFS=, read -r month year cover
    do 
    	echo "$cover"
        wget "$cover" -P data/cover_images

    done
} < ../data/thrasher_covers.csv
