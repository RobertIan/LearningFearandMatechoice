__author__ = 'ian'
import cv2
import os
import numpy as np
import pandas as pd
import argparse

############


def on_mouse(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'Start Mouse Position: ' + str(x) + ', ' + str(y)
        sbox = [x, y]
        boxes.append(sbox)
    elif event == cv2.EVENT_LBUTTONUP:
        print 'End Mouse Position: ' + str(x) + ', ' + str(y)
        ebox = [x, y]
        boxes.append(ebox)


def drawbox(boxpoints):
    (x1, y1) = boxpoints[-4]
    (x2, y2) = boxpoints[-3]
    (x3, y3) = boxpoints[-2]
    (x4, y4) = boxpoints[-1]
    lilbx = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    return lilbx, x1, x2, x3, x4


def getregions(xs1, xs2, xs3, xs4):
    xlist = [xs1, xs2, xs3, xs4]
    xlist.sort()
    xmin = xlist[0]
    xmax = xlist[3]
    third = (xmax - xmin) / 3
    xmidmin = xmin + third
    xmidmax = xmidmin + third
    data['lftmin'] = xmin
    data['midstrt'] = xmidmin
    data['midstp'] = xmidmax
    data['rgtmax'] = xmax
    data['inrgt'] = np.where(data['x'] > data['midstp'], 1, None)
    data['inlft'] = np.where(data['x'] < data['midstrt'], 1, None)
    data['inmid'] = np.where((data['midstrt'] < data['x']) & (data['x'] < data['midstp']), 1, None)

    return data


def fixROIs(datfram):
    rexmin = datfram['lftmin']
    rexmax = datfram['rgtmax']
    third = (rexmax - rexmin) / 3
    rexmidmin = rexmin + third
    rexmidmax = rexmidmin + third
    datfram['lftmin'] = rexmin
    datfram['midstrt'] = rexmidmin
    datfram['midstp'] = rexmidmax
    datfram['rgtmax'] = rexmax
    datfram['inrgt'] = np.where(datfram['x'] > datfram['midstp'], 1, None)
    datfram['inlft'] = np.where(datfram['x'] < datfram['midstrt'], 1, None)
    datfram['inmid'] = np.where((datfram['midstrt'] < datfram['x']) & (datfram['x'] < datfram['midstp']), 1, None)

    return datfram


def metadatata(fishid, inddata, masterdata): ###need to split name a la name_day_session
    indnom = fishid[:-1]
    session= int(fishid[-1:])
    '''
    if 0<session<5:
        day = 1
    if 4<session<9:
        day = 2
    if 8<session<13:
        day = 1
    if 4<session<9:
        day = 2
    '''
    masterdata.loc[str(len(masterdata))] = pd.Series({'fishID':indnom, 'session': session, 'timeL':inddata['inrgt'].sum(),
                                            'timeR':inddata['inlft'].sum(), 'timeM':inddata['inmid'].sum()})

    return masterdata

############

if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--inputVideo", help="path to the video")
    ap.add_argument("-t", "--trackingData", help="tracking data .csv file")
    ap.add_argument("-r", "--reloadData",
                    help="previous output, with ROI measured and interpolation 				performed")
    ap.add_argument("-m", "--masterData", help="master data sheet")
    ap.add_argument("-s", "--scotoData", help="scototaxis tracking data")
    ap.add_argument("-f", "--fixROIs", help="only used for initial data, fixed in later versions", action='store_true')
    args = vars(ap.parse_args())

    try:
        dname, ext = args["reloadData"].split(".")
        data2 = pd.read_csv(args["reloadData"])
        if args["fixROIs"]:
            print "fixing Ian's silly mistake"
            fixROIs(data2)
            data2.to_csv('data_fixed/' + dname + '.csv')
            exit()
    except:
        pass

    try:
        cap = args["inputVideo"]
        name, ext = args["inputVideo"].split(".")
        boxes = []
        cv2.namedWindow("tankview", cv2.WINDOW_AUTOSIZE)
        vid = cv2.VideoCapture(cap)
        try:
            tdatnom, exr = args["trackingData"].split(".")
        except:
            print 'I see a video but no tracking data. tell me where to look with: "-t"'
            exit()

        assert name == tdatnom, "the names of these files do not match: %r != %r" % (name, tdatnom)

        data = pd.read_csv(args["trackingData"], index_col=0)

        data.interpolate(method='linear', inplace=True)


    except:
        print 'missing files...'
        exit()



    if vid.isOpened():
        rval, frame = vid.read()
    else:
        rval = False

    while rval:
        k = cv2.waitKey(1)

        cv2.setMouseCallback('tankview', on_mouse, None)

        flag, frame = vid.read()
        if flag == 0:
            break

        if len(boxes) > 3:
            lilbx, xs1, xs2, xs3, xs4 = drawbox(boxes)
            cv2.polylines(frame, np.int32([lilbx]), 1, (0, 0, 255, 0))
            if k == 115: # 's' #Mac
            #if k == 1048691:  # 's' #Linux
                data = getregions(xs1, xs2, xs3, xs4)
                cv2.destroyWindow("tankview")
                cv2.waitKey(1)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
                vid.release()
                rval = False
                data.to_csv(name+'.csv')
                break
            elif k == 99: # 'c' #Mac
            #elif k == 1048675:  # 'c' #Linux
                print 'clear'
                del boxes[:]
            else:
                pass
        cv2.imshow("tankview", frame)

    cv2.destroyWindow("tankview")
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    try:
        metadat = pd.read_csv(args["masterData"])
    except IOError:
        print 'the data master-list is missing?'
        print 'searching directory'
    try:
        assert (os.path.exists('masterdata.csv'))
        metadat = pd.read_csv('masterdata.csv', index_col=0)
    except AssertionError:
        put = raw_input('No master file entered or found. Create new masterfile? [y/n]: ')
        print put
        if str(put) == 'y':
            print 'making master data sheet...'
            metadat = pd.DataFrame(columns={'day', 'session', 'fishID', 'activityT', 'activityL', 'activityR', 'activityM',
                                        'timeL', 'timeR', 'timeM'})
        if str(put) == 'n':
            print 'locate master data and place in this directory. use "-m" tag. Then resume.'
            print 'exiting'
            exit()

    metadat = metadatata(tdatnom, data, metadat)
    metadat.to_csv('masterdata.csv')
    print metadat