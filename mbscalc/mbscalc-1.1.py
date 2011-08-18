import cgi
import urllib, urllib2
import csv

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
    def get(self):
        useremail = users.get_current_user().email()
        if ('@chilmarkhill.com' in useremail or
            useremail == 'jake01@gmail.com' or
            useremail == 'alexhsu92@gmail.com' or
            useremail == 'broncos24@gmail.com'):
            self.response.out.write('''
              <html>
                <head>
                <title>Home</title>
                <style type="text/css">
                body {font-family:arial}
                </style>
                </head>
                <body>
                    <p style="text-align:right;"><a href="'''+users.create_logout_url("/")+'''">Sign Out</a></p>
                    <h1 style="text-align:center;">Utilities</h1>
                    <p style="text-align:center;">
                    <a href="/calculator">MBS Calculator</a><br /><br />
                    <a href="/grapher">Cash Flow Grapher</a><br /><br />
                    <a href="/price">CUSIP Price Finder</a><br /><br />
                    </p>
                </body>
            </html>''')
        else:
            self.response.out.write('''<html><head><title>Invalid Login</title>
                                        <script language="javascript">
                                        alert('User Access Denied');
                                        location.replace("'''+users.create_logout_url("/")+'''");
                                        </script></head></html>''')

class MBSCalculator(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
              <html>
                <head>
                <script language="javascript">
                function blncheck(){
                    if (document.getElementById('blnfield').checked == true){
                        document.getElementById('blntermfield').disabled = false;}
                    else {
                        document.getElementById('blntermfield').disabled = true;
                        document.getElementById('blntermfield').value = '';}}
                </script>
                <title>MBS Calculator</title>
                <style type="text/css">
                body {font-family:arial}
                </style>
                </head>
                <body>
                    <p><a href="/">Back to Home</a></p>
                    <h1 style="text-align:center;">MBS Calculator</h1>
                    <form action="/calculator" method="post">
                    <table align="center" cellpadding="10">
                    <tr><th>Current Principal ($)</th>
                    <th><input type="text" name="currprin" value="100000.00" /></th></tr>
                    <tr><th>Current WAC (%)</th>
                    <th><input type="text" name="currwac" value="5.00" /></th></tr>
                    <tr><th>Original Term (mo)</th>
                    <th><input id="origtermfield" type="text" name="origterm" value="360" /></th></tr>
                    <tr><th>Servicer Fee (bp)</th>
                    <th><input type="text" name="svcfee" value="25" /></th></tr>
                    <tr><th>CPR (%)</th>
                    <th><input type="text" name="cpr" value="2.00" /><br /></th></tr>
                    <tr><th colspan="2">Balloon Term?
                    <input id="blnfield" onclick="blncheck();" type="checkbox" name="balloon" value="True" /></th></tr>
                    <tr><th>Balloon Term (mo)</th>
                    <th><input id="blntermfield" type="text" name="blnterm" disabled /></th></tr>
                    <tr><td colspan="2"><p style="font-size:10px; text-align:center;">All enabled fields are required.<br />
                    Month entries must be an integer greater than zero.<br />Ballon Term must be less than Original Term.</p></td></tr>
                    <tr><th colspan="2"><input type="submit" value="Get Payment Calendar" /></th></tr>
                    </table>
                    </form>
                </body>
            </html>''')
    def post(self):
        currprin = float(self.request.get('currprin'))
        currwac = float(self.request.get('currwac'))/100
        monthlywac = currwac/12
        origterm = int(self.request.get('origterm'))
        svcfee = float(self.request.get('svcfee'))/10000
        cpr = float(self.request.get('cpr'))/100
        balloon = str(self.request.get('balloon'))
        if balloon == 'True':
            blnterm = int(self.request.get('blnterm'))
            check = 'checked'
            term = 'value="'+str(blnterm)+'"'
            disabled = ''
        else:
            blnterm = origterm
            check = ''
            term = ''
            disabled = 'disabled'
        self.response.out.write('''
        <html>
        <head>
        <title>Calculation Results</title>
        <style type="text/css">
        body {font-family:arial}
        </style>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript ">
        
        function blncheck(){
            if (document.getElementById('blnfield').checked == true){
                document.getElementById('blntermfield').disabled = false;}
            else {
                document.getElementById('blntermfield').disabled = true;
                document.getElementById('blntermfield').value = '';}}
                    
        google.load('visualization', '1', {packages:['table']});
        google.load('visualization', '1', {packages:['corechart']});
        google.load('visualization', '1.1', {packages:['controls']});
        google.setOnLoadCallback(drawDashboard);
        google.setOnLoadCallback(drawTable);
        google.setOnLoadCallback(drawPieChart);
        google.setOnLoadCallback(drawInputTable);
        
        var currprin = ''' + str(currprin)+ ''';
        var currwac = ''' + str(currwac) + ''';
        var monthlywac = currwac/12;
        var origterm = ''' + str(origterm) + ''';
        var svcfee = ''' + str(svcfee) + ''';
        var monthlysvcfee = (svcfee/12)*currprin
        var cpr = ''' + str(cpr) + ''';
        var balloon = ''' + "'" + balloon  + "'" + ''';
        var blnterm = ''' + str(blnterm) + ''';

        if (balloon != 'True'){
        balloon = 'False';
        blnterminput = 'N/A';}
        else {
        blnterminput = blnterm;}
        
        
        function round(var1, n)
        {
              return Math.round(var1*Math.pow(10,n)) / Math.pow(10,n);
        }

        var inputs = [currprin, currwac*100, origterm, svcfee*10000, cpr*100, balloon, blnterminput]
        
        var data = [];
        var smm = 1 - Math.pow(1 - cpr, 1 / 12);
        var month = 1;
        var wala = 1;
        var wam = origterm;
        var schedpmt = (currprin * monthlywac) / (1 - Math.pow((1 + monthlywac), (-wam)));
        var interest = currprin * monthlywac;
        var schedprin = schedpmt - interest;
        var unschedprin = currprin * smm;
        var pmt = schedprin + interest + unschedprin + monthlysvcfee;
        var netmoney = pmt;

        var netint = interest;
        var netsched = schedprin;
        var netunsched = unschedprin;

        while (month < blnterm)
        {
            data.push([month, wala, wam, round(currprin, 2), round(schedprin, 2),
                        round(unschedprin, 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
                        round(netmoney, 2)]);
            month++;
            wala++;
            wam--;
            currprin = currprin - (schedprin + unschedprin);
            schedpmt = (currprin * monthlywac) / (1 - Math.pow(1 + monthlywac, -wam));
            interest = currprin * monthlywac;
            schedprin = schedpmt - interest;
            unschedprin = currprin * smm;
            pmt = schedprin + interest + unschedprin + monthlysvcfee;
            netmoney = netmoney + pmt;

            netint = netint + interest;
            netsched = netsched + schedprin;
            netunsched = netunsched + unschedprin;
        }

        netint = netint - interest;
        netsched = netsched - schedprin;
        netunsched = netunsched - unschedprin;
        
        netmoney = netmoney - pmt;
        schedprin = currprin;
        unschedprin = 0;
        pmt = schedprin + interest + unschedprin + monthlysvcfee;
        netmoney = netmoney + pmt;
        
        netint = netint + interest;
        netsched = netsched + schedprin;
        netunsched = netunsched + unschedprin;
        
        data.push([month, wala, wam, round(currprin, 2), round(schedprin, 2),
            round(unschedprin, 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
            round(netmoney, 2)]);


        function drawInputTable()
        {
            var intable = new google.visualization.DataTable();
            intable.addColumn('number', 'Initial Principal ($)');
            intable.addColumn('number', 'WAC (%)');
            intable.addColumn('number', 'Original Term (mo)');
            intable.addColumn('number', 'Servicer Fee (bp)');
            intable.addColumn('number', 'CPR (%)');
            intable.addColumn('string', 'Balloon?');
            if (balloon == 'False'){
                intable.addColumn('string', 'Balloon Term (mo)');}
            else {
                intable.addColumn('number',' Balloon Term (mo)');}
            intable.addRows(1);
            for (var j=0;j<7;j++)
            {
                intable.setCell(0, j, inputs[j]);
            }
            
            var formatter = new google.visualization.NumberFormat();
            formatter.format(intable, 0);
            formatter.format(intable, 1);
            formatter.format(intable, 4);
            var indatatable = new google.visualization.Table(document.getElementById('inputtable_div'));
            indatatable.draw(intable);
        }

        function drawTable()
        {
            var table = new google.visualization.DataTable();
            table.addColumn('number', 'Month');
            table.addColumn('number', 'WALA');
            table.addColumn('number', 'WAM');
            table.addColumn('number', 'Principal Balance ($)');
            table.addColumn('number', 'Scheduled Principal ($)');
            table.addColumn('number', 'Unscheduled Principal ($)');
            table.addColumn('number', 'Interest ($)');
            table.addColumn('number', 'Servicer Fee ($)');
            table.addColumn('number', 'Payment ($)');
            table.addColumn('number', 'Net Money ($)');
            table.addRows(blnterm);
            for (var i=0;i<blnterm;i++)
            {
                for (var j=0;j<10;j++)
                {
                    table.setCell(i, j, data[i][j]);
                }
            }

            var formatter = new google.visualization.NumberFormat();
            formatter.format(table, 3);
            formatter.format(table, 4);
            formatter.format(table, 5);
            formatter.format(table, 6);
            formatter.format(table, 7);
            formatter.format(table, 8);
            formatter.format(table, 9);
            var datatable = new google.visualization.Table(document.getElementById('table_div'));
            datatable.draw(table, {page:'enable', pageSize:60});
        }

        function drawDashboard()
        {
            var coldata = new google.visualization.DataTable();
            coldata.addColumn('string', 'Month');
            coldata.addColumn('number', 'Scheduled Principal');
            coldata.addColumn('number', 'Unscheduled Principal');
            coldata.addColumn('number', 'Interest');
            coldata.addColumn('number', 'Servicer Fee');
            coldata.addColumn('number', 'Month Range');
            coldata.addRows(blnterm);

            for(var m=0;m<blnterm;m++)
            {
                coldata.setValue(m,0,data[m][0].toString());
                coldata.setValue(m,1,data[m][4]);
                coldata.setValue(m,2,data[m][5]);
                coldata.setValue(m,3,data[m][6]);
                coldata.setValue(m,4,data[m][7]);
                coldata.setValue(m,5,data[m][0]);
            }

            var formatter = new google.visualization.NumberFormat({prefix:'$'});
            formatter.format(coldata, 1);
            formatter.format(coldata, 2);
            formatter.format(coldata, 3);
            formatter.format(coldata, 4);
            var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));

            var rangeSlider = new google.visualization.ControlWrapper({
            controlType: 'NumberRangeFilter',
            containerId: 'numfilter_div',
            options: {filterColumnLabel: 'Month Range'}
            });
            
            var columnChart = new google.visualization.ChartWrapper({
            chartType: 'ColumnChart',
            containerId: 'colchart_div',
            options: {isStacked:true, width:1500, height:700, title:'Monthly Cash Flow',
                        hAxis:{title:'Month'}, legend:'top', vAxis:{title:'Payment', format:'$#,###'}},
            view: {columns:[0, 1, 2, 3, 4]}
            });

            dashboard.bind(rangeSlider, columnChart);
            dashboard.draw(coldata)
        }

        function drawPieChart()
        {
            var piedata = new google.visualization.DataTable();
            piedata.addColumn('string', 'Payment Type');
            piedata.addColumn('number', 'Cash Amount');
            piedata.addRows(4);
            piedata.setValue(0,0,'Scheduled Principal');
            piedata.setValue(1,0,'Unscheduled Principal');
            piedata.setValue(2,0,'Interest');
            piedata.setValue(3,0,'Servicer Fee');
            piedata.setValue(0,1,round(netsched, 2));
            piedata.setValue(1,1,round(netunsched, 2));
            piedata.setValue(2,1,round(netint, 2));
            piedata.setValue(3,1,round(monthlysvcfee*blnterm, 2));

            var formatter = new google.visualization.NumberFormat({prefix:'$'});
            formatter.format(piedata, 1);
            var piechart = new google.visualization.PieChart(document.getElementById('piechart_div'));
            piechart.draw(piedata, {height:700, width:700, legend:'top', title:'Proportion of Net Money', is3D:true});
        }
    </script>
    </head>
    <body>
    <p><a href="/">Back to Home</a></p>
    <h1 style="text-align:center;">MBS Calculator</h1>      
    <form name="f1" action="/calculator" method="post">
        <table align="center" cellpadding="10">
            <tr><th>Current Principal ($)</th>
            <th><input type="text" name="currprin" value="'''+("%.2f" % currprin)+'''" /></th></tr>
            <tr><th>Current WAC (%)</th>
            <th><input type="text" name="currwac" value="'''+("%.2f" % (currwac*100))+'''" /></th></tr>
            <tr><th>Original Term (mo)</th>
            <th><input id="origtermfield" type="text" name="origterm" value="'''+str(origterm)+'''"/></th></tr>
            <tr><th>Servicer Fee (bp)</th>
            <th><input type="text" name="svcfee" value="'''+("%.0f" % (svcfee*10000))+'''"/></th></tr>
            <tr><th>CPR (%)</th>
            <th><input type="text" name="cpr" value="'''+("%.2f" % (cpr*100))+'''"/><br /></th></tr>
            <tr><th colspan="2">Balloon Term?
            <input id="blnfield" onclick="blncheck();" type="checkbox" name="balloon" value="True" '''+check+''' /></th></tr>
            <tr><th>Balloon Term (mo)</th>
            <th><input id="blntermfield" type="text" name="blnterm" '''+term+disabled+'''/></th></tr>
            <tr><td colspan="2"><p style="font-size:10px; text-align:center;">All enabled fields are required.<br />
            Month entries must be an integer greater than zero.<br />Ballon Term must be less than Original Term.</p></td></tr>
            <tr><th colspan="2"><input type="submit" value="Get Payment Calendar"></th></tr>
        </table>
    </form>
    <br /><hr />
    <h1>Results</h1>
    <a href="#outputdata">Output Data</a><br />
    <a href="#columnchart">Time Series Payment Chart</a><br />
    <a href="#piechart">Net Money Breakdown Chart</a><br />
    <h2>Input Data</h2>
    <div id="inputtable_div"></div><br />
    <a name="outputdata"><a href="#top">Back to Top</a></a>
    <h2>Monthly Cash Flow</h2>
    <div id="table_div"></div><br />
    <a name="columnchart"><a href="#top">Back to Top</a></a>
    <h2>Time Chart of Cash Flow</h2>
    <div id="dashboard_div">
        <div id="numfilter_div"></div>
        <div id="colchart_div"></div></div><br />
    <a name="piechart"><a href="#top">Back to Top</a></a>
    <h2>Net Money Breakdown</h2>
    <div id="piechart_div"></div>
    </body>
    </html>
    ''')
        
class CashFlowGrapher(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
              <html>
                <head>
                <script language="javascript">
                function filecheck(){
                    if (document.getElementById('uploadfield').checked == true){
                        document.getElementById('filefield').disabled = false;
                        document.getElementById('inputdatafield').disabled = true;}
                    else {
                        document.getElementById('filefield').disabled = true;
                        document.getElementById('inputdatafield').disabled = false;}}
                </script>
                <title>Cash Flow Grapher</title>
                <style type="text/css">
                body {font-family:arial}
                </style>
                </head>
                <body>
                    <p><a href="/">Back to Home</a></p>
                    <h1 style="text-align:center;">Cash Flow Grapher</h1>
                    <form action="/grapher" enctype="multipart/form-data" method="post">
                    <table align="center" cellpadding="10">
                    <tr><th>Input Data<br />(date, principal, interest)</th><th><textarea id="inputdatafield" name="inputdata" rows="10" cols="50">01/01/11, 120, 10
02/01/11, 125, 15
03/01/11, 150, 20
04/01/11, 155, 20
05/01/11, 140, 20
06/01/11, 120, 5
07/01/11, 115, 5
08/01/11, 115, 0
09/01/11, 130, 15
10/01/11, 135, 15</textarea></th></tr>
                    <tr><td colspan="2"><p style="font-size:10px; text-align:center;">Every line requires all three values separated by commas. Enter 0 if there is no principal and/or interest.<br />
                    Make sure there is no extra empty line at end of dataset.</p></td></tr>
                    <tr><th>Upload CSV File <input id="uploadfield" onclick="filecheck();" type="checkbox" name="upload" value="True" /></th>
                        <th><input id="filefield" type="file" name="csv" disabled /></th></tr>
                    <tr><td colspan="2"><p style="font-size:10px; text-align:center;">Must be a CSV file with three columns in this order: date, principal, interest.<br />
                    Remove all headers and extra data from the file. Remove all number formatting.</p></td></tr>
                    <tr><th colspan="2"><input type="submit" value="Graph Cash Flow" /></th></tr>
                    </table>
                    </form>
                </body>
            </html>''')
    def post(self):
        if str(self.request.get('upload')) != 'True':
            check = ''
            filedisabled = 'disabled'
            inputdatadisabled = ''
            raw_data = self.request.get('inputdata')
            split_line = raw_data.split('\r\n')
            split_value = []
            for line in split_line:
                split_value.append(line.split(', '))
            data = []
            for line in split_value:
                new_line = []
                new_line.append(str(line[0]))
                new_line.append(float(line[1]))
                new_line.append(float(line[2]))
                data.append(new_line)
        else:
            check = 'checked'
            filedisabled = ''
            inputdatadisabled = 'disabled'
            csv = self.request.get('csv')
            split_line = csv.split('\r\n')[:-1]
            split_value = []
            for line in split_line:
                split_value.append(line.split(','))
            data = []
            for line in split_value:
                new_line = []
                new_line.append(line[0])
                new_line.append(float(line[1]))
                new_line.append(float(line[2]))
                data.append(new_line)
        self.response.out.write('''
        <html>
        <head>
        <title>Graphing Results</title>
        <style type="text/css">
        body {font-family:arial}
        </style>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript ">

        google.load('visualization', '1', {packages:['table']});
        google.load('visualization', '1', {packages:['corechart']});
        google.setOnLoadCallback(drawTable);
        google.setOnLoadCallback(drawColumnChart);

        var data = '''+str(data)+''';

        function drawTable()
        {
            var table = new google.visualization.DataTable();
            table.addColumn('string', 'Date');
            table.addColumn('number', 'Principal ($)');
            table.addColumn('number', 'Interest ($)');
            table.addRows(data.length);
            for (var i=0;i<data.length;i++){
                table.setCell(i, 0, data[i][0]);
                table.setCell(i, 1, data[i][1]);
                table.setCell(i, 2, data[i][2]);}
            
            var formatter = new google.visualization.NumberFormat();
            formatter.format(table, 1);
            formatter.format(table, 2);
            var datatable = new google.visualization.Table(document.getElementById('table_div'));
            datatable.draw(table, {width:400, page:'enable', pageSize:60});
        }


        function drawColumnChart()
        {
            var coldata = new google.visualization.DataTable();
            coldata.addColumn('string', 'Date');
            coldata.addColumn('number', 'Principal');
            coldata.addColumn('number', 'Interest');
            coldata.addRows(data.length);
            for (var i=0;i<data.length;i++){
                coldata.setValue(i, 0, data[i][0]);
                coldata.setValue(i, 1, data[i][1]);
                coldata.setValue(i, 2, data[i][2]);}
                
            var formatter = new google.visualization.NumberFormat({prefix:'$'});
            formatter.format(coldata, 1);
            formatter.format(coldata, 2);
            var columnchart = new google.visualization.ColumnChart(document.getElementById('columnchart_div'));
            columnchart.draw(coldata, {width:1500, height:700, title:'Cash Flow', isStacked:true,
                                hAxis:{title:'Date'}, legend:'top', vAxis:{title:'Payment', format:'$#,###'}})
        }

        function filecheck(){
            if (document.getElementById('uploadfield').checked == true){
                document.getElementById('filefield').disabled = false;
                document.getElementById('inputdatafield').disabled = true;}
            else {
                document.getElementById('filefield').disabled = true;
                document.getElementById('inputdatafield').disabled = false;}}
        </script>
        </head>
        
        <body>
        <p><a href="/">Back to Home</a></p>
        <h1 style="text-align:center;">Cash Flow Grapher</h1>
        <form action="/grapher" enctype="multipart/form-data" method="post">
        <table align="center" cellpadding="10">
        <tr><th>Input Data<br />(date, principal, interest)</th><th><textarea id="inputdatafield" name="inputdata" rows="10" cols="50" '''+inputdatadisabled+'''>'''+self.request.get('inputdata')+'''</textarea></th></tr>
        <tr><td colspan="2"><p style="font-size:10px; text-align:center;">Every line requires all three values separated by commas. Enter 0 if there is no principal and/or interest.<br />
        Make sure there is no extra empty line at end of dataset.</p></td></tr>
        <tr><th>Upload CSV File <input id="uploadfield" onclick="filecheck();" type="checkbox" name="upload" value="True" '''+check+''' /></th>
            <th><input id="filefield" type="file" name="csv" '''+filedisabled+''' /></th></tr>
        <tr><td colspan="2"><p style="font-size:10px; text-align:center;">Must be a CSV file with three columns in this order: date, principal, interest.<br />
        Remove all headers and extra data from the file. Remove all number formatting.</p></td></tr>
        <tr><th colspan="2"><input type="submit" value="Graph Cash Flow" /></th></tr>
        </table>
        </form>
        <br /><hr />
        
        <h1>Results</h1>
        <a href="#outputdata">Output Data</a><br />
        <a href="#columnchart">Time Series Cash Flow Chart</a><br /><br />
        <a name="outputdata"><a href="#top">Back to Top</a></a>
        <h2>Cash Flow</h2>
        <div id="table_div"></div><br />
        <a name="columnchart"><a href="#top">Back to Top</a></a>
        <h2>Time Chart of Cash Flow</h2>
        <div id="columnchart_div"></div>
        </body>
        </html>
        ''')

class PriceFinder(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
              <html>
                <head>
                <title>CUSIP Price Finder</title>
                <style type="text/css">
                body {font-family:arial}
                </style>
                </head>
                <body>
                    <p><a href="/">Back to Home</a></p>
                    <h1 style="text-align:center;">CUSIP Price Finder</h1>
                    <form action="/price" method="post">
                    <table align="center" cellpadding="10">
                    <tr><th>CUSIP List</th><th><textarea name="cusiplst" rows="3" cols="50">233889AE4, 12667GWF6, 68389FBW3, 86358RE29, 743873AP6, 617463AA2</textarea></th></tr>
                    <tr><td colspan="2"><p style="font-size:10px; text-align:center;">Enter CUSIP values separated by commas.<br />Do not enter any line breaks.</p></td></tr>
                    <tr><th colspan="2"><input type="submit" value="Find Price" /></th></tr>
                    </table>
                    </form>
                </body>
            </html>''')
    def post(self):
        cusip_input = self.request.get('cusiplst')
        split_input = cusip_input.split(', ')
        raw_data = []
        for cusip in split_input:
            raw_data.append(str(cusip))
        def getpx(cusip):
            url = 'http://fixedincome.fidelity.com/fi/FIBondAnalytics?displayFormat=TABLE&preferenceName=&cusip='+cusip
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            post = urllib.urlencode({'iagree':'Agree', 'User-Agent':user_agent})
            raw_data = urllib2.urlopen(url, post)
            html = raw_data.read()
            split1 = html.split('Third Party Price</a>\n\t\t\t\t\t</th>\n\t\t\t\t   \t<td>\n\t\t\t\t   \t\t')
            if len(split1) != 2:
                return 'ERROR: CANNOT FIND CUSIP'
            split2 = split1[1].split('\n')
            if split2[0] == '--':
                return 'NO AVAILABLE PRICE'
            else:
                px = split2[0]
            return px
        def pxfinder(cusiplst):
            pxmat = []
            for cusip in cusiplst:
                pxmat.append([cusip, getpx(cusip)])
            return pxmat
        data = pxfinder(raw_data)
        self.response.out.write('''
            <html>
                <head>
                <title>Pricing Results</title>
                <style type="text/css">
                body {font-family:arial}
                </style>
                <script type="text/javascript" src="https://www.google.com/jsapi"></script>
                <script type="text/javascript ">

                google.load('visualization', '1', {packages:['table']});
                google.load('visualization', '1', {packages:['corechart']});
                google.setOnLoadCallback(drawTable);

                var data = '''+str(data)+''';

                function drawTable()
                {
                    var table = new google.visualization.DataTable();
                    table.addColumn('string', 'CUSIP');
                    table.addColumn('string', 'Price');
                    table.addRows(data.length);
                    for (var i=0;i<data.length;i++){
                        table.setCell(i, 0, data[i][0]);
                        table.setCell(i, 1, data[i][1]);}
                    
                    var datatable = new google.visualization.Table(document.getElementById('table_div'));
                    datatable.draw(table, {width:300});
                }
                
                </script>
                </head>
                
                <body>
                    <p><a href="/">Back to Home</a></p>
                    <h1 style="text-align:center;">CUSIP Price Finder</h1>
                    <form action="/price" method="post">
                    <table align="center" cellpadding="10">
                    <tr><th>CUSIP List</th><th><textarea name="cusiplst" rows="3" cols="50">'''+self.request.get('cusiplst')+'''</textarea></th></tr>
                    <tr><td colspan="2"><p style="font-size:10px; text-align:center;">Enter CUSIP values separated by commas.<br />Do not enter any line breaks.</p></td></tr>
                    <tr><th colspan="2"><input type="submit" value="Find Price" /></th></tr>
                    </table>
                    </form>
                    <br /><hr />

                    <h1>Results</h1>
                    <h2>Price Data</h2>
                    <div id="table_div"></div>
                </body>
            </html>''')
                

application = webapp.WSGIApplication([('/', MainPage), ('/calculator', MBSCalculator), ('/grapher', CashFlowGrapher), ('/price', PriceFinder)], debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
