__author__ = 'ian'
import pandas as pd
import numpy as np
from scipy import stats
import sys
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go

#import data
data = pd.read_csv('masterdataNumerosity_sailfins.csv')
data['condition']=np.where(data['fishName'].str[:1]=='H','High','Low')
#
#
#
##############################
# side bias
tankRight = data.loc[data.tank=='R', ['propTimeRight', 'propTimeLeft']]
tankLeft = data.loc[data.tank=='L', ['propTimeRight', 'propTimeLeft']]
trace3 = go.Box(y=tankRight.propTimeRight,name='Right Tank Right Side')
trace2 = go.Box(y=tankRight.propTimeLeft,name='Right Tank Left Side')
trace1 = go.Box(y=tankLeft.propTimeRight,name='Left Tank Right Side')
trace0 = go.Box(y=tankLeft.propTimeLeft,name='Left Tank Left Side')
datum = [trace0, trace1, trace2, trace3]
sidebiasanovaF, sidebiasanovaP = stats.f_oneway(tankLeft.propTimeLeft, tankLeft.propTimeRight, tankRight.propTimeLeft, tankRight.propTimeRight)
sidebiasLeftLeftvLeftRightT, sidebiasLeftLeftvLeftRightP = stats.ttest_rel(tankLeft.propTimeLeft,tankLeft.propTimeRight)
sidebiasLeftLeftvRightRightT, sidebiasLeftLeftvRightRightP = stats.ttest_ind(tankLeft.propTimeLeft,tankRight.propTimeRight)

fig1 = go.Figure(data=datum)
plot_url = py.plot(fig1, filename='tank side bias')
print 'sidebiasanovaF: ', sidebiasanovaF
print 'sidebiasanovaP: ', sidebiasanovaP
print 'sidebiasLeftLeftvLeftRightT', sidebiasLeftLeftvLeftRightT
print 'sidebiasLeftLeftvLeftRightP', sidebiasLeftLeftvLeftRightP
###we see a bias in the left tank towards the right side/away from left side
### is this side bias correlated with thigmotaxis (our measure of stress)?
##############################
#
#
##############################
#stress levels (thigmotaxis)
righttank = data.loc[data.tank=='R',['propTimeEdge']]
lefttank = data.loc[data.tank=='L',['propTimeEdge']]
tr = go.Box(y=righttank.propTimeEdge,name='righttankstress')
tr2 = go.Box(y=lefttank.propTimeEdge, name='lefttankstress')
stressdata = [tr,tr2]
stressfig = go.Figure(data=stressdata)
stressplot = py.plot(stressfig, filename='stress by tank')
stresbytankU, stressbytankP = stats.ttest_ind(righttank.propTimeEdge, lefttank.propTimeEdge)
print 'stressbytankT',stressbytankT
print 'stressbytankP', stressbytankP
###stress levels are similar in both tanks

hightrainers = data.loc[data.condition=='High',['propTimeEdge']]
lowtrainers = data.loc[data.condition=='Low',['propTimeEdge']]
tr222 = go.Box(y=hightrainers.propTimeEdge,name='hightrainerstress')
tr2222 = go.Box(y=lowtrainers.propTimeEdge, name='lowtrainerstress')
stressdatahighlow = [tr222,tr2222]
stressfighl = go.Figure(data=stressdatahighlow)
stressplothl = py.plot(stressfighl, filename='stress by trained condition')
stressbytrainerT, stressbytrainerP = stats.ttest_ind(hightrainers.propTimeEdge, lowtrainers.propTimeEdge)
print 'stressbytrainerT',stressbytrainerT
print 'stressbytrainerP', stressbytrainerP
###stress levels are similar across training groups
##############################
#
#
##############################
# performance by ratio on testing days
'''
# individual trials
testing_days = data.loc[data["day"]>=5, ["fishName", "propTimeStim", "day", "ratio"]]

testdays5 = testing_days.loc[testing_days['ratio']==0.5, ["fishName", "propTimeStim"]]
testdays6 = testing_days.loc[testing_days['ratio']==0.67, ["fishName", "propTimeStim"]]
testdays7 = testing_days.loc[testing_days['ratio']==0.75, ["fishName", "propTimeStim"]]

x1 = testdays5.propTimeStim
x2 = testdays7.propTimeStim

trace5 = go.Scatter(y=testdays6.propTimeStim,x=x1,mode='markers',name='0.67v0.50',text=testdays6.index)
trace6 = go.Scatter(y=testdays7.propTimeStim,x=x1,mode='markers',name='0.75v0.50',text=testdays7.index)
trace7 = go.Scatter(y=testdays6.propTimeStim,x=x2,mode='markers',name='0.67v0.75',text=testdays6.index)

datuma = [trace5, trace6, trace7]
fig2 = go.Figure(data=datuma)
plot_url1 = py.plot(fig2, filename='cross-ratio performance (inc. reinf.)')

# averages
testdays5avgs = testdays5.groupby('fishName').propTimeStim.mean()
testdays6avgs = testdays6.groupby('fishName').propTimeStim.mean()
testdays7avgs = testdays7.groupby('fishName').propTimeStim.mean()

traceA = go.Scatter(y=testdays6avgs,x=testdays5avgs,mode='markers',name='0.67v0.50',text=testdays6avgs.index)
traceB = go.Scatter(y=testdays7avgs,x=testdays5avgs,mode='markers',name='0.75v0.50',text=testdays7avgs.index)
traceC = go.Scatter(y=testdays6avgs,x=testdays7avgs,mode='markers',name='0.67v0.75',text=testdays6avgs.index)

datumavgs = [traceA, traceB, traceC]
figavg = go.Figure(data=datumavgs)
plot_url2 = py.plot(figavg, filename='cross-ratio performance averages ALL (inc. reinf.)')
testdayavg6v7R, testdayavg6v7P = stats.pearsonr(testdays6avgs,testdays7avgs)
print 'testdayavg6v7R',testdayavg6v7R
print'testdayavg6v7P', testdayavg6v7P
###we see no significant relationship with individual tests but on averaged scores
### inividuals that perform well on the 0.67 ratio also perform well on 0.75
'''
#excluding reinfocement
testing_daysexc = data.loc[(data["day"]>=5)&(data["session"]<=3), ["fishName", "propTimeStim", "day", "session", "ratio"]]

testdays5exc = testing_daysexc.loc[testing_daysexc["ratio"]==0.5, ["fishName", "propTimeStim", "condition"]]
testdays6exc = testing_daysexc.loc[testing_daysexc["ratio"]==0.67, ["fishName", "propTimeStim", "condition"]]
testdays7exc = testing_daysexc.loc[testing_daysexc["ratio"]==0.75, ["fishName", "propTimeStim", "condition"]]

x1exc = testdays5exc.propTimeStim
x2exc = testdays7exc.propTimeStim

trace5exc = go.Scatter(y=testdays6exc.propTimeStim,x=x1exc,mode='markers',name='0.67v0.50',text=testdays6exc.index)
trace6exc = go.Scatter(y=testdays7exc.propTimeStim,x=x1exc,mode='markers',name='0.75v0.50',text=testdays7exc.index)
trace7exc = go.Scatter(y=testdays6exc.propTimeStim,x=x2exc,mode='markers',name='0.67v0.75',text=testdays6exc.index)

datumaexc = [trace5exc, trace6exc, trace7exc]
fig2exc = go.Figure(data=datumaexc)
plot_url3 = py.plot(fig2exc, filename='cross-ratio performance')

#exclusding reinforcenment averages
testdays5avgsexc = testdays5exc.groupby('fishName').propTimeStim.mean()
testdays6avgsexc = testdays6exc.groupby('fishName').propTimeStim.mean()
testdays7avgsexc = testdays7exc.groupby('fishName').propTimeStim.mean()

traceAexc = go.Scatter(y=testdays6avgsexc,x=testdays5avgsexc,mode='markers',name='0.67v0.50',text=testdays6avgsexc.index)
traceBexc = go.Scatter(y=testdays7avgsexc,x=testdays5avgsexc,mode='markers',name='0.75v0.50',text=testdays7avgsexc.index)
traceCexc = go.Scatter(y=testdays6avgsexc,x=testdays7avgsexc,mode='markers',name='0.67v0.75',text=testdays6avgsexc.index)

datumavgsexc = [traceAexc, traceBexc, traceCexc]
figavgexc = go.Figure(data=datumavgsexc)
plot_url4 = py.plot(figavgexc, filename='cross-ratio performance averages')
testdayavg6v7excR, testdayavg6v7excP = stats.pearsonr(testdays6avgsexc,testdays7avgsexc)
print 'testdayavg6v7excR',testdayavg6v7excR
print'testdayavg6v7excP', testdayavg6v7excP
###excluding reinforcement: we see no significant relationship with individual tests but on averaged scores
### inividuals that perform well on the 0.67 ratio also perform well on 0.75
################################
#

#
################################






'''
testing_days = data.loc[(data["day"]>=5)&(data["tank"]=='R'), ["fishName", "propTimeStim", "day", "ratio"]]

testdays5 = testing_days.loc[testing_days['ratio']==0.5, ["fishName", "propTimeStim"]]
testdays6 = testing_days.loc[testing_days['ratio']==0.67, ["fishName", "propTimeStim"]]
testdays7 = testing_days.loc[testing_days['ratio']==0.75, ["fishName", "propTimeStim"]]

x1 = testdays5.propTimeStim
x2 = testdays7.propTimeStim

trace5 = go.Scatter(y=testdays6.propTimeStim,x=x1,mode='markers',name='0.67v0.50')
trace6 = go.Scatter(y=testdays7.propTimeStim,x=x1,mode='markers',name='0.75v0.50')
trace7 = go.Scatter(y=testdays6.propTimeStim,x=x2,mode='markers',name='0.67v0.75')

datuma = [trace5, trace6, trace7]
fig2 = go.Figure(data=datuma)
plot_url1 = py.plot(fig2, filename='individual testing days across ratios')

# averages
testdays5avgs = testdays5.groupby('fishName').propTimeStim.mean()
testdays6avgs = testdays6.groupby('fishName').propTimeStim.mean()
testdays7avgs = testdays7.groupby('fishName').propTimeStim.mean()

traceA = go.Scatter(y=testdays6avgs,x=testdays5avgs,mode='markers',name='0.67v0.50')
traceB = go.Scatter(y=testdays7avgs,x=testdays5avgs,mode='markers',name='0.75v0.50')
traceC = go.Scatter(y=testdays6avgs,x=testdays7avgs,mode='markers',name='0.67v0.75')

datumavgs = [traceA, traceB, traceC]
figavg = go.Figure(data=datumavgs)
plot_url2 = py.plot(figavg, filename='average performancea across ratios')
testdayavg6v7R, testdayavg6v7P = stats.pearsonr(testdays6avgs,testdays7avgs)
print 'testdayavg6v7R',testdayavg6v7R
print'testdayavg6v7P', testdayavg6v7P
# we see no significant relationship with individual tests but on averaged scores
### inividuals that perform well on the 0.67 ratio also perform well on 0.75


'''







'''

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
