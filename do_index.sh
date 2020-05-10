#!/bin/bash

projectspace=$(pwd)
vault=/mnt/ssd/avashist/PhotoVault/vault
rawin=/mnt/ssd/avashist/rawin

docker run  -t  \
        -v ${rawin}:/p/in \
        -v ${vault}:/p/out \
        -v ${projectspace}:/work \
        photoman python  /work/src/photo_manage.py --inputFolder /p/in --outputFolder /p/out


docker run  -t  --rm \
-v  ${vault}:/vault \
-v ${projectspace}:/work \
photoman python  /work/src/photo_listings.py /vault/ORIGN
