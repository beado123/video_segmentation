from PIL import Image
from PIL import ImageDraw
import os,sys
import json
import pdb
import numpy as np
import glob

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

def read_image(json_file, jpg, coloridxmap={}):
    print("%s" % (jpg))
    im = Image.open('%s' % (jpg))
    mask_temp = Image.new('L', im.size) #temp image used to extract index
    mask = Image.new('L', im.size) # new image, the output
    print("%s" % (json_file))
    polgs = json.load(open('%s' % (json_file)))
    output = np.array(mask)
    index = 1
    box = {}
    #pdb.set_trace()
    new_polgs = sorted(polgs, key = lambda x: x['feature'][3])
    for i in range(len(polgs)):
        polygon = new_polgs[i]
        shape = list(map(tuple, polygon['polygon']))  #all contour coords of this object
        draw = ImageDraw.Draw(mask)
        draw_temp = ImageDraw.Draw(mask_temp)  	# 'draw' is the media to draw on 'mask'

        curid = polygon['feature'][3]
        if curid in coloridxmap:
            fillcolor = coloridxmap[curid]
        else:
            coloridxmap[curid] = colors[i]
            fillcolor = colors[i]
        draw_temp.polygon(shape, fill = fillcolor)

        tmp = np.array(mask_temp)
        #print(np.unique(tmp))
        for j in range(1,i+2):
                if (np.unique(tmp))[j] in box:
                        pass
                else:
                        box[(np.unique(tmp))[j]] = index
                        value = (np.unique(tmp))[j]
                        output[tmp==value] = index
                        index = index + 1
       
        #print(np.unique(output))
    
    mask = Image.fromarray(output.astype('uint8'))
    mask.putpalette(PALETTE)
    
    name = 'annotations/00' + jpg[15:18]+'.png'
    if not os.path.exists('annotations'):
        os.makedirs('annotations', 755)
    mask.save(name)
    return


if __name__ == '__main__': 
    #pdb.set_trace()
    for dirent in os.listdir('./'):
        if not dirent[0:3] == 'vid':
            continue
        print("In folder %s"%(dirent))

        json_files = []
        jpg_files = []
        os.chdir('./'+dirent)
        for file in glob.glob("*.json"):
            json_files.append(file)
        for file in glob.glob("*.jpg"):
            jpg_files.append(file)
        #pdb.set_trace()

        sorted_json = sorted(json_files, key = lambda x: str(x.split('_')[3]))
        #print(sorted_json)
        sorted_jpg = sorted(jpg_files, key = lambda x: str(x.split('_')[3]))
        #print(sorted_jpg)
        coloridxmap = {}      #may have bugs
        for i in range(0,len(json_files)):
            try:
                print("%s/%s"%(dirent,sorted_json[i]))
                read_image(sorted_json[i], sorted_jpg[i], coloridxmap)
            except FileNotFoundError:
                pass
            except UnicodeDecodeError:
                print('UnicodeDecode error occurs in '+ dirent +'/'+filename)
                pass
            except json.decoder.JSONDecodeError:
                print('jsonDecode error occurs in '+ dirent +'/'+filename)
                pass
        os.chdir('..')
    
