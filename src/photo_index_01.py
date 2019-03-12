import os
import re
import json
import sys
JPGPAT = re.compile(".*[.](jpg)$", re.IGNORECASE)

htmlcode="""<!doctype html>
<html>
    <head>
        <title>{title}</title>
        <link type="text/css" rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/galleria/1.5.7/themes/classic/galleria.classic.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/galleria/1.5.7/galleria.min.js"></script>
        <style>
            .galleria {{
                width:100%;
                height:900px
            }}
        </style>
    </head>
    <body>
        <h2>{title}</h2>
        <div class="galleria">
            {images}
        </div>
        <script>
	(function() {{
            Galleria.loadTheme('https://cdnjs.cloudflare.com/ajax/libs/galleria/1.5.7/themes/classic/galleria.classic.min.js');
            Galleria.run('.galleria', {{
              height: parseInt($('.galleria').css('height')),
              wait: true
             }});
        }}());
        </script>
    </body>
</html>"""


itempl="""<a href="{s2000}/{file}">
        <img src="{s0300}/{file}"
            data-big="{s2000}/{file}"
            data-title="{file}"
            />
    </a>"""

def doFolder(base,root,files):
    files = [file for file in files if JPGPAT.match(file)]
    if not files:
        return
    xbase = root.split(base)[-1]
    # print ('xbase',xbase)
    ddir = {'s2000':xbase,'s0300':xbase.replace('S2000','S0300'),};
    images = '\n'.join([ itempl.format(file=file,**ddir) for file in files])
    title = root
    xhtml = htmlcode.format(images=images,title=xbase)
    print ("Folder",title,base)
    with open(os.path.join(root,'index.html'),'w') as f:
        f.write(xhtml)


def folder_listing_json(base):
    _ofiles = []
    _folder = os.path.abspath(base)
    _fl = len (_folder)
    for root, dirs, files in os.walk(base+'/S2000'):
        doFolder(base,root,files)

if __name__ == '__main__':
    folder_listing_json(sys.argv[1])
