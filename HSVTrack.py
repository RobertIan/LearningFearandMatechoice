#!/usr/bin/env
import cv2, csv, os, re
import numpy as np
import argparse



def on_mouseblackbox(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        #print 'Start Mouse Position: ' + str(x) + ', ' + str(y)
        sbox = [x, y]
        blackbox.append(sbox)
    elif event == cv2.EVENT_LBUTTONUP:
        #print 'End Mouse Position: ' + str(x) + ', ' + str(y)
        ebox = [x, y]
        blackbox.append(ebox)

def on_mousewhitebox(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        #print 'Start Mouse Position: ' + str(x) + ', ' + str(y)
        sbox = [x, y]
        whitebox.append(sbox)
    elif event == cv2.EVENT_LBUTTONUP:
        #print 'End Mouse Position: ' + str(x) + ', ' + str(y)
        ebox = [x, y]
        whitebox.append(ebox)

def drawbox(boxpoints):
    (x1, y1) = boxpoints[-4]
    (x2, y2) = boxpoints[-3]
    (x3, y3) = boxpoints[-2]
    (x4, y4) = boxpoints[-1]
    lilbx = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    return lilbx, x1, x2, x3, x4

def convertToHSV(frame):
    height, width, channels = frame.shape
    blurred = cv2.blur(frame, (2, 2))
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = np.zeros((height, width, 3), np.uint8)
    mask[:, :] = hsv[:, :]
    return mask

def convertToHSVScoto(frame, blackbox, whitebox):
    height, width, channels = frame.shape
    blurred = cv2.blur(frame, (2, 2))
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = np.zeros((height, width, 3), np.uint8)
    mask[:, :] = hsv[:, :]
    return maskb,maskw

def findStartingPoint(video, numberOfFrames):
    # the function will go numberOfFrames frames ahead in the video and do a subtraction
    # the hope is that the fish will have moved at some point during this time
    count = 0
    # I don't know a better way to jump ahead so many frames
    while count <= numberOfFrames:
        # read in the frame for each tick of the loop
        ret, frame = video.read()
        # grab a frame from the middle. Assume the screens have turned on by then
        if count == numberOfFrames / 2:
            hsv_middle = convertToHSV(frame)
        if count == numberOfFrames / 4:
            hsv_Q1 = convertToHSV(frmae)
        if count == numberOfFrames:
            hsv_end = convertToHSV(frame)
        count += 1
        print "." * (count % 20)

    difference2 = cv2.subtract(hsv_end, hsv_initial)
    difference1 = cv2.subtract(hsv_end, hsv_middle)
    difference3 = cv2.subtract(hsv_Q1, hsv_end)
    difference4 = cv2.subtract(difference1, difference3)
    difference5 = cv2.subtract(difference2, difference2)
    difference = cv2.subtract(difference5, difference4)
    thresh = cv2.inRange(difference, np.array([0, 0, 0]), np.array([255, 255, 25]))
    invert = cv2.bitwise_not(thresh)
    return startingPoint

def findStartingPointScoto(video, numberOfFrames):
    # the function will go numberOfFrames frames ahead in the video and do a subtraction
    # the hope is that the fish will have moved at some point during this time
    count = 0
    # I don't know a better way to jump ahead so many frames
    while count <= numberOfFrames:
        # read in the frame for each tick of the loop
        ret, frame = video.read()
        # grab a frame from the middle. Assume the screens have turned on by then
        if count == numberOfFrames / 2:
            hsv_middle = convertToHSV(frame)
        if count == numberOfFrames / 4:
            hsv_Q1 = convertToHSV(frmae)
        if count == numberOfFrames:
            hsv_end = convertToHSV(frame)
        count += 1
        print "." * (count % 20)

    difference2 = cv2.subtract(hsv_end, hsv_initial)
    difference1 = cv2.subtract(hsv_end, hsv_middle)
    difference3 = cv2.subtract(hsv_Q1, hsv_end)
    difference4 = cv2.subtract(difference1, difference3)
    difference5 = cv2.subtract(difference2, difference2)
    difference = cv2.subtract(difference5, difference4)
    startingPointWhite = returnLargeContour(invert)
    startingpointBlack = returnLargeContour(thresh)
    return startingpointBlack, startingPointWhite

# returns centroid from largest contour from a binary image
def returnLargeContour(frame):
    potential_centroids = []

    # find all contours in the frame
    contours = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    print "number of contours: " + str(len(contours))

    for z in contours:
        # calculate some things
        area = cv2.contourArea(z)
        x, y, w, h = cv2.boundingRect(z)
        aspect_ratio = float(w) / h
        #the main filtering statement
        if area > 60 and area < 10000:  #and aspect_ratio <= 2.0 and aspect_ratio >= 0.5
            potential_centroids.append(z)
            print area
            print aspect_ratio

    largestCon = sorted(potential_centroids, key=cv2.contourArea, reverse=True)[:1]

    if len(potential_centroids) == 0:
        csv_writer.writerow(("NA", "NA", counter))
        return ()
    else:
        for j in largestCon:
            m = cv2.moments(j)
            centroid_x = int(m['m10'] / m['m00'])
            centroid_y = int(m['m01'] / m['m00'])
            csv_writer.writerow((centroid_x, centroid_y, counter))
            return ((centroid_x, centroid_y))

def returnLargeContoursScoto(frameb, framew):
    potential_centroidsb = []
    potential_centroidsw = []
    # find all contours in the frame
    contours = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    print "number of contours: " + str(len(contours))

    for z in contours:
        # calculate some things
        area = cv2.contourArea(z)
        x, y, w, h = cv2.boundingRect(z)
        aspect_ratio = float(w) / h
        #the main filtering statement
        if area > 60 and area < 10000:  #and aspect_ratio <= 2.0 and aspect_ratio >= 0.5
            potential_centroids.append(z)
            print area
            print aspect_ratio

    largestCon = sorted(potential_centroids, key=cv2.contourArea, reverse=True)[:1]

    if len(potential_centroids) == 0:
        csv_writer.writerow(("NA", "NA", counter))
        return ()
    else:
        for j in largestCon:
            m = cv2.moments(j)
            centroid_x = int(m['m10'] / m['m00'])
            centroid_y = int(m['m01'] / m['m00'])
            csv_writer.writerow((centroid_x, centroid_y, counter))
            return ((centroid_x, centroid_y))


if '__name__'=='__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inputVideo", help="path to the video")
    ap.add_argument("-s", "--scoto", help="for scototaxis videos", action="store_true")
    args = vars(ap.parse_args())
    lower = np.array([0, 0, 0])
    upper = np.array([255, 255, 25])
    counter = 0
    cap = cv2.VideoCapture(args["inputVideo"])
    name = re.split('[/.]', args["inputVideo"], flags=re.IGNORECASE)[-2]
    name = name + ".csv"
    #print(name)
    myfile = open(name, 'wb')
    csv_writer = csv.writer(myfile, quoting=csv.QUOTE_NONE)
    csv_writer.writerow(("x", "y", "frame"))

    ret, frame = cap.read()
    hsv_initial = convertToHSV(frame)

    while ret:
        if args["scoto"]:
            cv2.setMouseCallback('image', on_mouse2, None)
            blackbox =[]
            whitebox=[]
            if len(blackbox) > 3:
                blackbx, bx1, bx2, bx3, bx4 = drawbox(blackbox)
                cv2.polylines(frame, np.int32([blackbx]), 1, (0, 0, 255, 0))
                cv2.setMouseCallback('image', on_mouse2, None)
                if len(whitebox) > 3:
                    whitebx, wx1, wx2, wx3, wx4 = drawbox(whitebox)
                    cv2.polylines(frame, np.int32([whitebx]), 1, (255, 255, 0, 0))
                else:
                    pass
            else:
                pass

            if counter == 0:
                findStartingPoint(cap, 100)
                counter += 1
                # re-start the video capture
                cap = cv2.VideoCapture(args["inputVideo"])

            else:
                ret, frame = cap.read()
                hsv = convertToHSV(frame)
                difference = cv2.subtract(hsv_initial, hsv)
                masked = cv2.inRange(difference, lower, upper)
                maskedInvert = cv2.bitwise_not(masked)

                center = returnLargeContour(maskedInvert)

                if center:
                    cv2.circle(frame, center, 3, [255, 0, 0], -1)
                cv2.imshow('image', frame)
                #cv2.imshow('thresh', masked)
                #cv2.imshow('diff', difference)
                k = cv2.waitKey(1)
                if k == 27:
                    break
                # the idea here is to re-set the 'initial' image every 100 frames in case there are changes with the light or top of the water reflections
                if counter == 100 or counter == 200 or counter == 300:
                    hsv_initial = hsv
                counter += 1

        else:
            if counter == 0:
                findStartingPoint(cap, 100)
                counter += 1
                # re-start the video capture
                cap = cv2.VideoCapture(args["inputVideo"])
            else:
                ret, frame = cap.read()
                hsv = convertToHSV(frame)
                difference = cv2.subtract(hsv_initial, hsv)
                masked = cv2.inRange(difference, lower, upper)
                maskedInvert = cv2.bitwise_not(masked)
                # find the centroid of the largest blob
                center = returnLargeContour(maskedInvert)
                # draw the centroids on the image
                if center:
                    cv2.circle(frame, center, 3, [0, 0, 255], -1)
                cv2.imshow('image', frame)
                cv2.imshow('thresh', masked)
                cv2.imshow('diff', difference)
                k = cv2.waitKey(1)
                if k == 27:
                    break
                if counter == 100 or counter == 200 or counter == 300:
                    hsv_initial = hsv
                counter += 1
    cv2.destroyAllWindows()
