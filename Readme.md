## Python project for indexing photos

Let's say you take a lot of pictures. Over the years as your library grows and you have photos spread around 
multiple computers and folders. 

This project helps you consolidate and index your photos at one location using the date of your photos to index them

e.g. if you have photos spread around these folders 

```
mypictures/DCIM/23332XX/DSC_9392.JPG
mypictures/one/DSC_4233.JPG 
abc/232/DSC_6344.JPG
```

This project will help you get them in the order
```
<DESTINATION FOLDER>/ORIGN/2019/03/01/DSC_9392.JPG
<DESTINATION FOLDER>/ORIGN/2019/02/13/DSC_4233.JPG
<DESTINATION FOLDER>/ORIGN/2017/03/01/DSC_6344.JPG
```


1. Create Docker image
```bash
git clone https://github.com/ajarv/photoman.git ~/workspace/photoman
cd ~/workspace/photoman
docker build -t photoman .
```


2. Make input and output directories

```bash
mkdir /tmp/rawin
mkdir ~/PhotoVault
```
Copy/Dump all your photo folders ...  to  `/tmp/rawin`

3. Run docker container

```bash
projectspace=$(pwd)
vault=/mnt/ssd/avashist/PhotoVault/vault
rawin=/mnt/ssd/avashist/rawin

docker run  -t  \
-v ${rawin}:/p/in \
-v ${vault}:/p/out \
-v ${projectspace}:/work \
photoman python  /work/src/photo_manage.py --inputFolder /p/in --outputFolder /p/out 

```


4. Create JSON Index of files

```bash
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
photoman python /work/src/photo_listings.py /vault/S0300 



docker run  -t  --rm \
-v  ${vault}:/vault \
-v ${projectspace}:/work \
photoman python  /work/src/photo_index_01.py /vault 


```



```bash

./do_index.sh -i /mnt/ssd/raw  -o /mnt/ssd/avashist/PhotoVault/vault


./do_arrange.sh -s /mnt/ssd/raw  -d /mnt/ssd/avashist/PhotoVault/vault


## Create listings
docker run  -t  --rm \
        -u 1000 \
        -v  /mnt/ssd/avashist/PhotoVault/vault:/vault \
        -v /home/ajar/workspace/photo-manager:/work \
        photoman python  /work/src/photo_listings.py /vault/S2000

```

