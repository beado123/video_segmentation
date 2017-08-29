from PIL import Image
from PIL import ImageDraw
import os,sys,json,glob,pdb,cv2,numpy as np

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

    im = Image.open('%s' % (jpg))
    mask = Image.new('L', im.size) # new image, the output
    polgs = json.load(open('%s' % (json_file)))
    output = np.array(mask)
    index = 1
    box = {}
    new_polgs = sorted(polgs, key = lambda x: x['feature'][2])

    for i in range(len(polgs)):
        polygon = new_polgs[i]
        shape = list(map(tuple, polygon['polygon']))  #all contour coords of this object
        draw = ImageDraw.Draw(mask)

        curid = polygon['feature'][2]
        if curid in coloridxmap:
            fillcolor = coloridxmap[curid]
        else:
            coloridxmap[curid] = colors[i]
            fillcolor = colors[i]
        draw.polygon(shape, fill = fillcolor)
        #mask.save('annotations/00' + jpg[15:18]+'.jpg')

        tmp = np.array(mask)
        print(np.unique(tmp))
        value = 0
        for j in range(1,i+2):
                if  (np.unique(tmp))[j] in box :
                        pass
                else:
                        box[(np.unique(tmp))[j]] = index
                        value = (np.unique(tmp))[j]
                        output[tmp==value] = index
                        #print("index:%d"%(index))
                        index = index + 1
       
        print(np.unique(output))
    
    mask = Image.fromarray(output.astype('uint8'))
    mask.putpalette(PALETTE)
    print("Successfully generated png from %s"%(jpg))
    
    name = 'annotations/00' + jpg[15:18]+'.png'
    if not os.path.exists('annotations'):
        os.makedirs('annotations', 755)
    mask.save(name)
    return

def read_frames(start, end, video_folder, dirent, writer_root):
    try:
        os.path.isdir(video_folder)
    except Exception as e: print(e)
    
    # have to be in the video folder 
    os.chdir('../' + video_folder)
    vid = cv2.VideoCapture('./' + dirent + '.mp4')  
    success, image = vid.read()
    print( 'Read a new frame: ', success)

    count = start
    success = True
    while success:
        success,image = vid.read()
        print ('Read a new frame: ', success)
        os.chdir('..')
        cv2.imwrite(os.path.join(writer_root, "%05d.jpg"%count), image)
        os.chdir(video_folder)
        if count == end:
            break
        count += 1
    os.chdir('../'+dirent)


if __name__ == '__main__': 

    os.chdir('..')
    if not os.path.exists('./output_folder'):
            os.makedirs(os.path.join('./output_folder'))
    dest_folder = os.path.join(os.getcwd(), '/output_folder/')
    os.chdir(os.getcwd())

    for dirent in os.listdir('./'):
        if not dirent[0:3] == 'vid':
            continue

        # create output folder in 'output_folder'
        curr_dest = os.path.join(dest_folder, dirent)
        if not os.path.exists(curr_dest)
            os.makedirs(curr_dest)

        # navigate to video file
        os.chdir('./'+dirent)
        print("In folder %s"%(dirent))

        # create output folders
        if not os.path.exists('./annotations'):
            os.makedirs(os.path.join('./','annotations'))
        if not os.path.exists('./images'):
            os.makedirs(os.path.join('./','images'))

        # create json and jpg input lists
        json_files = []
        jpg_files = []
        for file in glob.glob("*.json"):
            json_files.append(file)
        for file in glob.glob("*.jpg"):
            jpg_files.append(file)

        sorted_json = sorted(json_files, key = lambda x: str(x.split('_')[3]))
        sorted_jpg = sorted(jpg_files, key = lambda x: str(x.split('_')[3]))

        # read all frames and output to images folder
        start = int(sorted_json[0][15:18])
        end = int(sorted_json[len(sorted_json)-1][15:18])
        video_folder = sys.argv[1]
        read_frames(start, end, video_folder, dirent, os.path.join(dirent+'/images'))

        coloridxmap = {}      #may have bugs
        for i in range(0,len(json_files)):
            try:
                read_image(sorted_json[i], sorted_jpg[i], coloridxmap)
                pass
            except FileNotFoundError:
                pass
            except UnicodeDecodeError:
                print('UnicodeDecode error occurs in '+ dirent +'/'+ sorted_json[i])
                pass
            except json.decoder.JSONDecodeError:
                print('jsonDecode error occurs in '+ dirent +'/'+ sorted_json[i])
                pass
        os.chdir('..')
    
