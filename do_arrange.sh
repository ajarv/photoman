#!/bin/bash

# ------ Variables
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"

  case $key in
    -s)
      SOURCE_DIR="$2"
      shift # past argument
      shift # past value
      ;;
    -d)
      DEST_DIR="$2"
      shift # past argument
      shift # past value
      ;;
    *)    # unknown option
      POSITIONAL+=("$1") # save it in an array for later
      shift # past argument
      ;;
  esac
done

if [ -z "${SOURCE_DIR}" ] || [ -z "${DEST_DIR}" ] ; then
    echo "Usage: $0 -s [Source dir]  -d [destination dir]"
    exit 1
fi

set -x 
projectspace=$(pwd)
vault=${DEST_DIR}
rawin=${SOURCE_DIR}

docker run  --rm -t \
        -u root \
        -v ${rawin}:/p/in \
        -v ${vault}:/p/out \
        -v ${projectspace}:/work \
        photoman python /work/src/photo_arrange.py --inputFolder /p/in --outputFolder /p/out --dry-run


set +x
