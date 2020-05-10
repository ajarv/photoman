#!/bin/bash

projectspace=$(pwd)
vault=/mnt/ssd/avashist/PhotoVault/vault
rawin=/mnt/ssd/avashist/rawin



docker run  -t  --rm \
-v  ${vault}:/vault \
-v ${projectspace}:/work \
photoman python  /work/src/photo_listings.py /vault/ORIGN

docker run  -t  --rm \
-v  ${vault}:/vault \
-v ${projectspace}:/work \
photoman python  /work/src/photo_listings.py /vault/S2000

docker run  -t  --rm \
-v  ${vault}:/vault \
-v ${projectspace}:/work \
photoman python  /work/src/photo_listings.py /vault/S0300
