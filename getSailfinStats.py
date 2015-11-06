__author__ = 'ian'
import pandas as pd
import numpy as np
from scipy import stats
import sys
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
import pylab

#import data
data = pd.read_csv('data/masterdataNumerosity_sailfins.csv')
#add high/low condition
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
#stats.probplot(tankRight.propTimeEdge, dist="norm", plot=pylab)
#stats.probplot(tankLeft.propTimeEdge, dist="norm", plot=pylab)
#pylab.show()
sidebiasLeftLeftvLeftRightU, sidebiasLeftLeftvLeftRightP = stats.mannwhitneyu(tankLeft.propTimeLeft,tankLeft.propTimeRight)
sidebiasLeftLeftvRightRightU, sidebiasLeftLeftvRightRightP = stats.mannwhitneyu(tankLeft.propTimeLeft,tankRight.propTimeRight)
fig1 = go.Figure(data=datum)
plot_url = py.plot(fig1, filename='tank side bias')
print 'sidebiasanovaF: ', sidebiasanovaF
print 'sidebiasanovaP: ', sidebiasanovaP
print 'sidebiasLeftLeftvLeftRightU', sidebiasLeftLeftvLeftRightU
print 'sidebiasLeftLeftvLeftRightP', sidebiasLeftLeftvLeftRightP
###we see a bias in the left tank towards the right side/away from left side
### is this side bias correlated with thigmotaxis (our measure of stress)?
##############################
#
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
stressbytankU, stressbytankP = stats.mannwhitneyu(righttank.propTimeEdge, lefttank.propTimeEdge)
print 'stressbytankU',stressbytankU
print 'stressbytankP', stressbytankP
###stress levels are similar in both tanks
hightrainers = data.loc[data.condition=='High',['propTimeEdge']]
lowtrainers = data.loc[data.condition=='Low',['propTimeEdge']]
tr222 = go.Box(y=hightrainers.propTimeEdge,name='hightrainerstress')
tr2222 = go.Box(y=lowtrainers.propTimeEdge, name='lowtrainerstress')
stressdatahighlow = [tr222,tr2222]
stressfighl = go.Figure(data=stressdatahighlow)
stressplothl = py.plot(stressfighl, filename='stress by trained condition')
stressbytrainerU, stressbytrainerP = stats.mannwhitnyeu(hightrainers.propTimeEdge, lowtrainers.propTimeEdge)
print 'stressbytrainerT',stressbytrainerU
print 'stressbytrainerP', stressbytrainerP
###stress levels are similar across training groups
##############################
#
#
#
##############################
# performance by ratio on testing days
##excluding reinfocement
testing_daysexc = data.loc[(data["day"]>=5)&(data["session"]<=3), ["fishName", "propTimeStim", "day", "session", "ratio"]]
testdays5exc = testing_daysexc.loc[testing_daysexc["ratio"]==0.5, ["fishName", "propTimeStim"]]
testdays6exc = testing_daysexc.loc[testing_daysexc["ratio"]==0.67, ["fishName", "propTimeStim"]]
testdays7exc = testing_daysexc.loc[testing_daysexc["ratio"]==0.75, ["fishName", "propTimeStim"]]
x1exc = testdays5exc.propTimeStim
x2exc = testdays7exc.propTimeStim
trace5exc = go.Scatter(y=testdays6exc.propTimeStim,x=x1exc,mode='markers',name='0.67v0.50',text=testdays6exc.index)
trace6exc = go.Scatter(y=testdays7exc.propTimeStim,x=x1exc,mode='markers',name='0.75v0.50',text=testdays7exc.index)
trace7exc = go.Scatter(y=testdays6exc.propTimeStim,x=x2exc,mode='markers',name='0.67v0.75',text=testdays6exc.index)
datumaexc = [trace5exc, trace6exc, trace7exc]
fig2exc = go.Figure(data=datumaexc)
plot_url3 = py.plot(fig2exc, filename='cross-ratio performance')
##exclusding reinforcenment averages
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
#
##ratio performance by trained condition (high/low)
#overall
testing_dayscond = data.loc[(data["day"]>=5)&(data["session"]<=3), ["fishName", "propTimeStim", "day", "session", "ratio", "condition"]]
h_fish = testing_dayscond[testing_dayscond['condition']=='High'].propTimeStim
l_fish = testing_dayscond[testing_dayscond['condition']=='Low'].propTimeStim
tracelow = go.Box(y=h_fish,name='hightrainerTstim')
tracehigh = go.Box(y=l_fish, name='lowtrainersTstim')
performancehighlow = [tracelow, tracehigh]
highlowfig1 = go.Figure(data=performancehighlow)
highlowplot = py.plot(highlowfig1, filename='performace high vs low')
#stats.probplot(h_fish, dist="norm", plot=pylab)
#stats.probplot(l_fish, dist="norm", plot=pylab)
#pylab.show()
highlowperfU, highlowperfP = stats.mannwhitneyu(h_fish, l_fish)
print 'highlowperfU', highlowperfU
print 'highlowperfP', highlowperfP
#not a significant difference across all ratios but a TREND towards fish trained to the high side doing better
#
#0.5 ratio
testing_dayscond5 = data.loc[(data["day"]>=5)&(data["session"]<=3)&(data["ratio"]==0.5), ["fishName", "propTimeStim", "day", "session", "ratio", "condition"]]
h_fish5 = testing_dayscond5[testing_dayscond5['condition']=='High'].propTimeStim
l_fish5 = testing_dayscond5[testing_dayscond5['condition']=='Low'].propTimeStim
tracelow5 = go.Box(y=h_fish5,name='hightrainerTstim 0.5')
tracehigh5 = go.Box(y=l_fish5, name='lowtrainersTstim 0.5')
performancehighlow5 = [tracelow5, tracehigh5]
highlowfig15 = go.Figure(data=performancehighlow5)
highlowplot5 = py.plot(highlowfig15, filename='performace high vs low 0.5')
#stats.probplot(h_fish5, dist="norm", plot=pylab)
#stats.probplot(l_fish5, dist="norm", plot=pylab)
#pylab.show()
highlowperf5U, highlowperf5P = stats.mannwhitneyu(h_fish5, l_fish5)
print 'highlowperf5U', highlowperf5U
print 'highlowperf5P', highlowperf5P
#
#0.67 ratio
testing_dayscond6 = data.loc[(data["day"]>=5)&(data["session"]<=3)&(data["ratio"]==0.67), ["fishName", "propTimeStim", "day", "session", "ratio", "condition"]]
h_fish6 = testing_dayscond6[testing_dayscond6['condition']=='High'].propTimeStim
l_fish6 = testing_dayscond6[testing_dayscond6['condition']=='Low'].propTimeStim
tracelow6 = go.Box(y=h_fish6,name='hightrainerTstim 0.67')
tracehigh6 = go.Box(y=l_fish6, name='lowtrainersTstim 0.67')
performancehighlow6 = [tracelow6, tracehigh6]
highlowfig16 = go.Figure(data=performancehighlow6)
highlowplot6 = py.plot(highlowfig16, filename='performace high vs low 0.67')
#stats.probplot(h_fish6, dist="norm", plot=pylab)
#stats.probplot(l_fish6, dist="norm", plot=pylab)
#pylab.show()
highlowperf6U, highlowperf6P = stats.mannwhitneyu(h_fish6, l_fish6)
print 'highlowperf6U', highlowperf6U
print 'highlowperf6P', highlowperf6P
#
#0.75 ratio
testing_dayscond7 = data.loc[(data["day"]>=5)&(data["session"]<=3)&(data["ratio"]==0.75), ["fishName", "propTimeStim", "day", "session", "ratio", "condition"]]
h_fish7 = testing_dayscond7[testing_dayscond7['condition']=='High'].propTimeStim
l_fish7 = testing_dayscond7[testing_dayscond7['condition']=='Low'].propTimeStim
tracelow7 = go.Box(y=h_fish7,name='hightrainerTstim 0.75')
tracehigh7 = go.Box(y=l_fish7, name='lowtrainersTstim 0.75')
performancehighlow7 = [tracelow7, tracehigh7]
highlowfig17 = go.Figure(data=performancehighlow7)
highlowplot7 = py.plot(highlowfig17, filename='performace high vs low 0.75')
#stats.probplot(h_fish6, dist="norm", plot=pylab)
#stats.probplot(l_fish6, dist="norm", plot=pylab)
#pylab.show()
highlowperf7U, highlowperf7P = stats.mannwhitneyu(h_fish7, l_fish7)
print 'highlowperf7U', highlowperf7U
print 'highlowperf7P', highlowperf7P
################################
#
#
#
################################
#by sex
testingdaysfemales = data.loc[(data["day"]>=5)&(data["session"]<=3)&(data["sex"]=='F'), ["fishName", "propTimeStim", "day", "session", "ratio", "condition"]]
testingdaysmales = data.loc[(data["day"]>=5)&(data["session"]<=3)&(data["sex"]=='M'), ["fishName", "propTimeStim", "day", "session", "ratio", "condition"]]
femaleteststrace = go.Box(y=testingdaysfemales.propTimeStim,name='femaletests')
maleteststrace = go.Box(y=testingdaysmales.propTimeStim,name='maletests')
malefemaletraces = [femaleteststrace, maleteststrace]
femalemale = go.Figure(data=malefemaletraces)
fmplot = py.plot(femalemale, filename='female and male performance')
femalemaleU, femalemaleP = stats.mannwhitneyu(testingdaysfemales.propTimeStim,testingdaysmales.propTimeStim)
print 'femalemaleU', femalemaleU
print 'femalemaleP', femalemaleP

#sex by high low
highfems = testingdaysfemales[testingdaysfemales["condition"]=='High'].propTimeStim
lowfems = testingdaysfemales[testingdaysfemales["condition"]=='Low'].propTimeStim
highmales = testingdaysmales[testingdaysmales["condition"]=='High'].propTimeStim
lowmales = testingdaysmales[testingdaysmales["condition"]=='Low'].propTimeStim
tracelowfems = go.Box(y=lowfems,name='lowfemales')
tracehighfems = go.Box(y=highfems, name='highfemales')
tracelowmales = go.Box(y=lowmales,name='lowmales')
tracehighmales = go.Box(y=highmales, name='highmales')
performancehighlowfemalemale = [tracelowfems, tracehighfems, tracelowmales, tracehighmales]
femalemalehighlowfig = go.Figure(data=performancehighlowfemalemale)
fmhlplot = py.plot(femalemalehighlowfig, filename='female and male performance across training condition')

#sexbyratio
