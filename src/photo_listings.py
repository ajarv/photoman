import os
import re
import json
import sys
JPGPAT = re.compile(".*[.](jpg)$", re.IGNORECASE)

def folder_listing_json(folder):
    _ofiles = []
    _folder = os.path.abspath(folder)
    _fl = len (_folder)
    for root, dirs, files in os.walk(folder):
        files = [file for file in files if JPGPAT.match(file)]
        file_paths = [ os.path.abspath(os.path.join(root, name))[_fl:].replace('\\', '/') for name in files]
        _ofiles += file_paths;
    _d, _fn = os.path.split(folder)
    _json_file = os.path.join(_d, "{}__list.json".format(_fn))
    _ofiles.sort()
    _o = dict(total=len(_ofiles), files=_ofiles)
    with open(_json_file, 'w') as f:
        json.dump(_o, f, indent=2)

if __name__ == '__main__':
    folder_listing_json(sys.argv[1])
