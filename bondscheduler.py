##Authors: Alex Hsu, James Feng
##Date: August 18, 2011
##
##Securities library with an assortment of functions. 

import csv
import math
from datetime import datetime, time, date, timedelta

# Open and read .csv with securities information (see wiki for the .csv's)
data = csv.reader(open('pfd-list1.csv', 'rb'))
mydata = []
for row in data:    
    mydata.append(row)
header = mydata[0]
values = mydata[1:]

# Defines secur, a dictionary of dictionaries. Keys of outside dictionary
# are CUSIPs, and values of outside dictionary are also dictionaries. Keys of
# inside dictionaries are column headers (Cpn, AnnAmt, Freq, etc.) and values
# are the corresponding data for each particular CUSIP. 
secur = {}
for row in values:
    entries = {}
    for num in range(1, len(row)):
        entries[header[num]] = row[num]
    secur[row[0]] = entries

# Grab data from given CUSIP 
def tkr(cusip):
    return secur[cusip]['Tkr']
def name(cusip):
    return secur[cusip]['Name']
def ex(cusip):
    return secur[cusip]['Ex']
def issuedate(cusip):
    return datetime.strptime(secur[cusip]['IssueDate'], "%m/%d/%Y")
def cpn(cusip):
    return float(secur[cusip]['Cpn'])/100
def annamt(cusip):
    return float(secur[cusip]['AnnAmt'])
def freq(cusip):
    return int(secur[cusip]['Freq'])
def matpx(cusip):
    return float(secur[cusip]['MatPx'])
def callpx(cusip):
    return float(secur[cusip]['CallPx'])
def calldt(cusip):
    return datetime.strptime(secur[cusip]['CallDt'], "%m/%d/%Y")
def matdt(cusip):
    return datetime.strptime(secur[cusip]['MatDt'], "%m/%d/%Y")
def mdy(cusip):
    return secur[cusip]['Mdy']
def snp(cusip):
    return secur[cusip]['SnP']
def ftch(cusip):
    return secur[cusip]['Ftch']
def ratdt(cusip):
    return datetime.strptime(secur[cusip]['RatDt'], "%m/%d/%Y")
def paydates(cusip):
    if freq(cusip) == 12:
        return datetime.strptime(secur[cusip]['Paydates'], "%d")
    else:
        return [datetime.strptime(date, "%m/%d") for date in secur[cusip]['Paydates'].split('-')]
def origf(cusip):
    return float(secur[cusip]['OrigF'])
def currf(cusip):
    return float(secur[cusip]['CurrF'])

#Datetime object for current time
NOW = datetime.now()

#Takes CUSIP and date and returns the closest paydate after that date for
#the CUSIP 
def get_closest_paydate(cusip, date):
    daysdates = {}
    if freq(cusip) == 12:
        withyear = paydates(cusip).replace(year=date.year)
        if withyear.day > date.day:
            withmonth = withyear.replace(month=date.month)
        else:
            if date.month == 12:
                withmonth = withyear.replace(month=1).replace(year=withyear.year+1)
            else:
                withmonth = withyear.replace(month=date.month+1)
        daysdates[(withmonth - date).days] = withmonth       
    else:
        for day in paydates(cusip):
            withyear = day.replace(year=date.year)
            daysdates[(withyear - date).days] = withyear  
    positivechecker = 0
    for key in daysdates.keys():
        if key >= 0:
            positivechecker = 1
    smallestpositive = float("inf")
    largestnegative = 0
    if positivechecker == 1:
        for key in daysdates.keys():
            if key < smallestpositive and key >= 0:
                smallestpositive = key
    else:
        for key in daysdates.keys():
            if key < largestnegative:
                largestnegative = key
    if largestnegative == 0:
        return daysdates[smallestpositive]
    else:
        return daysdates[largestnegative].replace(year=date.year+1)

#Returns a dictionary of closest paydates for all CUSIPs in .csv.
#Keys are CUSIPs and values are closest paydates.
def get_closest_paydate_dict():
    closestpaydate = {}
    for cusip in secur.keys():
       closestpaydate[cusip] = get_closest_paydate(cusip, NOW)
    return closestpaydate
##    print 'cusip, closest paydate from today'
##    for cusip in sorted(closestpaydate):
##        print cusip, closestpaydate[cusip]

#Returns dictionary of all paydates for all CUSIPs in .csv.
#Keys are CUSIPs and values are lists with all paydates
def get_all_paydates_dict():
    allpaydates = {}
    for cusip in secur.keys():
        securpaydates = []
        maturedate = matdt(cusip)
        closest = get_closest_paydate(cusip, issuedate(cusip))
        now = closest
        while closest < maturedate:
            securpaydates.append(closest)
            now = closest.replace(day=closest.day+1)
            closest = get_closest_paydate(cusip, now)
        securpaydates.append(maturedate)
        allpaydates[cusip] = securpaydates
    return allpaydates
##    for cusip in sorted(allpaydates):
##        print cusip, 'all paydates from issue to maturity:'
##        for date in allpaydates[cusip]:
##            print date

#Returns dictionary of all interest payments for a given CUSIP and number of shares.
#Keys are dates and values are lists of interest and principal payments.
#Assumes that principal payments are zero. 
def get_payments(cusip, shares):
    allpaydates = get_all_paydates_dict()
    pmtdict = {}
    pmt = shares*(annamt(cusip)/freq(cusip))
    for date in allpaydates[cusip]:
        pmtdict[date] = [pmt, 0]
    pmtdict[allpaydates[cusip][len(allpaydates[cusip])-1]] = [pmt, matpx(cusip)*shares]
    return pmtdict
##    print 'date, interest, principal'
##    for date in sorted(pmtdict):
##        print date, pmtdict[date][0], pmtdict[date][1]

#Takes inputs of desired cashflow and date before which portfolio finishes
#payments. Function generates numcomb number of portfolio combinations that
#satisfy the parameter criteria.
#NOTE: Depending on size of .csv file, there could potentially be millions
#of different portfolio combinations. This function only returns the first n
#(numcomb) combinations from the leftmost branch of all possible combinations.
#Out of the returned combinations, the optimal portfolio is the cheapest one.
#(Need another function that returns the cheapest)
def get_port_comb(cshflw, enddate, numcomb):
    cusiplst = secur.keys()
    pmtcal = {}
    comblst = []   
    def portblder(dataset):
        pmtcal.clear()
        monthchecker = [0]*12
        def checkmonth(cusip):
            for date in paydates(cusip):
                if monthchecker[date.month-1]:
                    return False
              
                else:
                    return True
        for cusip in dataset:
            if all(monthchecker):
                get_port_descrip()
                return True
            else:
                if freq(cusip) != 12 and matdt(cusip) > enddate:
                    if checkmonth(cusip):
                        for date in paydates(cusip):
                            pmtcal[date.month] = cusip
                            monthchecker[date.month-1] = 1 
    def get_port_descrip():    
        totalcost = 0
        cusiptracker = []
        valuesdict = {}
        for month in pmtcal.keys():
            cusip = pmtcal[month]
            if cusiptracker.count(cusip) == 0:
                shares = math.ceil(cshflw*freq(cusip)/annamt(cusip))
                months = [date.month for date in paydates(cusip)]
                income = shares*annamt(cusip)/freq(cusip)
                price = matpx(cusip)*shares
                totalcost = totalcost+price
                cusiptracker.append(cusip)
                valuesdict[cusip] = [months,shares,income,price]
        comblst.append([valuesdict, totalcost])
    def combblder(dataset, numcomb):
        if portblder(dataset):
            pmtcalcusips = []
            for month in pmtcal.keys():
                if pmtcalcusips.count(pmtcal[month]) == 0:
                    pmtcalcusips.append(pmtcal[month])
            for cusip in pmtcalcusips:
                if len(comblst)<numcomb:
                    newdata = []
                    for data in dataset:
                        newdata.append(data)
                    newdata.remove(cusip)
                    combblder(newdata, numcomb/2)
                else:
                    break
    combblder(cusiplst, numcomb)
    comblst.sort()
    for comb in comblst:
        print comb
    print len(comblst)      

#Creates a portfolio dictionary with given portfolio worth and desired percent
#of portfolio returned per year. Keys are CUSIPs and values are lists with
#number of shares, maturity date, and maturity price. 
def get_yearly_payments(portworth, annpercent):
    pmtdict = {}
    yeardict = {}
    consecyears = math.ceil(100/float(annpercent))
    for year in range(int(NOW.year+1), int(NOW.year+consecyears+1)):
        cusiplist = []
        for cusip in secur.keys():
            if matdt(cusip).year == year:
                cusiplist.append(cusip)
        yeardict[year] = cusiplist
        if not yeardict[year]:
            return 'Not possible.'
    pmtamt = (float(portworth)*annpercent)/100
    for year in sorted(yeardict.keys())[:-1]:
        numbonds = len(yeardict[year])
        for cusip in yeardict[year]:
            matprice = matpx(cusip)
            shares = (pmtamt/numbonds)/matprice
            pmtdict[cusip] = [shares, matdt(cusip), matprice*shares]
    for cusip in yeardict[sorted(yeardict.keys())[-1]]:
        numbonds = len(yeardict[sorted(yeardict.keys())[-1]])
        matprice = matpx(cusip)
        modamt = portworth - pmtamt*(consecyears-1)
        shares = (modamt/numbonds)/matprice
        pmtdict[cusip] = [shares, matdt(cusip), matprice*shares]
    return pmtdict
