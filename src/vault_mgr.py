from rethinkdb import RethinkDB
import hashlib
import logging
import shutil
import os

logger = logging.getLogger(__file__)

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096*4), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

class Vault:
    def __init__(self,base_dir):
        self.base_dir = base_dir
        self.r = r = RethinkDB()
        self.conn = r.connect(host='localhost',
                 port=28015,
                 db='test')
        pass
    def add_checksum(self,file_path,checksum):
        self.r.table('vault').insert({'id':checksum,'p':file_path}).run(self.conn)
        logger.info(f"Added {file_path} -> {checksum}")

    def findByPath(self, d_path):
        v = self.r.db('test').table('vault').filter({
            'p': d_path
        }).run(self.conn)
        v = list(v)
        return v[0] if v else None

    def findByChecksum(self, checksum):
        v = self.r.db('test').table('vault').filter({
            'id': checksum
        }).run(self.conn)
        v = list(v)
        return v[0] if v else None
        pass

    def add_file(self,src_path,dest_path):
        logger.info(f"working on {src_path}")
        if not dest_path.startswith(f"{self.base_dir}/ORIGN/"):
            raise Exception(f"Destination path must begin with {self.base_dir}/ORIGN/")
        item = self.findByPath(d_path=dest_path)
        if  item:
            logger.info(
                f"File already catalogued - {item['id']} -> {dest_path}")
            return False

        checksum = md5(src_path)
        item = self.findByChecksum(checksum=checksum)
        if  item:
            logger.info(
                f"File {src_path} already catalogued - {item['id']} -> {dest_path}")
            return False
        if dest_path != src_path:
            tgtdir ,f= os.path.split(dest_path)
            os.makedirs(tgtdir, mode=511, exist_ok=True)
            shutil.copyfile(src_path,dest_path)
        self.add_checksum(dest_path,checksum)


    def resync(self):
        for root, dirs, files in os.walk(f"{self.base_dir}/ORIGN/"):
            for name in files:
                src_path = os.path.join(root, name)
                self.add_file(src_path,src_path)



if  __name__ == '__main__' :
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    vault = Vault("/mnt/5tb/PhotoVault/vault")
    vault.resync()
