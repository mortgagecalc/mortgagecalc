currprin = float(raw_input('Current Principal ($): '))
currwac = float(raw_input('Current WAC (%): '))/100
monthlywac = currwac/12
origterm = int(raw_input('Original Term (mo): '))
svcfee = float(raw_input('Servicer Fee (bp): '))/10000
monthlysvcfee = (svcfee/12)*currprin
vpr = float(raw_input('VPR (%): '))/100
cdr = float(raw_input('CDR (%): '))/100
vprsmm = 1 - (1 - vpr)**(1./12)
cdrsmm = 1 - (1 - cdr)**(1./12)
sev = float(raw_input('Severity (%): '))/100
cdrlag = int(raw_input('CDR Lag (mo): '))
balloon = raw_input('Balloon? (True or False): ')

while balloon == 'True':
    try:
        blnterm = int(raw_input('Balloon Term: '))
        break
    except blnterm > origterm:
        print 'Error: Balloon Term greater than Original Term.'
else:
    blnterm = origterm

inputs = [['Current Principal ($)', 'Current WAC (%)', 'Original Term (mo)',
           'Servicer Fee (bp)', 'VPR (%)', 'CDR (%)', 'Severity (%)',
           'CDR Lag (mo)', 'Balloon?', 'Balloon Term'],
          [currprin, currwac*100, origterm, svcfee, vpr*100, cdr*100, sev*100,
           cdrlag, balloon]]
if balloon == 'True':
    inputs[1].append(blnterm)
else:
    inputs[1].append('N/A')

data = []
month = 1
wala = 1
wam = origterm
vprunschedprin = currprin * vprsmm

if (cdrlag == 0):
    cdrunschedprin = currprin * cdrsmm * (1 - sev)
else:
    cdrunschedprin = 0

totunschedprin = vprunschedprin + cdrunschedprin

if (cdrlag == 0):
    lossprin = currprin * cdrsmm * sev
else:
    lossprin = 0

schedpmt = (currprin * monthlywac) / (1 - (1 + monthlywac)**(-wam))
interest = currprin * monthlywac
schedprin = schedpmt - interest
currprin = currprin - (totunschedprin + schedprin)
pmt = schedprin + interest + vprunschedprin + monthlysvcfee
netmoney = pmt

data.append([month, wala, wam, round(currprin, 2), round(schedprin, 2), round(vprunschedprin, 2), round(cdrunschedprin, 2),
    round(totunschedprin, 2), round(-(lossprin), 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
    round(netmoney, 2)])

netint = interest
netsched = schedprin
netvprunsched = vprunschedprin
netcdrunsched = cdrunschedprin
netloss = lossprin

while (month < cdrlag):
    month += 1
    wala += 1
    wam -= 1
    vprunschedprin = currprin * vprsmm
    totunschedprin = vprunschedprin + cdrunschedprin
    schedpmt = (currprin * monthlywac) / (1 - (1 + monthlywac)**(-wam))
    interest = currprin * monthlywac
    schedprin = schedpmt - interest
    currprin = currprin - (totunschedprin + schedprin)
    pmt = schedprin + interest + totunschedprin + monthlysvcfee
    netmoney = netmoney + pmt
    
    data.append([month, wala, wam, round(currprin, 2), round(schedprin, 2), round(vprunschedprin, 2), round(cdrunschedprin, 2),
        round(totunschedprin, 2), round(-(lossprin), 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
        round(netmoney, 2)])
        
    netint = netint + interest
    netsched = netsched + schedprin
    netvprunsched = netvprunsched + vprunschedprin

while (month < (blnterm - 1)):
    month += 1
    wala += 1
    wam -= 1
    vprunschedprin = currprin * vprsmm
    cdrunschedprin = currprin * cdrsmm * (1 - sev)
    lossprin = currprin * cdrsmm * sev
    totunschedprin = vprunschedprin + cdrunschedprin
    currprin = currprin - (cdrunschedprin + lossprin)
    schedpmt = (currprin * monthlywac) / (1 - (1 + monthlywac)**(-wam))
    interest = currprin * monthlywac
    schedprin = schedpmt - interest
    currprin = currprin - (vprunschedprin + schedprin)
    pmt = schedprin + interest + totunschedprin + monthlysvcfee
    netmoney = netmoney + pmt

    data.append([month, wala, wam, round(currprin, 2), round(schedprin, 2), round(vprunschedprin, 2), round(cdrunschedprin, 2),
                round(totunschedprin, 2), round(-(lossprin), 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
                round(netmoney, 2)]);
                
    netint = netint + interest
    netsched = netsched + schedprin
    netvprunsched = netvprunsched + vprunschedprin
    netcdrunsched = netcdrunsched + cdrunschedprin
    netloss = netloss + lossprin

month += 1
wala += 1
wam -= 1
vprunschedprin = 0
cdrunschedprin = currprin * cdrsmm * (1 - sev)
lossprin = currprin * cdrsmm * sev
totunschedprin = vprunschedprin + cdrunschedprin
currprin = currprin - (cdrunschedprin + lossprin)
interest = currprin * monthlywac
schedprin = currprin
currprin = currprin - (vprunschedprin + schedprin)
pmt = schedprin + interest + totunschedprin + monthlysvcfee
netmoney = netmoney + pmt

data.append([month, wala, wam, round(currprin, 2), round(schedprin, 2), round(vprunschedprin, 2), round(cdrunschedprin, 2),
    round(totunschedprin, 2), round(-(lossprin), 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
    round(netmoney, 2)]);
        
netint = netint + interest
netsched = netsched + schedprin
netvprunsched = netvprunsched + vprunschedprin
netcdrunsched = netcdrunsched + cdrunschedprin
netloss = netloss + lossprin

headers = ['Month', 'WALA', 'WAM', 'Principal Balance ($)', 'Scheduled Principal ($)', 'Unscheduled VPR ($)',
           'Unscheduled CDR ($)', 'Unscheduled Principal Total ($)', 'Principal Loss ($)', 'Interest ($)',
           'Servicer Fee ($)', 'Payment ($)', 'Net Money ($)']
print headers
for month in data:
    print month

export = raw_input('Export data to CSV file? (Yes or No): ')
if export == 'Yes':
    import csv
    datawriter = csv.writer(open('mbscalc.csv', 'wb'))
    datawriter.writerow(['Input Data'])
    for row in inputs:
        datawriter.writerow(row)
    datawriter.writerows([[],['Output Data']])
    datawriter.writerow(headers)
    for month in data:
        datawriter.writerow(month)
    print 'Export complete.'


