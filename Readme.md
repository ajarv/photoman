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

docker run  -t  \
-v /tmp/rawin:/p/in \
-v ~/PhotoVault:/p/out \
-v /home/ajar/workspace/photo-manage:/work \
photoman python  /work/src/photo_manage.py --inputFolder /p/in --outputFolder /p/out 