'''
Created on Dec 29, 2011

@author: AVashist
'''

import os
import time
import shutil
from os.path import join
import argparse
import logging
import collections
import i_util

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.WARN)

def timeit_w_args_n_r(method):
    def timed(*args, **kw):
        ts = time.time()
        #         print 'Begin -- %r (%s) ' % \
        #               (method.__name__, str(args))
        try:
            result = method(*args, **kw)
            te = time.time()
            logging.info( '%r (%s) -> %r  ,%2.2f sec , OK' % \
                  (method.__name__, str(args), result, te - ts))
        except:
            result = None
            te = time.time()
            logging.exception( '%r (%s) -> %r  ,%2.2f sec , FAIL' % \
                  (method.__name__, str(args), result, te - ts))
        return result
    return timed

def orderFileList(file_paths):
    tree = {}
    for file_path in file_paths:
        _y,_m,_d  = time.localtime(os.path.getmtime(file_path))[0:3]
        yd = tree.get(_y,{}) ; tree[_y] = yd
        md = tree.get(_m,{}) ; tree[_m] = md
        dd = tree.get(_d,[]) ; tree[_d] = dd
        dd.append(file_path)

def arrange_files_by_date(source,destination,dry_run=False,keep=False):
    print("arrange_files_by_date ", source, destination, dry_run,keep)
    # existing_dest_file_set = build_file_set(destination)
    for root, dirs, files in os.walk(source):
        print ("Working on ",root)
        files = [
            file for file in files
            if i_util.JPGPAT.match(file) or i_util.MOVPAT.match(file)
        ]
        #-- Date Groups
        file_paths = [join(root, name) for name in files]
        date_groups = collections.defaultdict(list)
        for file_path in file_paths:
            _date = i_util.get_image_creation_date(file_path)
            date_groups[_date].append(file_path)
        for date_Y_M_D,file_list in date_groups.items():
            send_to_date_bins(destination,date_Y_M_D,file_list,dry_run=dry_run,keep=keep)

        if not dry_run and not keep:
            try:
                os.rmdir(root)
                print ("Success   Remove ",root)
            except:
                print ("Failed to Remove ",root)
                pass

def send_to_date_bins(destination,timetakenstr,file_list,dry_run=False,keep=False):

    for sfile in file_list:
        _dest_folder = os.path.join(destination,'ORIGN',*timetakenstr.split('-'))

        file_name = os.path.split(sfile)[-1]
        dfile = os.path.join(_dest_folder,file_name)

        ddir = os.path.dirname(dfile)
        if not os.path.exists(ddir):
            os.makedirs(ddir)

        if os.path.exists(dfile) :
            sz_dest ,sz_src = os.path.getsize(dfile),os.path.getsize(sfile)
            if sz_dest >= sz_src:
                print (f"{timetakenstr}: KEEPING DEST {dfile} [{sz_dest}] >= [{sz_src}] {sfile}")
                if not dry_run:
                    if not keep:
                        try:
                            os.remove(sfile)
                        except:
                            print(f"Failed to remove {sfile}")
            else:
                print (f"{timetakenstr}: UPDATING DEST {dfile} [{sz_dest}] < [{sz_src}] {sfile}")
                dtemp = dfile+"_"
                if not dry_run:
                    shutil.move(dfile,dtemp)
                    if not keep:
                        os.remove(dtemp)
                    shutil.move(sfile,dfile)
        else:
            print (f"{timetakenstr}: CREATING {dfile} <- {sfile}")
            if not dry_run:
                try:
                    shutil.move(sfile, dfile)
                    # utime = time.mktime( [int(t) for t in timetakenstr.split('-')] + [0] * 6)
                except:
                    logging.exception("xxxx")
                    print(f"Failed to move {sfile} -> {dfile}")


def do_copy_parrot(s,d):
    dir_name, _ = os.path.split(d)
    os.makedirs(dir_name,exist_ok=True)
    try:
        shutil.copy(s,d)
    except:
        print(f"Trying brute force copy {s} -> {d}")
        with open(s, 'rb') as f:
            data = f.read()
        with open(s, 'wb') as f:
            f.write(data)
    os.remove(s)

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='Index Photos into a folder structure')
    parser.add_argument('--input-folder', type=str, required=False,
                        default='sandbox',
                        help='Folder Path to Scan')
    parser.add_argument('--output-folder', type=str, required=False,
                        default='vault',
                        help='Destination path for photos')
    parser.add_argument('--dry_run',
                        default=False,
                        help='Dry Run',
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--keep',
                        default=False,
                        help='Keep the input files',
                        action=argparse.BooleanOptionalAction)

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()
    arrange_files_by_date(args.input_folder,args.output_folder,dry_run= args.dry_run,keep=args.keep)
