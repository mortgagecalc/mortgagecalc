##Authors: Alex Hsu, James Feng
##Date: August 19, 2011
##
##Reads daily close prices for a given ticker in a given range of dates. Computes
##the 10-day RSI and indicates long when the RSI climbs from below a benchmark to
##above another benchmark (currently set at 30 and 70, respectively). Likewise,
##indicates short when the RSI falls from a benchmark to below another benchmark
##(also set at 70 and 30, respectively). This file reads price data from Yahoo
##Finance. 

# uses QSTK, matplotlib, pandas, and pylab libraries
import qstkutil.dateutil as du
import qstkutil.tsutil as tsu
import qstkutil.DataAccess as da
import matplotlib.pyplot as plt
import pandas
from qstkutil import tsutil as tsu
from pylab import *

import csv
import datetime
import numpy as np
import math
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager


def relative_strength(prices, n):
    """
    compute the n period relative strength indicator
    http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    http://www.investopedia.com/terms/r/rsi.asp
    """

    deltas = np.diff(prices)
    seed = deltas[:n+1] # takes the last 1 price differences? 12 market days?
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi


# preparing data
startdate = datetime.date(2006,1,1)
today = enddate = datetime.date.today()
ticker = 'GS'

fh = finance.fetch_historical_yahoo(ticker,startdate,today) # a numpy record array with fields: date, open, high, low, close, volume, adj_close
r  = mlab.csv2rec(fh); fh.close()
r.sort()

dates = r.date[9:]
px = r.adj_close
prices = px[9:]
rsi = relative_strength(px, 10)[9:]

dtcount = 0
pxdict = {}
for date in dates:
    pxdict[date] = prices[dtcount]
    dtcount = dtcount + 1


# alloc and daily returns
allocmat = {}
returnsmat = {}
count = 1
previousrsi = rsi[0]

allocmat[dates[0]] = [0.,1.]
returnsmat[dates[0]] = 0

# alloc for all other days
for i in rsi[1:]:
    if previousrsi <= 30 and i >= 50:
        allocmat[dates[count]] = [1.,0.]
        previousrsi = i
        returnsmat[dates[count]] = 0.
    elif previousrsi >= 70 and i <= 50:
        allocmat[dates[count]] = [-1.,2.]
        previousrsi = i
        returnsmat[dates[count]] = 0
    elif count != 1:
        if allocmat[dates[count-1]] == [1.,0.]:
            if allocmat[dates[count-2]] == [1.,0.]:
                allocmat[dates[count]] = [0.,1.]
                
            else:
                allocmat[dates[count]] = [1.,0.]
            returnsmat[dates[count]] = prices[count]/prices[count-1]
        elif allocmat[dates[count-1]] == [-1.,2.]:
            if allocmat[dates[count-2]] == [-1.,2.]:
                allocmat[dates[count]] = [0.,1.]
                
            else:
                allocmat[dates[count]] = [-1.,2.]
            returnsmat[dates[count]] = 2 - prices[count]/prices[count-1]
        else:
            if i <= 30 or i >= 70:
                previousrsi = i
            allocmat[dates[count]] = [0.,1.]
            returnsmat[dates[count]] = 0.
    else:
        if i <= 30 or i >= 70:
            previousrsi = i
        allocmat[dates[count]] = [0.,1.]
        returnsmat[dates[count]] = 0.
    count = count + 1


# profit and losses on each trade
plmat = {}
prvalloc = [0.,1.]
allcash = [0.,1.]
golong = [1.,0.]
goshort = [-1.,2.]
valuelst = []
for date in sorted(allocmat):
    if allocmat[date] != prvalloc:
        if prvalloc == allcash: # enter position
            if allocmat[date] == golong: # long
                valuelst = [date, 1, 'LONG']
                prvalloc = allocmat[date]
            else: # short
                valuelst = [date, 1, 'SHORT']
                prvalloc = allocmat[date]
        elif prvalloc == golong: # exit long postion
            valuelst[1] = pxdict[date] / pxdict[valuelst[0]]
            plmat[date] = valuelst
            prvalloc = allocmat[date]
        else: # exit short position
            valuelst[1] = 2 - pxdict[date] / pxdict[valuelst[0]]
            plmat[date] = valuelst
            prvalloc = allocmat[date]


# dataset calculations
def totalreturn():
    totret = 1
    for date in sorted(plmat):
       totret = plmat[date][1]*totret
    return totret

def get_dsharpe():
    returnslist = []
    for date in sorted(returnsmat):
        if returnsmat[date] != 0:
            returnslist.append(returnsmat[date]-1)
        else:
            returnslist.append(returnsmat[date])
    return np.average(returnslist)/np.std(returnslist)

def get_ysharpe():
    return get_dsharpe()*252/math.sqrt(252)


# print options
print 'exit date', 'entry date', 'return on transaction', 'transaction type'
for date in sorted(plmat):
    print date, plmat[date][0], plmat[date][1], plmat[date][2]
print ' '
print 'total return', 'daily sharpe ratio', 'yearly sharpe ratio'
print totalreturn(), get_dsharpe(), get_ysharpe()


# export options
def export():
    start = startdate.strftime('%Y-%m-%d')
    end = today.strftime('%Y-%m-%d')
    f = open('30-70 ' + ticker + ' ' + start + ' ' + end + '.csv', 'wb')
    w = csv.writer(f)
    w.writerows([['exit date','entry date','return on transaction', 'transaction type']])
    for date in sorted(plmat):
        w.writerows([[date, plmat[date][0], plmat[date][1], plmat[date][2]]])
    w.writerows([[]])
    w.writerows([['total return','daily sharpe ratio','yearly sharpe ratio']])
    w.writerows([[totalreturn(), get_dsharpe(), get_ysharpe()]])
    print 'Export complete.'

ex = raw_input('Export to CSV? (True or False): ')
if ex == 'True':
    export()
