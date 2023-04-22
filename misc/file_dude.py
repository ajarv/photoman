import re
import os
import shutil
import sys
DATEPAT_01 = re.compile(
    ".*?[\w]{32}-(?P<file_name>(?P<date_y>(20[0-2][0-9])).*?(?P<date_m>([0-1][0-9])).*?(?P<date_d>([0-3][0-9])).*mp4)",
    re.IGNORECASE)


def process_file(f, base_path='/mnt/5tb/Photovault/vault/ORIGN'):
    a,b = os.path.split(f)
    m = DATEPAT_01.match(b)
    if not m:
        print (f"No Match {b}")
        return
    gd = m.groupdict()
    dest_f = f"{base_path}/{gd['date_y']}/{gd['date_m']}/{gd['date_d']}/{gd['file_name']}"
    if os.path.exists(dest_f):
        print(f"Dest file already exists: {dest_f}")
        return

    shutil.move(f,dest_f)
    print (f"Move {f} - {os.path.exists(dest_f)}")

def process_dir(d):
    for root, dirs, files in os.walk(d, topdown=False):
        print(root,dirs,files)
    pass

def m1():
    f = '/mnt/5tb/Photovault/vault/ORIGN/9999/00/00/ff33f2d770ff3a62e51e976f8e20f7a9-20210909_191158.mp4'
    m = DATEPAT_01.match(f)
    print (m and m.groupdict())
    scan_dir = '/mnt/5tb/Photovault/vault/ORIGN/9999/00/00'
    for f in os.listdir(scan_dir):
        process_file(f"{scan_dir}/{f}")
if __name__ == "__main__":
    process_dir(sys.argv[1])
    pass

