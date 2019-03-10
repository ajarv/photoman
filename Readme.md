docker build -t photobabu .

mkdir -p /tmp/sbox
mkdir -p /tmp/vault

docker run  -v /tmp/sbox:/p/in -v /tmp/vault/:/p/out -t photobabu python /work/src/photo_manage.py --inputFolder /p/in --outputFolder /p/out


docker run  -t  -v /mnt/ssd/avashist/rawin:/p/in -v /mnt/ssd/avashist/PhotoVault/vault/:/p/out photobabu python /work/src/photo_manage.py --inputFolder /p/in --outputFolder /p/out --name photobabu