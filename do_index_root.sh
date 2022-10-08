#!/bin/bash

while getopts 'i:o:' OPTION; do
#while getopts 'io:' OPTION; do
  case "$OPTION" in
    i)
      rawin=${OPTARG}
      ;;

    o)
      vault=${OPTARG}
      ;;
    ?)
      echo "script usage: $(basename $0) -i [inputdir] -o [output dir]" >&2
      exit 1
      ;;
  esac
done
shift "$(($OPTIND -1))"
set -x
projectspace=$(pwd)
vault=${vault:-/mnt/5tb/PhotoVault/vault}

docker run  -t \
        -u root \
        -v ${vault}:/p/out \
        -v ${projectspace}:/work \
        photoman python  /work/src/photo_manage.py --vault /p/out


docker run  -t  --rm \
        -u root \
        -v  ${vault}:/vault \
        -v ${projectspace}:/work \
        photoman python  /work/src/photo_listings.py /vault/ORIGN

docker run  -t  --rm \
        -u root \
        -v  ${vault}:/vault \
        -v ${projectspace}:/work \
        photoman python  /work/src/photo_listings.py /vault/S2000

set +x
