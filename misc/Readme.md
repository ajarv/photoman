
```bash
for xi in `find /mnt/5tb/Photovault/vault/ORIGN/2010/11 -type f` ; 
do 
    echo $(sha256sum $xi) $xi>> /tmp/zilla.txt ; 
done
```

```sh
cd /mnt/ssd/raw; mkdir -p x; cd x;
for x in `ls ../PhotosG-*zip` ;  
do 
    echo $x; 
    unzip $x 
    mc mv -r PhotosG libra/images
    sleep 30
done


```