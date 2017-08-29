from PIL import Image
from PIL import ImageDraw
import os,sys
import json
import pdb
import numpy as np
import glob
from operator import itemgetter
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return (int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))
PALETTE = [ '#000000', '#ec5f67', '#f99157', '#fac863',
'#99c794', '#62b3b2', '#6699cc', '#c594c5',
'#ab7967', '#ffffff', '#65737e', ]
PALETTE = [v for value in PALETTE for v in hex_to_rgb(value)]
ANTI_PALATTE = [0]*3 + [16]*30

colors = ['red','orange','blue','magenta'] 
MYCOLOR = '#ec5f61'
sorted_json = 'vid_seg_00115_f070.json'
sorted_jpg = 'vid_seg_00115_f070.jpg'

def read_image(json_file, jpg, coloridxmap={}):
    im = Image.open('%s' % (jpg))
    mask = Image.new('RGB', im.size) # new image, the output
    #mask.putpalette(PALETTE)
    polgs = json.load(open('%s' % (json_file)))
    #pdb.set_trace()
    new_polgs = sorted(polgs, key = lambda x: x['feature'][2])
    #new_polgs = sorted(polgs, key=itemgetter('feature'))
    for i in range(len(polgs)):
        polygon = new_polgs[i]
        #pdb.set_trace()
        shape = list(map(tuple, polygon['polygon']))  #all contour coords of this object
        draw = ImageDraw.Draw(mask)

        #if i==0:
            #for j in range(0, len(shape)):
                #draw.point((shape[j],shape[j]), fill=100)

        curid = polygon['feature'][2]
        if curid in coloridxmap:
            fillcolor = coloridxmap[curid]
        else:
            coloridxmap[curid] = colors[i]
            fillcolor = colors[i]
        draw.polygon(shape, fill = fillcolor)
        mask.show()
    print("Successfully generated png from %s"%(jpg))
    
    name =  'polygon.png'
    mask.save(name)
    return


if __name__ == '__main__': 
    #pdb.set_trace()
    coloridxmap = {}      #may have bugs
        
    try:
         #print("%s/%s"%(dirent,sorted_json[i]))
         read_image(sorted_json, sorted_jpg, coloridxmap)
    except FileNotFoundError:
         pass
    except UnicodeDecodeError:
         print('UnicodeDecode error occurs in '+ dirent +'/'+ sorted_json[i])
         pass
    except json.decoder.JSONDecodeError:
         print('jsonDecode error occurs in '+ dirent +'/'+ sorted_json[i])
         pass
    
