from PIL import Image
import sys
import glob
import os
import cv2
import threading

class myThread (threading.Thread):
    def __init__(self, threadID, name ,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.files = name
        self.counter = counter
    def run(self):
        print("Starting "+ self.name)
        blend_two_images(self.counter,self.counter,self.counter)
        print("Exiting " + self.name)

def get_filename(data):
    filenames=[]
    if data == 'colorimage':
        search_files = os.path.join('./','*_image.png')
        filenames = glob.glob(search_files)
    else:
        if data == 'labelimage':
            search_files = os.path.join('./','*_prediction.png')
            filenames = glob.glob(search_files)
        else:
            search_files = os.path.join('./','*_blendimg.png')
            filenames = glob.glob(search_files)

    return sorted(filenames)



def blend_two_images(number,colorimage,labelimage):
    for i in range(number):
        img_add = colorimage[i]
        img1 = Image.open(img_add)
        img1 = img1.convert('RGBA')
        label_add = labelimage[i]
        img2 = Image.open(label_add)
        img2 = img2.convert('RGBA')
        img = Image.blend(img1, img2, 0.8)
        #img.show()
        img.save('./'+ "%06d"%(i) +'_blendimg.png')
        sys.stdout.write('\r>> Converting image %d/%d' % (int(i), number))
        sys.stdout.flush()
    print '\r'
    return

def imagetovideo(blendimage):
    path = './video.avi'
    fps = 30
    imagesize = (3384,2710)
    #fourcc = cv2.cv.CV_FOURCC('M','J','P','G')
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    videoWriter = cv2.VideoWriter(path,fourcc,fps,imagesize)


    for i in range(len(blendimage)):
        frame = cv2.imread(blendimage[i])
        videoWriter.write(frame)
        sys.stdout.write('\r>> Converting image %d/%d' % (int(i), len(blendimage)))
        sys.stdout.flush()

    videoWriter.release()
    print('finished')


if __name__ == '__main__':
    # colorimage = get_filename('colorimage')
    # labelimage = get_filename('labelimage')
    # blend_two_images(len(colorimage),colorimage,labelimage)
    blendimage = get_filename('blendimage')
    imagetovideo(blendimage)



