import imageio
import sys
import numpy as np
import visvis as vv
from skimage import color, measure, morphology
from skimage.feature import peak_local_max
from scipy import ndimage
import cv2

def readimg(src):
    return imageio.imread(src)

def videotoframes(src):
    vid = imageio.get_reader(src)
    for frame in vid:
        frames.append(frame)
    return frames

def tohsv(frame):
    return color.rgb2hsv(frame)

def togrey(frame):
    return color.rgb2gray(frame)

def mask(frame):
    return np.zeros(frame.shape, np.float)

def gaussblur(frame, sigma=3):
    frame = ndimage.gaussian_filter(frame, sigma)
    return ndimage.gaussian_filter(frame, 1)

def computebg(frames, mask):
    N = len(frames)
    for i in range(N):
        frame = frames.get_data(i)
        framearray = np.array(frame, dtype=np.float)
        mask = mask+framearray/N
    return np.array(np.round(mask), dtype=np.uint8)

def findcontours(frame, level=3):
    binary_img = frame > 0.5
    open_img = ndimage.binary_opening(binary_img)
    close_img = ndimage.binary_closing(open_img)
    contours = measure.find_contours(frame, level)
    #for n, contour in enumerate(contours):

def watershed(frame):
    distance = ndimage.distance_transform_edt(frame)
    local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)), labels=frame)
    markers = measure.label(local_maxi)
    labels_ws = morphology.watershed(-distance, markers, mask=frame)
    return labels_ws

def removesmall(frame, minsize=200):
    return morphology.remove_small_objects(frame, minsize,  connectivity=2)

def showimg(img):
    cv2.imshow('frame',img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return




video = sys.argv[1]
frames = videotoframes(video)
#cap = cv2.VideoCapture(video)


while True:
    ret, frame = cap.read()
    frame = togrey(frame)
    mask = mask(frame)
    blur = gaussblur(frame)
    #background = computebg(frame, mask)
    label = watershed(blur)
    cv2.imshow('frame',label)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
