#!/bin/bash

i=0

# replace the Immich path to the script path
# local immich path
find="/usr/src/app/upload/"

# local script path to immich files
replace="mnt/pond/media/Photos/Immich/"

# path to untracked.txt exported from immich repair page
untracked="/home/nuthanael/Documents/untracked.txt"

# path to which files should be moved
destination="/mnt/pond/media/Photos/for review/"

IFS=$'\n'                         ## split only on newlines
for line in $(cat "$untracked")
do
    #  --dry-run
    localPath="${line//$find//$replace}"
    #echo $localPath
    rsync -axHAWXS --remove-source-files --relative --quiet $localPath $destination
    printf 'count: %s ' $i
    printf '%s\n' $localPath
    let ++i                       ## increment counter
done
unset IFS                         ## reset IFS to default
printf 'total: %s lines\n' $i
