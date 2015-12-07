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


def on_mouse2(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print 'Start Mouse Position: ' + str(x) + ', ' + str(y)
        sbox = [x, y]
        rois.append(sbox)
    elif event == cv2.EVENT_LBUTTONUP:
        print 'End Mouse Position: ' + str(x) + ', ' + str(y)
        ebox = [x, y]
        rois.append(ebox)


def drawbox(boxpoints):
    (x1, y1) = boxpoints[-4]
    (x2, y2) = boxpoints[-3]
    (x3, y3) = boxpoints[-2]
    (x4, y4) = boxpoints[-1]
    lilbx = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    return lilbx, x1, x2, x3, x4


def activitylevel(inddata):
    pixdistance = np.sqrt((inddata['x'].diff()) ** 2 + (inddata['y'].diff()) ** 2)
    inddata['stepdistanceRight'] = np.where(inddata['inrgt'], pixdistance, None)
    inddata['stepdistanceLeft'] = np.where(inddata['inlft'], pixdistance, None)
    inddata['stepdistanceMiddle'] = np.where(inddata['inmid'], pixdistance, None)
    inddata['stepdistanceTotal'] = pixdistance
    inddata.fillna(value=0, inplace=True)
    return inddata


def getroidata(xs1, xs2, xs3, xs4):
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


def getthigmodata(datfram, roibox):
    [x1b, y1b], [x2b, y2b], [x3b, y3b], [x4b, y4b] = roibox
    avgtop = int((y1b + y2b) / 2)
    avgbot = int((y3b + y4b) / 2)
    datfram['atedge'] = np.where((data['y'] < avgtop) | (data['y'] > avgbot), 1, None)
    return datfram


def scotoregion(lilbx):
    print lilbx
    datfram = lilbx
    return datfram


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

'''
def masterdatata(fishid, inddata, masterdata):  ###need to split name a la name_day_session
    indnom, day, session, = fishid.split("_")
    masterdata.loc[str(len(masterdata))] = pd.Series({'fishName': indnom, 'session': session, 'day': day,
                                                      'trialtype': 'numerosity'
                                                      'timeRight': inddata['inrgt'].sum(),
                                                      'timeLeft': inddata['inlft'].sum(),
                                                      'timeMiddle': inddata['inmid'].sum(),
                                                      'activityLeft': inddata['stepdistanceLeft'].sum(),
                                                      'activityRight': inddata['stepdistanceRight'].sum(),
                                                      'activityMiddle': inddata['stepdistanceMiddle'].sum(),
                                                      'activityTotal': inddata['stepdistanceTotal'].sum(),
                                                      'propActivityRight': float(inddata['stepdistanceRight'].sum()) /
                                                                           inddata['stepdistanceTotal'].sum(),
                                                      'propActivityLeft': float(inddata['stepdistanceLeft'].sum()) /
                                                                          inddata['stepdistanceTotal'].sum(),
                                                      'propActivityMiddle': float(inddata['stepdistanceMiddle'].sum()) /
                                                                            inddata['stepdistanceTotal'].sum(),
                                                      'timeEdge': inddata['atedge'].sum(),
                                                      'propTimeEdge': inddata['atedge'].sum() / float(len(inddata)),
                                                      'propTimeLeft': inddata['inlft'].sum() / float(len(inddata)),
                                                      'propTimeRight': inddata['inrgt'].sum() / float(len(inddata)),
                                                      'propTimeMiddle': inddata['inmid'].sum() / float(len(inddata))})
    return masterdata
'''

def masterdatato(fishid, inddata, masterdata):

    if args['mateChoice']:
        indnom, maleside, unused = fishid.split("_")
        masterdata.loc[str(len(masterdata))] = pd.Series({'fishName': indnom,
                                                      'timeRight': inddata['inrgt'].sum(), 'sex': 'F',
                                                      'trialtype': 'choice',
                                                      'timeLeft': inddata['inlft'].sum(),
                                                      'timeMiddle': inddata['inmid'].sum(),
                                                      'timeEdge': inddata['atedge'].sum(),
                                                      'propTimeEdge': inddata['atedge'].sum() / float(len(inddata)),
                                                      'propTimeLeft': inddata['inlft'].sum() / float(len(inddata)),
                                                      'propTimeRight': inddata['inrgt'].sum() / float(len(inddata)),
                                                      'propTimeMiddle': inddata['inmid'].sum() / float(len(inddata)),
                                                      'activityLeft': inddata['stepdistanceLeft'].sum(),
                                                      'activityRight': inddata['stepdistanceRight'].sum(),
                                                      'activityMiddle': inddata['stepdistanceMiddle'].sum(),
                                                      'activityTotal': inddata['stepdistanceTotal'].sum(),
                                                      'propActivityRight': float(inddata['stepdistanceRight'].sum()) /
                                                                           inddata['stepdistanceTotal'].sum(),
                                                      'propActivityLeft': float(inddata['stepdistanceLeft'].sum()) /
                                                                          inddata['stepdistanceTotal'].sum(),
                                                      'propActivityMiddle': float(inddata['stepdistanceMiddle'].sum()) /
                                                                            inddata['stepdistanceTotal'].sum(),
                                                      'timeStim': inddata['inrgt'].sum() if maleside == 'R' else
                                                          inddata['inlft'].sum(),
                                                      'activityStim': inddata['stepdistanceRight'].sum() if
                                                          maleside == 'R' else inddata['stepdistanceLeft'].sum(),
                                                      'propTimeStim': inddata['inrgt'].sum() / float(len(inddata)) if
                                                          maleside == 'R' else inddata['inlft'].sum() / float(len(inddata)),
                                                      'propActivityStim': float(inddata['stepdistanceRight'].sum()) /
                                                                              inddata['stepdistanceTotal'].sum() if
                                                          maleside == 'R' else float(inddata['stepdistanceLeft'].sum())})

    if args['socioData']:
        indnom, groupside, sex = fishid.split("_")
        masterdata.loc[str(len(masterdata))] = pd.Series({'fishName': indnom,
                                                      'timeRight': inddata['inrgt'].sum(), 'sex': sex,
                                                      'trialtype': 'socio',
                                                      'timeLeft': inddata['inlft'].sum(),
                                                      'timeMiddle': inddata['inmid'].sum(),
                                                      'timeEdge': inddata['atedge'].sum(),
                                                      'propTimeEdge': inddata['atedge'].sum() / float(len(inddata)),
                                                      'propTimeLeft': inddata['inlft'].sum() / float(len(inddata)),
                                                      'propTimeRight': inddata['inrgt'].sum() / float(len(inddata)),
                                                      'propTimeMiddle': inddata['inmid'].sum() / float(len(inddata)),
                                                      'activityLeft': inddata['stepdistanceLeft'].sum(),
                                                      'activityRight': inddata['stepdistanceRight'].sum(),
                                                      'activityMiddle': inddata['stepdistanceMiddle'].sum(),
                                                      'activityTotal': inddata['stepdistanceTotal'].sum(),
                                                      'propActivityRight': float(inddata['stepdistanceRight'].sum()) /
                                                                           inddata['stepdistanceTotal'].sum(),
                                                      'propActivityLeft': float(inddata['stepdistanceLeft'].sum()) /
                                                                          inddata['stepdistanceTotal'].sum(),
                                                      'propActivityMiddle': float(inddata['stepdistanceMiddle'].sum()) /
                                                                            inddata['stepdistanceTotal'].sum(),
                                                      'timeStim': inddata['inrgt'].sum() if groupside == 'R' else
                                                          inddata['inlft'].sum(),
                                                      'activityStim': inddata['stepdistanceRight'].sum() if
                                                          groupside == 'R' else inddata['stepdistanceLeft'].sum(),
                                                      'propTimeStim': inddata['inrgt'].sum() / float(len(inddata)) if
                                                          groupside == 'R' else inddata['inlft'].sum() / float(len(inddata)),
                                                      'propActivityStim': float(inddata['stepdistanceRight'].sum()) /
                                                                              inddata['stepdistanceTotal'].sum() if
                                                          groupside == 'R' else float(inddata['stepdistanceLeft'].sum())})

    if args['scotoData']:
        pass

    else:
        species, round, SL, sex, indnom, day, session, stimulus, presside = fishid.split("_")
        masterdata.loc[str(len(masterdata))] = pd.Series({'fishName': indnom, 'session': session, 'day': day,
                                                          'trialtype': 'numerosity',
                                                          'timeRight': inddata['inrgt'].sum(),
                                                          'timeLeft': inddata['inlft'].sum(),
                                                          'timeMiddle': inddata['inmid'].sum(),
                                                          'activityLeft': inddata['stepdistanceLeft'].sum(),
                                                          'activityRight': inddata['stepdistanceRight'].sum(),
                                                          'activityMiddle': inddata['stepdistanceMiddle'].sum(),
                                                          'activityTotal': inddata['stepdistanceLeft'].sum() + inddata[
                                                              'stepdistanceRight'].sum() + inddata[
                                                                               'stepdistanceMiddle'].sum(),
                                                          'propActivityRight': float(inddata['stepdistanceRight'].sum()) /
                                                                               inddata['stepdistanceTotal'].sum(),
                                                          'propActivityLeft': float(inddata['stepdistanceLeft'].sum()) /
                                                                              inddata['stepdistanceTotal'].sum(),
                                                          'propActivityMiddle': float(inddata['stepdistanceMiddle'].sum()) /
                                                                                inddata['stepdistanceTotal'].sum(),
                                                          'timeEdge': inddata['atedge'].sum(),
                                                          'propTimeEdge': inddata['atedge'].sum() / float(len(inddata)),
                                                          'propTimeLeft': inddata['inlft'].sum() / float(len(inddata)),
                                                          'propTimeRight': inddata['inrgt'].sum() / float(len(inddata)),
                                                          'propTimeMiddle': inddata['inmid'].sum() / float(len(inddata)),
                                                          'species': species, 'standardLength': SL, 'sex': sex,
                                                          'ROUND': round,
                                                          'stimulus': stimulus, 'stimSide': presside,
                                                          'timeStim': inddata['inrgt'].sum() if presside == 'R' else
                                                          inddata['inlft'].sum(),
                                                          'activityStim': inddata['stepdistanceRight'].sum() if
                                                          presside == 'R' else inddata['stepdistanceLeft'].sum(),
                                                          'propTimeStim': inddata['inrgt'].sum() / float(len(inddata)) if
                                                          presside == 'R' else inddata['inlft'].sum() / float(len(inddata)),
                                                          'propActivityStim': float(inddata['stepdistanceRight'].sum()) /
                                                                              inddata['stepdistanceTotal'].sum() if
                                                          presside == 'R' else float(inddata['stepdistanceLeft'].sum()) /
                                                                               inddata['stepdistanceTotal'].sum()})
    return masterdata


if __name__ == "__main__":
    ### setup arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--inputVideo", help="path to the video, defaults to numerosity videos")
    ap.add_argument("-t", "--trackingData", help="tracking data .csv file, defaults to numerosity data")
    ap.add_argument("-m", "--masterData", help="master data sheet")
    ap.add_argument("-c", "--mateChoice", help="indicates matechoice tracking data", action='store_true')
    ap.add_argument("-g", "--socioData", help="indicates sociality tracking data", action='store_true')
    ap.add_argument("-s", "--scotoData", help="indicates scototaxis tracking data", action='store_true')
    ap.add_argument("-f", "--fixROIs", help="only used for initial data, fixed in later versions", action='store_true')
    args = vars(ap.parse_args())

    ### read in video/tracking data
    try:
        cap = args["inputVideo"]
        name, ext = args["inputVideo"].split(".")
        cv2.namedWindow("tankview", cv2.WINDOW_AUTOSIZE)
        vid = cv2.VideoCapture(cap)
        try:
            tdatnom, exr = args["trackingData"].split(".")
        except:
            print 'I see a video but no tracking data. tell me where to look with: "-t"'
            exit()
        assert name == tdatnom, "the names of these files do not match: %r != %r" % (name, tdatnom)
        data = pd.read_csv(args["trackingData"])
        data.interpolate(method='linear', inplace=True)
    except:
        print 'missing files...'
        exit()

    #################### mark ROIS on video
    boxes = []
    rois = []
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
            cv2.setMouseCallback('tankview', on_mouse2, None)
            if len(rois) > 3:
                lilbx2, xs12, xs22, xs32, xs42 = drawbox(rois)
                cv2.polylines(frame, np.int32([lilbx2]), 1, (0, 255, 0, 0))
                # if k == 115:  # 's' #Mac
                if k == 1048691:  # 's' #Linux
                    data.fillna(value=0, inplace=True)
                    data = data[data['x'] != 0]
                    if args["scotoData"]:
                        data = scotoregion(lilbx)
                    else:
                        # bs = data.columns.values.tolist()
                        # print bs
                        data = getroidata(xs1, xs2, xs3, xs4)
                        data = getthigmodata(data, lilbx2)
                        data = activitylevel(data)
                        # data = distance(data)
                    cv2.destroyWindow("tankview")
                    cv2.waitKey(1)
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)
                    vid.release()
                    rval = False
                    data.to_csv(name + '_processed.csv')
                    break
                # elif k == 99:  # 'c' #Mac
                elif k == 1048675:  # 'c' #Linux
                    print 'clear'
                    del boxes[:]
                    del rois[:]
            else:
                pass
        cv2.imshow("tankview", frame)
    cv2.destroyWindow("tankview")
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    ### Data Sheet creation
    if args["socioData"]:
        try:
            metadataSocio = pd.read_csv(args["masterData"])
        except IOError:
            print 'the data master-list is missing?'
            print 'searching directory'
        try:
            assert (os.path.exists('masterdataSocio.csv'))
            masterdataSocio = pd.read_csv('masterdataSocio.csv')
        except AssertionError:
            put = raw_input('No master file entered or found. Create new masterfile? [y/n]: ')
            print put
            if str(put) == 'y':
                print 'making master data sheet...'


        ######
                masterdataSocio = pd.DataFrame(columns={
                                         'fishID', 'fishName', 'species', 'sex', 'stimSide', 'trialtype',
                                         'timeStim', 'activityStim', 'propTimeStim',
                                         'propActivityStim',
                                         'activityTotal',
                                         'activityLeft', 'activityRight', 'activityMiddle',
                                         'propActivityLeft', 'propActivityRight', 'propActivityMiddle',
                                         'timeLeft', 'timeRight', 'timeMiddle',
                                         'propTimeLeft', 'propTimeRight', 'propTimeMiddle',
                                         'timeEdge', 'propTimeEdge', })
        masterdataSocio = masterdatato(tdatnom, data, masterdataSocio)
        masterdataSocio.to_csv('masterdataChoice.csv', index=False, columns=['species', 'sex', 'round', 'day',
                                                                              'trialtype',
                                                                                  'session',
                                                                                  'standardLength', 'fishID',
                                                                                  'fishName', 'timeEdge',
                                                                                  'propTimeEdge',
                                                                                  'propTimeStim', 'propActivityStim',
                                                                                  'stimulus', 'stimSide', 'timeStim',
                                                                                  'activityStim',
                                                                                  'activityTotal', 'activityLeft',
                                                                                  'activityRight', 'activityMiddle',
                                                                                  'propActivityLeft',
                                                                                  'propActivityRight',
                                                                                  'propActivityMiddle', 'timeLeft',
                                                                                  'timeRight', 'timeMiddle',
                                                                                  'propTimeLeft', 'propTimeRight',
                                                                                  'propTimeMiddle', 'survivalMetric'])
        print masterdataChoice
    if args["mateChoice"]:
        try:
            metadataChoice = pd.read_csv(args["masterData"])
        except IOError:
            print 'the data master-list is missing?'
            print 'searching directory'
        try:
            assert (os.path.exists('masterdataChoice.csv'))
            masterdataChoice = pd.read_csv('masterdataChoice.csv')
        except AssertionError:
            put = raw_input('No master file entered or found. Create new masterfile? [y/n]: ')
            print put
            if str(put) == 'y':
                print 'making master data sheet...'


        ######
                masterdataChoice = pd.DataFrame(columns={
                                         'fishID', 'fishName', 'species', 'sex', 'stimSide', 'trialtype',
                                         'timeStim', 'activityStim', 'propTimeStim',
                                         'propActivityStim',
                                         'activityTotal',
                                         'activityLeft', 'activityRight', 'activityMiddle',
                                         'propActivityLeft', 'propActivityRight', 'propActivityMiddle',
                                         'timeLeft', 'timeRight', 'timeMiddle',
                                         'propTimeLeft', 'propTimeRight', 'propTimeMiddle',
                                         'timeEdge', 'propTimeEdge', })
        masterdataChoice = masterdatato(tdatnom, data, masterdataChoice)
        masterdataChoice.to_csv('masterdataChoice.csv', index=False, columns=['species', 'sex', 'round', 'day',
                                                                              'trialtype',
                                                                                  'session',
                                                                                  'standardLength', 'fishID',
                                                                                  'fishName', 'timeEdge',
                                                                                  'propTimeEdge',
                                                                                  'propTimeStim', 'propActivityStim',
                                                                                  'stimulus', 'stimSide', 'timeStim',
                                                                                  'activityStim',
                                                                                  'activityTotal', 'activityLeft',
                                                                                  'activityRight', 'activityMiddle',
                                                                                  'propActivityLeft',
                                                                                  'propActivityRight',
                                                                                  'propActivityMiddle', 'timeLeft',
                                                                                  'timeRight', 'timeMiddle',
                                                                                  'propTimeLeft', 'propTimeRight',
                                                                                  'propTimeMiddle', 'survivalMetric'])
        print masterdataChoice
            ##################
    else:
        try:
            metadataNumerosity = pd.read_csv(args["masterData"])
        except IOError:
            print 'the data master-list is missing?'
            print 'searching directory'
        try:
            assert (os.path.exists('masterdataNumerosity.csv'))
            masterdataNumerosity = pd.read_csv('masterdataNumerosity.csv')
        except AssertionError:
            put = raw_input('No master file entered or found. Create new masterfile? [y/n]: ')
            print put
            if str(put) == 'y':
                print 'making master data sheet...'
                masterdataNumerosity = pd.DataFrame(columns={'day', 'session', 'round', 'trialtype',
                                                             'fishID', 'fishName', 'species', 'sex', 'standardLength',
                                                             'survivalMetric',
                                                             'stimulus', 'stimSide',
                                                             'timeStim', 'activityStim', 'propTimeStim',
                                                             'propActivityStim',
                                                             'activityTotal',
                                                             'activityLeft', 'activityRight', 'activityMiddle',
                                                             'propActivityLeft', 'propActivityRight', 'propActivityMiddle',
                                                             'timeLeft', 'timeRight', 'timeMiddle',
                                                             'propTimeLeft', 'propTimeRight', 'propTimeMiddle',
                                                             'timeEdge', 'propTimeEdge', })
        if str(put) == 'n':
            print 'locate master data and place in this directory. use "-m" tag. Then resume.'
            print 'exiting'
            exit()
        masterdataNumerosity = masterdatato(tdatnom, data, masterdataNumerosity)


        ######################write to file


        masterdataNumerosity.to_csv('masterdataNumerosity.csv', index=False, columns=['species', 'sex', 'round', 'day',
                                                                                      'trialtype',
                                                                                  'session',
                                                                                  'standardLength', 'fishID',
                                                                                  'fishName', 'timeEdge',
                                                                                  'propTimeEdge',
                                                                                  'propTimeStim', 'propActivityStim',
                                                                                  'stimulus', 'stimSide', 'timeStim',
                                                                                  'activityStim',
                                                                                  'activityTotal', 'activityLeft',
                                                                                  'activityRight', 'activityMiddle',
                                                                                  'propActivityLeft',
                                                                                  'propActivityRight',
                                                                                  'propActivityMiddle', 'timeLeft',
                                                                                  'timeRight', 'timeMiddle',
                                                                                  'propTimeLeft', 'propTimeRight',
                                                                                  'propTimeMiddle', 'survivalMetric'])
        print masterdataNumerosity
