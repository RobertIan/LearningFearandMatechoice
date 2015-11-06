__author__ = 'ian'


import pandas as pd
import numpy as np
import sys

#import data
data = pd.read_csv(sys.argv[1])

#define subsets
sexgroup = data.groupby('sex')
speciesgroup = data.groupby('species')
daygroup = data.groupby('day')

learners = data[(data.day>4) & (data.propTimeStim>0.60)]
nonlearners = data[(data.day>4) & (data.propTimeStim<0.60)]

learnersbyday = learners.groupby('day')
nonlearnersbyday = nonlearners.groupby('day')

learnersbysex = learners.groupby('sex')
nonlearnersbysex = nonlearners.groupby('sex')

learnersbyspecies = learners.groupby('species')
nonlearnersbyspecies = nonlearners.groupby('species')









'''

'species', 'sex', 'round', 'day',
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
                                                                                  'propTimeMiddle', 'survivalMetric']


'''