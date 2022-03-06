import shutil
import sys
import time
import os
import logging
import i_util
LOGGER = logging.getLogger(__file__)

existing_dirs = set()
def ensure_dir(t):
    if t in existing_dirs: return
    os.makedirs(t,exist_ok=True)
    existing_dirs.add(t)

def should_copy(src_file,tgt_file):
    if not os.path.exists(tgt_file):
        return True
    sz_dest ,sz_src = os.path.getsize(tgt_file),os.path.getsize(src_file)
    rval = sz_dest < sz_src
    LOGGER.info(f"should_copy({src_file},{tgt_file}) -> {rval}")
    return rval

def move_file(src_file, tgt_base):
    mtime = os.path.getmtime(src_file)
    if i_util.IMGPAT.match(src_file):
        stamp = i_util.get_image_creation_date(src_file).replace('-','/')
    else:
        stamp = time.strftime('%Y/%m/%d', time.localtime(mtime))
    fname = os.path.split(src_file)[-1]
    tgt_dir = os.path.join(tgt_base,*(stamp.split('/')))

    tgt_file =  os.path.join(tgt_dir,fname)
    if not should_copy(src_file,tgt_file):
        return False
    LOGGER.info(f"ensure_dir({tgt_dir})")
    ensure_dir(tgt_dir)
    LOGGER.info(f"shutil.copy({src_file},{tgt_file})")
    shutil.copy(src_file,tgt_file)
    return True

def arrange(src_dir,dest_base="/mnt/5tb/Photovault/vault/ORIGN"):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_file = os.path.join(root,file)
            if move_file(src_file,dest_base):
                LOGGER.info(f"move_file({src_file},{dest_base}) - > YES")
            else:
                LOGGER.info(f"move_file({src_file},{dest_base}) - > NO")

    pass

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    # arrange(sys.argv[1])
    arrange('/mnt/ssd/raw')
