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
            useremail == 'broncos24@gmail.com' or
            useremail == 'jcmaltmail@gmail.com'):
            self.response.out.write('''
<html>
    <head>
        <title>Chilmark Hill Utilities</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/redmond/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script>
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }
            function chilmarkhome() {window.location="http://www.chilmarkhill.com/"; }  

            $(document).ready(function() {
                $("button").button(); });
        </script>
        <style>
            a {text-decoration: none}
        </style>
    </head>
    <body>
        <p style="font-size:62.5%;"><button type="button" onclick="chilmarkhome();">Chilmark Hill Capital LLC</button><button type="button" onclick="logout();");">Sign Out</button></p>
        <h1 style="font-family:arial; text-align:center;">Chilmark Hill Utilities</h1>
        <p style="font-family:arial; text-align:center;">
        <a href="/calculator">MBS Calculator</a><br /><br />
        <a href="/grapher">Cash Flow Grapher</a><br /><br />
        <a href="/price">CUSIP Price Finder</a><br /></p><br />
        <p style="font-family:arial; font-size:10px; text-align:center;">
        Optimized for Google Chrome.<br />
        Known bugs in Mozilla Firefox.<br />
        Not supported in Internet Explorer.</p>
    </body>
</html>
        ''')
        else:
            self.response.out.write('''
<html>
    <head>
        <title>Access Denied</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/redmond/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script>
            $(document).ready(function() {
                $("#access-denied").dialog({
                    modal: true,
                    resizable: false,
                    draggable: false,
                    closeOnEscape: false,
                    open: function(event, ui) { $(".ui-dialog-titlebar-close").hide(); },
                    buttons: {"Return to Login": function() {
                        location.replace("'''+users.create_logout_url("/")+'''");
                        $( this ).dialog( "close" ); } }
                });
            });
        </script>
    </head>
    <body style="font-size:62.5%;">
        <div id="access-denied" title="Access Denied">
            <p style="text-align:center;">User Access Denied.</p>
        </div>
    </body>
</html>
        ''')

class MBSCalculator(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
<html>
    <head>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/redmond/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script language="javascript">
            function blncheck(){
                if (document.getElementById('blnfield').checked == true){
                    document.getElementById('blntermfield').disabled = false;}
                else {
                    document.getElementById('blntermfield').disabled = true;
                    document.getElementById('blntermfield').value = '';}}
        </script>
        <title>MBS Calculator</title>
        <script>
            function home() {window.location="/"; }
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }
            
            $(document).ready(function() {
                $("button").button();
                $("#accordion").accordion(); });
	</script>
    </head>
    <body style="font-size:62.5%;">
        <button type="button" onclick="home();");">Back to Home</button>
        <button type="button" onclick="logout();");">Sign Out</button>
        <div id="accordion">
            <h3><a href="#">MBS Calculator</a></h3>
            <div>
                <form name="f1" action="/calculator" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td>Current Principal ($)</td>
                        <td><input type="text" name="currprin" value="100000000.00" /></td></tr>
                        <tr><td>Current WAC (%)</td>
                        <td><input type="text" name="currwac" value="5.00" /></td></tr>
                        <tr><td>Original Term (mo)</td>
                        <td><input id="origtermfield" type="text" name="origterm" value="360"/></td></tr>
                        <tr><td>Servicer Fee (bp)</td>
                        <td><input type="text" name="svcfee" value="25"/></td></tr>
                        <tr><td>VPR (%)</td>
                        <td><input type="text" name="vpr" value="4.00"/></td></tr>
                        <tr><td>CDR (%)</td>
                        <td><input type="text" name="cdr" value="2.00"/></td></tr>
                        <tr><td>Severity (%)</td>
                        <td><input type="text" name="sev" value="30.00"/><br /></td></tr>
                        <tr><td>CDR Lag (mo)</br><p style="font-size:10px;">Month(s) before defaults begin to affect pool.</p></td>
                        <td><input type="text" name="cdrlag" value="6"/><br /></td></tr>
                        <tr><td colspan="2">Balloon Term?
                        <input id="blnfield" onclick="blncheck();" type="checkbox" name="balloon" value="True" /></td></tr>
                        <tr><td>Balloon Term (mo)</td>
                        <td><input id="blntermfield" type="text" name="blnterm" disabled /></td></tr>
                        <tr><td colspan="2"><p style="font-size:10px;">All enabled fields are required.</p></td></tr>
                        <tr><td colspan="2"><button type="submit">Get Payment Calendar</button></td></tr>
                    </table>
                </form>
            </div>
        </div>
    </body>
</html>
    ''')
    def post(self):
        currprin = float(self.request.get('currprin'))
        currwac = float(self.request.get('currwac'))/100
        monthlywac = currwac/12
        origterm = int(self.request.get('origterm'))
        svcfee = float(self.request.get('svcfee'))/10000
        vpr = float(self.request.get('vpr'))/100
        cdr = float(self.request.get('cdr'))/100
        cdrlag = int(self.request.get('cdrlag'))
        sev = float(self.request.get('sev'))/100
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
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/redmond/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript ">
            function blncheck() {
                if (document.getElementById('blnfield').checked == true) {
                    document.getElementById('blntermfield').disabled = false; }
                else {
                    document.getElementById('blntermfield').disabled = true;
                    document.getElementById('blntermfield').value = ''; } }
                    
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
            var monthlysvcfee = (svcfee/12)*currprin;
            var vpr = ''' + str(vpr) + ''';
            var cdr = ''' + str(cdr) + ''';
            var vprsmm = 1 - Math.pow(1 - vpr, 1 / 12);
            var cdrsmm = 1 - Math.pow(1 - cdr, 1 / 12);
            var sev = ''' + str(sev) + ''';
            var cdrlag = ''' + str(cdrlag) + ''';
            var balloon = ''' + "'" + balloon  + "'" + ''';
            var blnterm = ''' + str(blnterm) + ''';

            if (balloon != 'True') {
                balloon = 'False';
                blnterminput = 'N/A'; }
            else {
                blnterminput = blnterm; }


            function round(var1, n) {
                return Math.round(var1*Math.pow(10,n)) / Math.pow(10,n); }

            var inputs = [currprin, currwac*100, origterm, svcfee*10000, vpr*100, cdr*100, sev*100, cdrlag, balloon, blnterminput]

            var data = [];
            var month = 1;
            var wala = 1;
            var wam = origterm;
            var vprunschedprin = currprin * vprsmm;

            if (cdrlag == 0) {
                var cdrunschedprin = currprin * cdrsmm * (1 - sev); }
            else {
                var cdrunschedprin = 0; }

            var totunschedprin = vprunschedprin + cdrunschedprin

            if (cdrlag == 0) {
                lossprin = currprin * cdrsmm * sev; }
            else {
                var lossprin = 0; }

            var schedpmt = (currprin * monthlywac) / (1 - Math.pow((1 + monthlywac), (-wam)));
            var interest = currprin * monthlywac;
            var schedprin = schedpmt - interest;
            currprin = currprin - (totunschedprin + schedprin)
            var pmt = schedprin + interest + vprunschedprin + monthlysvcfee;
            var netmoney = pmt;

            data.push([month, wala, wam, round(currprin, 2), round(schedprin, 2), round(vprunschedprin, 2), round(cdrunschedprin, 2),
                round(totunschedprin, 2), round(-(lossprin), 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
                round(netmoney, 2)]);

            var netint = interest;
            var netsched = schedprin;
            var netvprunsched = vprunschedprin;
            var netcdrunsched = cdrunschedprin;
            var netloss = lossprin;

            while (month < cdrlag) {
                month++;
                wala++;
                wam--;
                vprunschedprin = currprin * vprsmm;
                totunschedprin = vprunschedprin + cdrunschedprin
                schedpmt = (currprin * monthlywac) / (1 - Math.pow((1 + monthlywac), (-wam)));
                interest = currprin * monthlywac;
                schedprin = schedpmt - interest;
                currprin = currprin - (totunschedprin + schedprin)
                pmt = schedprin + interest + totunschedprin + monthlysvcfee;
                netmoney = netmoney + pmt;
                
                data.push([month, wala, wam, round(currprin, 2), round(schedprin, 2), round(vprunschedprin, 2), round(cdrunschedprin, 2),
                    round(totunschedprin, 2), round(-(lossprin), 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
                    round(netmoney, 2)]);
                    
                netint = netint + interest;
                netsched = netsched + schedprin;
                netvprunsched = netvprunsched + vprunschedprin; }

            while (month < (blnterm - 1)) {
                month++;
                wala++;
                wam--;
                vprunschedprin = currprin * vprsmm;
                cdrunschedprin = currprin * cdrsmm * (1 - sev)
                lossprin = currprin * cdrsmm * sev
                totunschedprin = vprunschedprin + cdrunschedprin
                currprin = currprin - (cdrunschedprin + lossprin)
                schedpmt = (currprin * monthlywac) / (1 - Math.pow((1 + monthlywac), (-wam)));
                interest = currprin * monthlywac;
                schedprin = schedpmt - interest;
                currprin = currprin - (vprunschedprin + schedprin)
                pmt = schedprin + interest + totunschedprin + monthlysvcfee;
                netmoney = netmoney + pmt;

                data.push([month, wala, wam, round(currprin, 2), round(schedprin, 2), round(vprunschedprin, 2), round(cdrunschedprin, 2),
                            round(totunschedprin, 2), round(-(lossprin), 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
                            round(netmoney, 2)]);
                            
                netint = netint + interest;
                netsched = netsched + schedprin;
                netvprunsched = netvprunsched + vprunschedprin;
                netcdrunsched = netcdrunsched + cdrunschedprin;
                netloss = netloss + lossprin; }

            month++;
            wala++;
            wam--;
            vprunschedprin = 0
            cdrunschedprin = currprin * cdrsmm * (1 - sev)
            lossprin = currprin * cdrsmm * sev
            totunschedprin = vprunschedprin + cdrunschedprin
            currprin = currprin - (cdrunschedprin + lossprin)
            interest = currprin * monthlywac;
            schedprin = currprin;
            currprin = currprin - (vprunschedprin + schedprin)
            pmt = schedprin + interest + totunschedprin + monthlysvcfee;
            netmoney = netmoney + pmt;

            data.push([month, wala, wam, round(currprin, 2), round(schedprin, 2), round(vprunschedprin, 2), round(cdrunschedprin, 2),
                round(totunschedprin, 2), round(-(lossprin), 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
                round(netmoney, 2)]);
                    
            netint = netint + interest;
            netsched = netsched + schedprin;
            netvprunsched = netvprunsched + vprunschedprin;
            netcdrunsched = netcdrunsched + cdrunschedprin;
            netloss = netloss + lossprin;

            function drawInputTable() {
                var intable = new google.visualization.DataTable();
                intable.addColumn('number', 'Initial Principal ($)');
                intable.addColumn('number', 'WAC (%)');
                intable.addColumn('number', 'Original Term (mo)');
                intable.addColumn('number', 'Servicer Fee (bp)');
                intable.addColumn('number', 'VPR (%)');
                intable.addColumn('number', 'CDR (%)');
                intable.addColumn('number', 'Severity (%)');
                intable.addColumn('number', 'CDR Lag (mo)');
                intable.addColumn('string', 'Balloon?');
                
                if (balloon == 'False') {
                    intable.addColumn('string', 'Balloon Term (mo)'); }
                else {
                    intable.addColumn('number',' Balloon Term (mo)'); }
                    
                intable.addRows(1);
                for (var j=0;j<inputs.length;j++) {
                    intable.setCell(0, j, inputs[j]); }

                var formatter = new google.visualization.NumberFormat();
                formatter.format(intable, 0);
                formatter.format(intable, 1);
                formatter.format(intable, 4);
                formatter.format(intable, 5);
                formatter.format(intable, 6);
                
                var indatatable = new google.visualization.Table(document.getElementById('inputtable_div'));
                indatatable.draw(intable); }

            function drawTable() {
                var table = new google.visualization.DataTable();
                table.addColumn('number', 'Month');
                table.addColumn('number', 'WALA');
                table.addColumn('number', 'WAM');
                table.addColumn('number', 'Principal Balance ($)');
                table.addColumn('number', 'Scheduled Principal ($)');
                table.addColumn('number', 'Unscheduled VPR ($)');
                table.addColumn('number', 'Unscheduled CDR ($)');
                table.addColumn('number', 'Unscheduled Principal Total ($)');
                table.addColumn('number', 'Principal Loss ($)');
                table.addColumn('number', 'Interest ($)');
                table.addColumn('number', 'Servicer Fee ($)');
                table.addColumn('number', 'Payment ($)');
                table.addColumn('number', 'Net Money ($)');
                
                table.addRows(blnterm);
                for (var i=0;i<blnterm;i++) {
                    for (var j=0;j<data[0].length;j++) {
                        table.setCell(i, j, data[i][j]); } }

                var formatter = new google.visualization.NumberFormat(
                    {negativeColor: 'red', negativeParens: true});
                formatter.format(table, 3);
                formatter.format(table, 4);
                formatter.format(table, 5);
                formatter.format(table, 6);
                formatter.format(table, 7);
                formatter.format(table, 8);
                formatter.format(table, 9);
                formatter.format(table, 10);
                formatter.format(table, 11);
                formatter.format(table, 12);
                
                var datatable = new google.visualization.Table(document.getElementById('table_div'));
                datatable.draw(table, {allowHtml:true}); }

            var rangeSlider;
            var columnChart;
            function drawDashboard() {
                var coldata = new google.visualization.DataTable();
                coldata.addColumn('string', 'Month');
                coldata.addColumn('number', 'Scheduled Principal');
                coldata.addColumn('number', 'Unscheduled VPR');
                coldata.addColumn('number', 'Unscheduled CDR');
                coldata.addColumn('number', 'Interest');
                coldata.addColumn('number', 'Servicer Fee');
                coldata.addColumn('number', 'Month Range');
                
                coldata.addRows(blnterm);
                for(var m=0;m<blnterm;m++) {
                    coldata.setValue(m,0,data[m][0].toString());
                    coldata.setValue(m,1,data[m][4]);
                    coldata.setValue(m,2,data[m][5]);
                    coldata.setValue(m,3,data[m][6]);
                    coldata.setValue(m,4,data[m][9]);
                    coldata.setValue(m,5,data[m][10]);
                    coldata.setValue(m,6,data[m][0]); }

                var formatter = new google.visualization.NumberFormat({prefix:'$'});
                formatter.format(coldata, 1);
                formatter.format(coldata, 2);
                formatter.format(coldata, 3);
                formatter.format(coldata, 4);
                formatter.format(coldata, 5);
                
                var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));

                rangeSlider = new google.visualization.ControlWrapper({
                    controlType: 'NumberRangeFilter',
                    containerId: 'numfilter_div',
                    options: {filterColumnLabel: 'Month Range'} });
                        
                columnChart = new google.visualization.ChartWrapper({
                    chartType: 'ColumnChart',
                    containerId: 'colchart_div',
                    options: {isStacked:true, width:1500, height:700, title:'Monthly Cash Flow',
                        hAxis:{title:'Month'}, legend:'right', vAxis:{title:'Payment', format:'$#,###'} },
                    view: {columns:[0, 1, 2, 3, 4, 5]} });

                dashboard.bind(rangeSlider, columnChart);
                dashboard.draw(coldata); }

            function drawPieChart() {
                var piedata = new google.visualization.DataTable();
                piedata.addColumn('string', 'Payment Type');
                piedata.addColumn('number', 'Cash Amount');
                
                piedata.addRows(6);
                piedata.setValue(0,0,'Scheduled Principal');
                piedata.setValue(1,0,'Unscheduled VPR');
                piedata.setValue(2,0,'Unscheduled CDR');
                piedata.setValue(3,0,'Principal Loss');
                piedata.setValue(4,0,'Interest');
                piedata.setValue(5,0,'Servicer Fee');
                piedata.setValue(0,1,round(netsched, 2));
                piedata.setValue(1,1,round(netvprunsched, 2));
                piedata.setValue(2,1,round(netcdrunsched, 2));
                piedata.setValue(3,1,round(netloss, 2));
                piedata.setValue(4,1,round(netint, 2));
                piedata.setValue(5,1,round(monthlysvcfee*blnterm, 2));

                var formatter = new google.visualization.NumberFormat({prefix:'$'});
                formatter.format(piedata, 1);
                
                var piechart = new google.visualization.PieChart(document.getElementById('piechart_div'));
                piechart.draw(piedata, {height:700, width:1500, legend:'right', title:'Cash Breakdown', is3D:true}); }
        </script>
        <script>
            function home() {window.location="/"; }
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }
            function sliderChange(low, high) {rangeSlider.setState({'lowValue':low, 'highValue':high}); rangeSlider.draw(); }
            function chartChange(id) {
                var a = ["schedprin", "unschedvpr", "unschedcdr", "interest", "svcfee"];
                var b = [0];
                for(var i=0;i<a.length;i++) {
                    if (document.getElementById(a[i]).checked == true) {
                        b.push(i+1); } }
                if (b.length == 1) {id.checked = true; }
                else {
                columnChart.setView({columns:b});
                columnChart.draw(); } }
            
            $(document).ready(function() {
                $("#tabs").tabs();
                $("button").button();
                $("#accordion1").accordion({active: false, collapsible: true});
                $("#accordion2").accordion({collapsible: true, autoHeight: false});
                $("#categories").buttonset();
                $("#slider-range").slider({
                    range: true,
                    min: 1,
                    max: '''+str(blnterm)+''',
                    values: [1, '''+str(blnterm)+'''],
                    animate: "normal",
                    slide: function(event, ui) {$("#amount").val(ui.values[0] + " - " + ui.values[1]); sliderChange(ui.values[0], ui.values[1]);} }); 
		$("#amount").val($("#slider-range").slider("values", 0) + " - " + $("#slider-range").slider("values", 1)); });
	</script>
    </head>
    <body style="font-size:62.5%;">
        <button type="button" onclick="home();");">Back to Home</button>
        <button type="button" onclick="logout();");">Sign Out</button>
	
        <div id="accordion1">
            <h3><a href="#">MBS Calculator</a></h3>
            <div>
                <form name="f1" action="/calculator" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td>Current Principal ($)</td>
                        <td><input type="text" name="currprin" value="'''+("%.2f" % currprin)+'''" /></td></tr>
                        <tr><td>Current WAC (%)</td>
                        <td><input type="text" name="currwac" value="'''+("%.2f" % (currwac*100))+'''" /></td></tr>
                        <tr><td>Original Term (mo)</td>
                        <td><input id="origtermfield" type="text" name="origterm" value="'''+str(origterm)+'''"/></td></tr>
                        <tr><td>Servicer Fee (bp)</td>
                        <td><input type="text" name="svcfee" value="'''+("%.0f" % (svcfee*10000))+'''"/></td></tr>
                        <tr><td>VPR (%)</td>
                        <td><input type="text" name="vpr" value="'''+("%.2f" % (vpr*100))+'''"/></td></tr>
                        <tr><td>CDR (%)</td>
                        <td><input type="text" name="cdr" value="'''+("%.2f" % (cdr*100))+'''"/></td></tr>
                        <tr><td>Severity (%)</td>
                        <td><input type="text" name="sev" value="'''+("%.2f" % (sev*100))+'''"/><br /></td></tr>
                        <tr><td>CDR Lag (mo)</br><p style="font-size:10px;">Month(s) before defaults begin to affect pool.</p></td>
                        <td><input type="text" name="cdrlag" value="'''+str(cdrlag)+'''"/><br /></td></tr>
                        <tr><td colspan="2">Balloon Term?
                        <input id="blnfield" onclick="blncheck();" type="checkbox" name="balloon" value="True" '''+check+''' /></td></tr>
                        <tr><td>Balloon Term (mo)</td>
                        <td><input id="blntermfield" type="text" name="blnterm" '''+term+disabled+'''/></td></tr>
                        <tr><td colspan="2"><p style="font-size:10px;">All enabled fields are required.</p></td></tr>
                        <tr><td colspan="2"><button type="submit">Get Payment Calendar</button></td></tr>
                    </table>
                </form>
            </div>
        </div>
        <div id="accordion2">
            <h3><a href="#">Results</a></h3>
            <div>
                <div id="inputtable_div" align="center"></div><br />
                <div id="tabs">
                    <ul>
                        <li><a href="#table_div">Monthly Cash Flow</a></li>
                        <li><a href="#dashboard_div">Time Chart of Cash Flow</a></li>
                        <li><a href="#piechart_div">Cash Breakdown</a></li>
                    </ul>
                    <div id="table_div" align="center"></div>
                    <div id="dashboard_div">
                        <label for="amount" style="font-family:arial; font-size:12px;">Month Range:</label>
                        <input type="text" id="amount" style="border:0; color:#f6931f; font-weight:bold;" readonly="readonly" />
                        <div id="slider-range"></div><br />
                        <div id="categories">
                            <input type="checkbox" id="svcfee" onchange="chartChange(this);" checked /><label for="svcfee">Servicer Fee</label>
                            <input type="checkbox" id="interest" onchange="chartChange(this);" checked /><label for="interest">Interest</label>
                            <input type="checkbox" id="unschedcdr" onchange="chartChange(this);" checked /><label for="unschedcdr">Unscheduled CDR</label>
                            <input type="checkbox" id="unschedvpr" onchange="chartChange(this);" checked /><label for="unschedvpr">Unscheduled VPR</label>
                            <input type="checkbox" id="schedprin" onchange="chartChange(this);" checked /><label for="schedprin">Scheduled Principal</label>
                        </div>
                        <div id="numfilter_div" style="display:none"></div>
                        <div id="colchart_div" align="center"></div></div>
                    <div id="piechart_div" align="center"></div>
                </div>
            </div>
        </div>
    </body>
</html>
    ''')
        
class CashFlowGrapher(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
<html>
    <head>
        <script language="javascript">
            function filecheck() {
                if (document.getElementById('uploadfield').checked == true) {
                    document.getElementById('filefield').disabled = false;
                    document.getElementById('inputdatafield').disabled = true; }
                else {
                    document.getElementById('filefield').disabled = true;
                    document.getElementById('inputdatafield').disabled = false; } }
        </script>
        <title>Cash Flow Grapher</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/redmond/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script>
            function home() {window.location="/"; }
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }
            
            $(document).ready(function() {
                $("button").button();
                $("#accordion").accordion(); });
        </script>
    </head>
    <body style="font-size:62.5%;">
        <button type="button" onclick="home();");">Back to Home</button>
        <button type="button" onclick="logout();");">Sign Out</button>
        <div id="accordion">
            <h3><a href="#">Cash Flow Grapher</a></h3>
            <div>
                <form action="/grapher" enctype="multipart/form-data" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td>Input Data<br />(date, principal, interest)</td><td><textarea id="inputdatafield" name="inputdata" rows="10" cols="50">
08/25/2011, 0, 252.84
09/26/2011, 0, 261
10/25/2011, 0, 236.53
11/25/2011, 0, 252.84
12/27/2011, 0, 261
01/25/2012, 0, 236.53
02/27/2012, 0, 269.16
03/26/2012, 0, 228.38
04/25/2012, 0, 244.69
05/25/2012, 0, 244.69
06/25/2012, 0, 252.84
07/25/2012, 0, 244.69
08/27/2012, 0, 269.16
09/25/2012, 0, 236.53
10/25/2012, 0, 244.69
11/26/2012, 0, 261
12/26/2012, 0, 244.69
01/25/2013, 0, 244.69
02/25/2013, 0, 252.84
03/25/2013, 0, 228.38
04/25/2013, 0, 252.84
05/28/2013, 0, 269.16
06/25/2013, 0, 228.38
07/25/2013, 0, 244.69
08/26/2013, 0, 261
09/25/2013, 0, 244.69
10/25/2013, 0, 244.69
11/25/2013, 0, 252.84
12/26/2013, 0, 252.84
01/27/2014, 0, 261
02/25/2014, 0, 236.53
03/25/2014, 0, 228.38
04/25/2014, 0, 252.84
05/27/2014, 0, 261
06/25/2014, 0, 236.53
07/25/2014, 0, 244.69
08/25/2014, 0, 252.84
09/25/2014, 0, 252.84
10/27/2014, 0, 261
11/25/2014, 0, 236.53
12/26/2014, 0, 252.84
01/26/2015, 0, 252.84
02/25/2015, 0, 244.69
03/25/2015, 0, 228.38
04/27/2015, 0, 269.16
05/26/2015, 0, 236.53
06/25/2015, 0, 244.69
07/27/2015, 0, 261
08/25/2015, 0, 236.53
09/25/2015, 0, 252.84
10/26/2015, 0, 252.84
11/25/2015, 0, 244.69
12/28/2015, 0, 269.16
01/25/2016, 0, 228.38
02/25/2016, 0, 252.84
03/25/2016, 0, 236.53
04/25/2016, 0, 252.84
05/25/2016, 0, 244.69
06/27/2016, 0, 269.16
07/25/2016, 0, 228.38
08/25/2016, 0, 252.84
09/26/2016, 0, 261
10/25/2016, 0, 236.53
11/25/2016, 0, 252.84
12/27/2016, 0, 261
01/25/2017, 0, 236.53
02/27/2017, 0, 269.16
03/27/2017, 0, 228.38
04/25/2017, 0, 236.53
05/25/2017, 0, 244.69
06/26/2017, 0, 261
07/25/2017, 0, 236.53
08/25/2017, 0, 252.84
09/25/2017, 0, 252.84
10/25/2017, 0, 244.69
11/27/2017, 0, 269.16
12/26/2017, 0, 236.53
01/25/2018, 0, 244.69
02/26/2018, 0, 261
03/26/2018, 0, 228.38
04/25/2018, 0, 244.69
05/25/2018, 0, 244.69
06/25/2018, 0, 252.84
07/25/2018, 0, 244.69
08/27/2018, 0, 269.16
09/25/2018, 0, 236.53
10/25/2018, 0, 244.69
11/26/2018, 0, 261
12/26/2018, 0, 244.69
01/25/2019, 0, 244.69
02/25/2019, 0, 252.84
03/25/2019, 0, 228.38
04/25/2019, 0, 252.84
05/28/2019, 0, 269.16
06/25/2019, 0, 228.38
07/25/2019, 0, 244.69
08/26/2019, 0, 261
09/25/2019, 0, 244.69
10/25/2019, 0, 244.69
11/25/2019, 0, 252.84
12/26/2019, 0, 252.84
01/27/2020, 0, 261
02/25/2020, 0, 236.53
03/25/2020, 0, 236.53
04/27/2020, 0, 269.16
05/26/2020, 0, 236.53
06/25/2020, 0, 244.69
07/27/2020, 0, 261
08/25/2020, 0, 236.53
09/25/2020, 0, 252.84
10/26/2020, 0, 252.84
11/25/2020, 0, 244.69
12/28/2020, 0, 269.16
01/25/2021, 0, 228.38
02/25/2021, 0, 252.84
03/25/2021, 0, 228.37
04/26/2021, 0, 261
05/25/2021, 0, 236.53
06/25/2021, 0, 252.84
07/26/2021, 0, 252.84
08/25/2021, 0, 328.02
09/27/2021, 0, 360.82
10/25/2021, 0, 306.15
11/26/2021, 0, 349.89
12/27/2021, 0, 338.95
01/25/2022, 0, 317.09
02/25/2022, 0, 338.95
03/25/2022, 0, 306.15
04/25/2022, 0, 338.95
05/25/2022, 0, 328.02
06/27/2022, 0, 360.82
07/25/2022, 0, 306.15
08/25/2022, 0, 338.95
09/26/2022, 0, 349.89
10/25/2022, 0, 317.09
11/25/2022, 8931.32, 338.95
12/27/2022, 12558.74, 343.64
01/25/2023, 12443.79, 303.46
02/27/2023, 12189.83, 336.33
03/27/2023, 12118.15, 277.91
04/25/2023, 11928.26, 280.15
05/25/2023, 11741.97, 281.99
06/26/2023, 11539.49, 292.57
07/25/2023, 11433.7, 257.82
08/25/2023, 11236.83, 267.85
09/25/2023, 11079.32, 260.23
10/25/2023, 10941.7, 244.57
11/27/2023, 10735.59, 261.13
12/26/2023, 10652.43, 222.67
01/25/2024, 10485.7, 223.36
02/26/2024, 10304.57, 230.91
03/25/2024, 10225.41, 195.74
04/25/2024, 10032.71, 209.78
05/28/2024, 9859.42, 216.08
06/25/2024, 9799.41, 177.3
07/25/2024, 9630.16, 183.54
08/26/2024, 9463.7, 189.03
09/25/2024, 9359.81, 171.01
10/25/2024, 9227.17, 164.87
11/25/2024, 9082.14, 164.11
12/26/2024, 8953.73, 157.95
01/27/2025, 8812.87, 156.78
02/25/2025, 8730.08, 136.49
03/25/2025, 8620.17, 126.44
04/25/2025, 8457.15, 134.15
05/27/2025, 8323.55, 132.56
06/25/2025, 8244.81, 114.85
07/25/2025, 8114.35, 113.4
08/25/2025, 7986.26, 111.68
09/25/2025, 7872.7, 106.27
10/27/2025, 7748.3, 104.19
11/25/2025, 7674.59, 89.5
12/26/2025, 7540.93, 90.47
01/26/2026, 7433.43, 85.36
02/25/2026, 7338.71, 77.73
03/25/2026, 7256.77, 68.06
04/27/2026, 7096.37, 74.97
05/26/2026, 7039.37, 61.38
06/25/2026, 6926.23, 58.88
07/27/2026, 6805.24, 57.96
08/25/2026, 6739.4, 48.21
09/25/2026, 6621.86, 46.97
10/26/2026, 6526.9, 42.48
11/25/2026, 6442.87, 36.83
12/28/2026, 6319.94, 35.86
01/25/2027, 6276.05, 26.56
02/25/2027, 6154.26, 25.15
03/25/2027, 6094.32, 18.95
04/26/2027, 5968.84, 17.39
05/25/2027, 5910.58, 11.97
06/25/2027, 5807.02, 8.79
07/26/2027, 5723.15, 4.85
08/25/2027, 1437.9, 0.94</textarea></td></tr>
                        <tr><td colspan="2"><p style="font-size:10px;">Every line requires all three values separated by commas. Enter 0 if there is no principal and/or interest.<br />
                        Make sure there is no extra empty line at end of dataset.</p></td></tr>
                        <tr><td>Upload CSV File <input id="uploadfield" onclick="filecheck();" type="checkbox" name="upload" value="True" /></td>
                            <td><input id="filefield" type="file" name="csv" disabled /></td></tr>
                        <tr><td colspan="2"><p style="font-size:10px;">Must be a CSV file with three columns in this order: date, principal, interest.<br />
                        Remove all headers and extra data. Remove all number formatting.</p></td></tr>
                        <tr><td colspan="2"><button type="submit">Graph Cash Flow</button></td></tr>
                    </table>
                </form>
            </div>
        </div>
    </body>
</html>
    ''')
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
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/redmond/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript ">

        google.load('visualization', '1', {packages:['table']});
        google.load('visualization', '1', {packages:['corechart']});
        google.load('visualization', '1.1', {packages:['controls']});
        google.setOnLoadCallback(drawDashboard);
        google.setOnLoadCallback(drawTable);
        google.setOnLoadCallback(drawPieChart);

        var data = '''+str(data)+''';
        var totint = 0
        var totprin = 0
        for (var i=0;i<data.length;i++) {
            totprin = totprin + data[i][1];
            totint = totint + data[i][2]; }

        function round(var1, n) {
            return Math.round(var1*Math.pow(10,n)) / Math.pow(10,n); }

        function drawTable() {
            var table = new google.visualization.DataTable();
            table.addColumn('string', 'Date');
            table.addColumn('number', 'Principal ($)');
            table.addColumn('number', 'Interest ($)');
            
            table.addRows(data.length);
            for (var i=0;i<data.length;i++) {
                table.setCell(i, 0, data[i][0]);
                table.setCell(i, 1, data[i][1]);
                table.setCell(i, 2, data[i][2]); }
            
            var formatter = new google.visualization.NumberFormat();
            formatter.format(table, 1);
            formatter.format(table, 2);
            
            var datatable = new google.visualization.Table(document.getElementById('table_div'));
            datatable.draw(table, {width:500}); }

        var rangeSlider;
        var columnChart;
        function drawDashboard() {
            var coldata = new google.visualization.DataTable();
            coldata.addColumn('string', 'Date');
            coldata.addColumn('number', 'Principal');
            coldata.addColumn('number', 'Interest');
            coldata.addColumn('number', 'Date Range');
            
            coldata.addRows(data.length);
            for (var i=0;i<data.length;i++) {
                coldata.setValue(i, 0, data[i][0]);
                coldata.setValue(i, 1, data[i][1]);
                coldata.setValue(i, 2, data[i][2]);
                coldata.setValue(i, 3, i+1); }
                
            var formatter = new google.visualization.NumberFormat({prefix:'$'});
            formatter.format(coldata, 1);
            formatter.format(coldata, 2);

            var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));

            rangeSlider = new google.visualization.ControlWrapper({
                controlType: 'NumberRangeFilter',
                containerId: 'numfilter_div',
                options: {filterColumnLabel: 'Date Range'} });
            
            columnChart = new google.visualization.ChartWrapper({
                chartType: 'ColumnChart',
                containerId: 'colchart_div',
                options: {isStacked:true, width:1500, height:700, title:'Cash Flow',
                    hAxis:{title:'Date'}, legend:'right', vAxis:{title:'Payment', format:'$#,###'} },
                view: {columns:[0, 1, 2]} });

            dashboard.bind(rangeSlider, columnChart);
            dashboard.draw(coldata); }

        function drawPieChart() {
            var piedata = new google.visualization.DataTable();
            piedata.addColumn('string', 'Payment Type');
            piedata.addColumn('number', 'Cash Amount');
            
            piedata.addRows(2);
            piedata.setValue(0,0,'Principal');
            piedata.setValue(1,0,'Interest');
            piedata.setValue(0,1,round(totprin, 2));
            piedata.setValue(1,1,round(totint, 2));
            
            var formatter = new google.visualization.NumberFormat({prefix:'$'});
            formatter.format(piedata, 1);
            
            var piechart = new google.visualization.PieChart(document.getElementById('piechart_div'));
            piechart.draw(piedata, {height:700, width:1500, legend:'right', title:'Cash Breakdown', is3D:true}); }

        function filecheck(){
            if (document.getElementById('uploadfield').checked == true) {
                document.getElementById('filefield').disabled = false;
                document.getElementById('inputdatafield').disabled = true; }
            else {
                document.getElementById('filefield').disabled = true;
                document.getElementById('inputdatafield').disabled = false; } }
        </script>
        <script>
            function home() {window.location="/"; }
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }
            function sliderChange(low, high) {rangeSlider.setState({'lowValue':low, 'highValue':high}); rangeSlider.draw(); }
            function chartChange(id) {
                var a = ["schedprin", "interest"];
                var b = [0];
                for(var i=0;i<a.length;i++) {
                    if (document.getElementById(a[i]).checked == true) {
                        b.push(i+1); } }
                if (b.length == 1) {id.checked = true; }
                else {
                columnChart.setView({columns:b});
                columnChart.draw(); } }
            
            $(document).ready(function() {
                $("#tabs").tabs();
                $("button").button();
                $("#categories").buttonset();
                $("#accordion1").accordion({active: false, collapsible: true});
                $("#accordion2").accordion({collapsible: true, autoHeight: false});
                $("#slider-range").slider({
                    range: true,
                    min: 1,
                    max: data.length,
                    values: [1, data.length],
                    animate: "normal",
                    slide: function(event, ui) {$("#amount").val(data[(ui.values[0]-1)][0] + " - " + data[(ui.values[1]-1)][0]); sliderChange(ui.values[0], ui.values[1]);} }); 
		$("#amount").val(data[$("#slider-range").slider("values", 0)-1][0] + " - " + data[$("#slider-range").slider("values", 1)-1][0]); });
        </script>
    </head>
    <body style="font-size:62.5%;">
        <button type="button" onclick="home();");">Back to Home</button>
        <button type="button" onclick="logout();");">Sign Out</button>
        <div id="accordion1">
            <h3><a href="#">Cash Flow Grapher</a></h3>
            <div>
                <form action="/grapher" enctype="multipart/form-data" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td>Input Data<br />(date, principal, interest)</td><td><textarea id="inputdatafield" name="inputdata" rows="10" cols="50" '''+inputdatadisabled+'''>'''+self.request.get('inputdata')+'''</textarea></td></tr>
                        <tr><td colspan="2"><p style="font-size:10px;">Every line requires all three values separated by commas. Enter 0 if there is no principal and/or interest.<br />
                        Make sure there is no extra empty line at end of dataset.</p></td></tr>
                        <tr><td>Upload CSV File <input id="uploadfield" onclick="filecheck();" type="checkbox" name="upload" value="True" '''+check+''' /></td>
                            <td><input id="filefield" type="file" name="csv" '''+filedisabled+''' /></td></tr>
                        <tr><td colspan="2"><p style="font-size:10px;">Must be a CSV file with three columns in this order: date, principal, interest.<br />
                        Remove all headers and extra data. Remove all number formatting.</p></td></tr>
                        <tr><td colspan="2"><button type="submit">Graph Cash Flow</button></td></tr>
                    </table>
                </form>
            </div>
        </div>
        <div id="accordion2">
            <h3><a href="#">Results</a></h3>
            <div>
                <div id="tabs">
                    <ul>
                        <li><a href="#table_div">Cash Flow</a></li>
                        <li><a href="#dashboard_div">Time Chart of Cash Flow</a></li>
                        <li><a href="#piechart_div">Cash Breakdown</a></li>
                    </ul>
                    <div id="table_div" align="center"></div>
                    <div id="dashboard_div">
                        <label for="amount" style="font-family:arial; font-size:12px;">Date Range:</label>
                        <input type="text" size="40" id="amount" style="border:0; color:#f6931f; font-weight:bold;" readonly="readonly" />
                        <div id="slider-range"></div><br />
                        <div id="categories">
                            <input type="checkbox" id="interest" onchange="chartChange(this);" checked /><label for="interest">Interest</label>
                            <input type="checkbox" id="schedprin" onchange="chartChange(this);" checked /><label for="schedprin">Scheduled Principal</label>
                        </div>
                        <div id="numfilter_div" style="display:none"></div>
                        <div id="colchart_div" align="center"></div></div>
                    <div id="piechart_div" align="center"></div>
                </div>
            </div>
        </div>
    </body>
</html>
        ''')

class PriceFinder(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
<html>
    <head>
        <title>CUSIP Price Finder</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/redmond/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script>
            function home() {window.location="/"; }
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }
            
            $(document).ready(function() {
                $("button").button();
                $("#accordion1").accordion();
                $("#accordion2").accordion(); });
        </script>
    </head>
    <body style="font-size:62.5%;">
        <button type="button" onclick="home();");">Back to Home</button>
        <button type="button" onclick="logout();");">Sign Out</button>
        <div id="accordion1">
            <h3><a href="#">CUSIP List Price Finder</a></h3>
            <div>
                <form action="/price" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td><textarea name="cusiplst" rows="3" cols="200">233889AE4, 12667GWF6, 68389FBW3, 86358RE29, 743873AP6, 617463AA2</textarea></td></tr>
                        <tr><td><p style="font-size:10px;">Enter CUSIP values separated by commas.<br />Do not enter any line breaks.</p></td></tr>
                        <tr><td><button type="submit" name="find-1" value="Find Price">Find Price</button></td></tr>
                    </table>
                </form>
            </div>
        </div>
        <div id="accordion2">
            <h3><a href="#">CUSIP Paste Price Finder</a></h3>
            <div>
                <form action="/price" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td><textarea name="cusippaste" rows="15" cols="200">
233889AE4 these
12667GWF6 characters
68389FBW3 will
86358RE29 be
743873AP6 ignored</textarea></td></tr>
                        <tr><td><p style="font-size:10px;">The first 9 characters of each line will be interpreted as a CUSIP.</p></td></tr>
                        <tr><td><button type="submit" name="find-2" value="Find Price">Find Price</button></td></tr>
                    </table>
                </form>
            </div>
        </div>
    </body>
</html>
        ''')
    def post(self):
        raw_data = []
        if str(self.request.get('find-1')) == 'Find Price':
            cusip_input = self.request.get('cusiplst')
            split_input = cusip_input.split(', ')
            for cusip in split_input:
                raw_data.append(str(cusip))
        else:
            cusip_input = self.request.get('cusippaste')
            split_input = cusip_input.split('\r\n')
            for i in split_input:
                raw_data.append(str(i)[:9])
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
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/redmond/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script>
            function home() {window.location="/"; }
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }
            
            $(document).ready(function() {
                $("button").button();
                $("#accordion1").accordion({active: false, collapsible: true});
                $("#accordion2").accordion({active: false, collapsible: true});
                $("#accordion3").accordion({collapsible: true, autoHeight: false}); });
        </script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript ">

        google.load('visualization', '1', {packages:['table']});
        google.load('visualization', '1', {packages:['corechart']});
        google.setOnLoadCallback(drawTable);

        var data = '''+str(data)+''';

        function drawTable() {
            var table = new google.visualization.DataTable();
            table.addColumn('string', 'CUSIP');
            table.addColumn('string', 'Price');
            
            table.addRows(data.length);
            for (var i=0;i<data.length;i++){
                table.setCell(i, 0, data[i][0]);
                table.setCell(i, 1, data[i][1]);}
            
            var datatable = new google.visualization.Table(document.getElementById('table_div'));
            datatable.draw(table, {width:300}); }
            
        </script>
    </head>
    <body style="font-size:62.5%;">
        <button type="button" onclick="home();");">Back to Home</button>
        <button type="button" onclick="logout();");">Sign Out</button>
        <div id="accordion1">
            <h3><a href="#">CUSIP List Price Finder</a></h3>
            <div>
                <form action="/price" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td><textarea name="cusiplst" rows="3" cols="200">'''+self.request.get('cusiplst')+'''</textarea></td></tr>
                        <tr><td><p style="font-size:10px;">Enter CUSIP values separated by commas.<br />Do not enter any line breaks.</p></td></tr>
                        <tr><td><button type="submit" name="find-1" value="Find Price">Find Price</button></td></tr>
                    </table>
                </form>
            </div>
        </div>
        <div id="accordion2">
            <h3><a href="#">CUSIP Paste Price Finder</a></h3>
            <div>
                <form action="/price" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td><textarea name="cusippaste" rows="15" cols="200">'''+self.request.get('cusippaste')+'''</textarea></td></tr>
                        <tr><td><p style="font-size:10px;">The first 9 characters of each line will be interpreted as a CUSIP.</p></td></tr>
                        <tr><td><button type="submit" name="find-2" value="Find Price">Find Price</button></td></tr>
                    </table>
                </form>
            </div>
        </div>
        <div id="accordion3">
            <h3><a href="#">Results</a></h3>
            <div>
                <div id="table_div" align="center"></div>
            </div>
        </div>
    </body>
</html>
        ''')
                

application = webapp.WSGIApplication([('/', MainPage), ('/calculator', MBSCalculator), ('/grapher', CashFlowGrapher), ('/price', PriceFinder)], debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
