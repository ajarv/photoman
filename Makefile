

WORKSPACE=$(shell pwd)
vault ?= /mnt/ssd/avashist/PhotoVault/vault
rawin ?= /mnt/ssd/avashist/rawin

build-worker-image:
	docker build  -t photoman ${WORKSPACE}

photo-arrange:
	docker run  --tty --rm  \
	-v ${rawin}:/p/in \
	-v ${vault}:/p/out \
	-v ${WORKSPACE}:/work \
	-w /work \
	photoman python  ./src/photo_manage.py --inputFolder /p/in --outputFolder /p/out 

photo-index:
	docker run  --tty --rm  \
	-v ${vault}:/vault \
	-v ${WORKSPACE}:/work \
	photoman python ./src/photo_listings.py /vault/S2000
