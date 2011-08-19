##Alex Hsu
##James Feng
##8/17/2011
##Version 1.6

import urllib, urllib2
import csv

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

header = 'Alex Hsu, James Feng, 8/17/2011, Version 1.6'
jquerytheme = 'redmond'

# this entire code is the source of the site. each class is a page on the site.
# get method is the page that inititally displays. post method is the page that displays upon a call to post (usually from submitting forms).
# self.response.out.write() outputs javascript and html as string to webpage.

class MainPage(webapp.RequestHandler):
    def get(self):
        useremail = users.get_current_user().email()
        if ('@chilmarkhill.com' in useremail or
            useremail == 'jake01@gmail.com' or
            useremail == 'alexhsu92@gmail.com' or
            useremail == 'broncos24@gmail.com' or
            useremail == 'jcmaltmail@gmail.com'):
            self.response.out.write('''
<!-- '''+header+''' -->
<html>
    <head>
        <title>Chilmark Hill Utilities</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/'''+jquerytheme+'''/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script>
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }
            function chilmarkhome() {window.location="http://www.chilmarkhill.com/"; }  

            // initialize jquery ui elements.
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
        <a href="/price">CUSIP Price Finder</a><br /><br />
        <a href="/visual">Bond Visualization</a><br /><br /></p>
        <p style="font-family:arial; font-size:10px; text-align:center;">
        Optimized for Google Chrome.<br />
        Known bugs in Mozilla Firefox.<br />
        Not supported in Internet Explorer.</p>
    </body>
</html>
        ''')
        else:
            self.response.out.write('''
<!-- '''+header+''' -->
<html>
    <head>
        <title>Access Denied</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/'''+jquerytheme+'''/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script>
            // access denied alert.
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
<!-- '''+header+''' -->
<html>
    <head>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/'''+jquerytheme+'''/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script language="javascript">
            // check if balloon checkbox is checked.
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

            // initialize jquery ui elements.
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
        # pulls inputs from form.
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
        # begin to output page for mortgage calculator results.
        self.response.out.write('''
<!-- '''+header+''' -->
<html>
    <head>
        <title>Calculation Results</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/'''+jquerytheme+'''/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript ">
            // check if balloon checkbox is checked.
            function blncheck() {
                if (document.getElementById('blnfield').checked == true) {
                    document.getElementById('blntermfield').disabled = false; }
                else {
                    document.getElementById('blntermfield').disabled = true;
                    document.getElementById('blntermfield').value = ''; } }

            // load google charts.
            google.load('visualization', '1', {packages:['table']});
            google.load('visualization', '1', {packages:['corechart']});
            google.load('visualization', '1.1', {packages:['controls']});

            // call these functions when page loads. functions defined below.
            google.setOnLoadCallback(drawDashboard);
            google.setOnLoadCallback(drawTable);
            google.setOnLoadCallback(drawPieChart);
            google.setOnLoadCallback(drawInputTable);

            // set variables based on user input.
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

            // function for rounding values.
            function round(var1, n) {
                return Math.round(var1*Math.pow(10,n)) / Math.pow(10,n); }

            // an array of original user inputs.
            var inputs = [currprin, currwac*100, origterm, svcfee*10000, vpr*100, cdr*100, sev*100, cdrlag, balloon, blnterminput]

            // calculate for first month.
            var data = [];
            var month = 1;
            var wala = 1;
            var wam = origterm;
            var vprunschedprin = currprin * vprsmm;

            if (cdrlag == 0) {
                var cdrunschedprin = currprin * cdrsmm * (1 - sev);
                var lossprin = currprin * cdrsmm * sev; }
            else {
                var cdrunschedprin = 0;
                var lossprin = 0; }

            var totunschedprin = vprunschedprin + cdrunschedprin
            var schedpmt = (currprin * monthlywac) / (1 - Math.pow((1 + monthlywac), (-wam)));
            var interest = currprin * monthlywac;
            var schedprin = schedpmt - interest;
            currprin = currprin - (totunschedprin + schedprin)
            var pmt = schedprin + interest + vprunschedprin + monthlysvcfee;
            var netmoney = pmt;

            // push data for first month into global data 2D array.
            data.push([month, wala, wam, round(currprin, 2), round(schedprin, 2), round(vprunschedprin, 2), round(cdrunschedprin, 2),
                round(totunschedprin, 2), round(-(lossprin), 2), round(interest, 2), round(monthlysvcfee, 2), round(pmt, 2),
                round(netmoney, 2)]);

            // begin to keep track of net interest, scheduled principal, losses, etc.
            var netint = interest;
            var netsched = schedprin;
            var netvprunsched = vprunschedprin;
            var netcdrunsched = cdrunschedprin;
            var netloss = lossprin;

            // calculate for months before cdr lag (before losses start).
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

            // calculate for remaining months except last month.
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

            // calculate last month separately to account for balloon payment.
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

            // draw table of user inputs.
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

                // format columns to currency form.
                var formatter = new google.visualization.NumberFormat();
                formatter.format(intable, 0);
                formatter.format(intable, 1);
                formatter.format(intable, 4);
                formatter.format(intable, 5);
                formatter.format(intable, 6);
                
                var indatatable = new google.visualization.Table(document.getElementById('inputtable_div'));
                indatatable.draw(intable); }

            // draw table of monthly cash flow results.
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

                // format columns to currency form.
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

            // draw column chart of cash flow. rangeSlider and columnChart are global variables so they can be accessed by other functions below.
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

                // looping over every month to build coldata data table.
                coldata.addRows(blnterm);
                for(var m=0;m<blnterm;m++) {
                    coldata.setValue(m,0,data[m][0].toString());
                    coldata.setValue(m,1,data[m][4]);
                    coldata.setValue(m,2,data[m][5]);
                    coldata.setValue(m,3,data[m][6]);
                    coldata.setValue(m,4,data[m][9]);
                    coldata.setValue(m,5,data[m][10]);
                    coldata.setValue(m,6,data[m][0]); }

                // format columns to currency form.
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

            // draw cash breakdown pie chart.
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

                // format columns to currency form.
                var formatter = new google.visualization.NumberFormat({prefix:'$'});
                formatter.format(piedata, 1);
                
                var piechart = new google.visualization.PieChart(document.getElementById('piechart_div'));
                piechart.draw(piedata, {height:700, width:1500, legend:'right', title:'Cash Breakdown', is3D:true}); }
        </script>
        <script>
            function home() {window.location="/"; }
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }

            // jquery slider tied to original google charts slider (which is now hidden). jquery slider changes google charts slider and tells it to redraw chart.
            function sliderChange(low, high) {rangeSlider.setState({'lowValue':low, 'highValue':high}); rangeSlider.draw(); }

            // function for changing view of column chart. allow user to only view individual categories.
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

            // initialize jquery ui elements.
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
                    slide: function(event, ui) {$("#amount").val(ui.values[0] + " - " + ui.values[1]); sliderChange(ui.values[0], ui.values[1]);},
                    stop: function(event, ui) {$("#amount").val(ui.values[0] + " - " + ui.values[1]); sliderChange(ui.values[0], ui.values[1]);} }); 
		$("#amount").val($("#slider-range").slider("values", 0) + " - " + $("#slider-range").slider("values", 1)); });
	</script>
    </head>
    <body style="font-size:62.5%;">
        <button type="button" onclick="home();");">Back to Home</button>
        <button type="button" onclick="logout();");">Sign Out</button>
	<!-- for user to recalculate using different inputs -->
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
        <!-- display results -->
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
<!-- '''+header+''' -->
<html>
    <head>
        <script language="javascript">
            // checks if upload csv file option is checked.
            function filecheck() {
                if (document.getElementById('uploadfield').checked == true) {
                    document.getElementById('filefield').disabled = false;
                    document.getElementById('inputdatafield').disabled = true; }
                else {
                    document.getElementById('filefield').disabled = true;
                    document.getElementById('inputdatafield').disabled = false; } }
        </script>
        <title>Cash Flow Grapher</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/'''+jquerytheme+'''/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script>
            function home() {window.location="/"; }
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }

            // initialize jquery ui elements.
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
                <!-- option to load Merrill Lynch sample data -->
                <form action="/grapher" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td colspan="2"><button type="submit" name="loadml" value="true">Load MLMI2007-ML1 M1</button></td></tr>
                    </table>
                </form>
                <!-- input with sample data -->
                <form action="/grapher" enctype="multipart/form-data" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td>Input Data<br />(date, principal, interest)</td><td><textarea id="inputdatafield" name="inputdata" rows="10" cols="50">
11/25/2022, 8931.32, 338.95
12/27/2022, 12558.74, 343.64
01/25/2023, 12443.79, 303.46
02/27/2023, 12189.83, 336.33
03/27/2023, 12118.15, 277.91
04/25/2023, 11928.26, 280.15
05/25/2023, 11741.97, 281.99
06/26/2023, 11539.49, 292.57
07/25/2023, 11433.7, 257.82
08/25/2023, 11236.83, 267.85</textarea></td></tr>
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
        # load sample Merrill Lynch bond data.
        if str(self.request.get('loadml')) == 'true':
            loadml = ''
            data = 'CPR02CDR05'
            check = ''
            filedisabled = 'disabled'
            inputdatadisabled = ''
        else:
            # if NOT uploading csv file, parse data.
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
            # if uploading csv file, parse csv file.
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
            # if not loading Merrill Lynch data, hide the toolbar for switching between scenarios.
            loadml = '''style="display:none"'''
        self.response.out.write('''
<!-- '''+header+''' -->
<html>
    <head>
        <title>Graphing Results</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/'''+jquerytheme+'''/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript ">

        // load google charts api.
        google.load('visualization', '1', {packages:['table']});
        google.load('visualization', '1', {packages:['corechart']});
        google.load('visualization', '1.1', {packages:['controls']});
        google.setOnLoadCallback(calculateTotal);
        google.setOnLoadCallback(drawDashboard);
        google.setOnLoadCallback(drawTable);
        google.setOnLoadCallback(drawPieChart);

        // function for rounding.
        function round(var1, n) {
            return Math.round(var1*Math.pow(10,n)) / Math.pow(10,n); }

        // preloaded Merrill Lynch data.
        var CPR02CDR05 = [['08/25/2011', 0.0, 252.84], ['09/26/2011', 0.0, 270.22], ['10/25/2011', 0.0, 244.89], ['11/25/2011', 0.0, 261.78], ['12/27/2011', 0.0, 270.22], ['01/25/2012', 0.0, 244.89], ['02/27/2012', 0.0, 278.67], ['03/26/2012', 0.0, 236.44], ['04/25/2012', 0.0, 253.33], ['05/25/2012', 0.0, 253.33], ['06/25/2012', 0.0, 261.78], ['07/25/2012', 0.0, 253.33], ['08/27/2012', 0.0, 278.67], ['09/25/2012', 0.0, 244.89], ['10/25/2012', 0.0, 253.33], ['11/26/2012', 0.0, 270.22], ['12/26/2012', 0.0, 253.33], ['01/25/2013', 0.0, 253.33], ['02/25/2013', 0.0, 261.78], ['03/25/2013', 0.0, 236.44], ['04/25/2013', 0.0, 261.78], ['05/28/2013', 0.0, 278.67], ['06/25/2013', 0.0, 236.44], ['07/25/2013', 0.0, 253.33], ['08/26/2013', 0.0, 270.22], ['09/25/2013', 0.0, 253.33], ['10/25/2013', 0.0, 253.33], ['11/25/2013', 0.0, 261.78], ['12/26/2013', 0.0, 261.78], ['01/27/2014', 0.0, 270.22], ['02/25/2014', 0.0, 244.89], ['03/25/2014', 0.0, 236.44], ['04/25/2014', 0.0, 261.78], ['05/27/2014', 0.0, 270.22], ['06/25/2014', 0.0, 244.89], ['07/25/2014', 0.0, 253.33], ['08/25/2014', 0.0, 261.78], ['09/25/2014', 0.0, 261.78], ['10/27/2014', 0.0, 270.22], ['11/25/2014', 0.0, 244.89], ['12/26/2014', 0.0, 261.78], ['01/26/2015', 0.0, 261.78], ['02/25/2015', 0.0, 253.33], ['03/25/2015', 0.0, 236.44], ['04/27/2015', 0.0, 278.67], ['05/26/2015', 0.0, 244.89], ['06/25/2015', 0.0, 253.33], ['07/27/2015', 0.0, 270.22], ['08/25/2015', 0.0, 244.89], ['09/25/2015', 0.0, 261.78], ['10/26/2015', 0.0, 261.78], ['11/25/2015', 0.0, 253.33], ['12/28/2015', 0.0, 278.67], ['01/25/2016', 0.0, 236.44], ['02/25/2016', 0.0, 261.78], ['03/25/2016', 0.0, 244.89], ['04/25/2016', 0.0, 261.78], ['05/25/2016', 0.0, 253.33], ['06/27/2016', 0.0, 278.67], ['07/25/2016', 0.0, 236.44], ['08/25/2016', 0.0, 261.78], ['09/26/2016', 0.0, 270.22], ['10/25/2016', 0.0, 244.89], ['11/25/2016', 0.0, 261.78], ['12/27/2016', 0.0, 270.22], ['01/25/2017', 0.0, 244.89], ['02/27/2017', 0.0, 278.67], ['03/27/2017', 0.0, 236.44], ['04/25/2017', 0.0, 244.89], ['05/25/2017', 0.0, 253.33], ['06/26/2017', 0.0, 270.22], ['07/25/2017', 0.0, 244.89], ['08/25/2017', 0.0, 261.78], ['09/25/2017', 0.0, 261.78], ['10/25/2017', 0.0, 253.33], ['11/27/2017', 0.0, 278.67], ['12/26/2017', 0.0, 244.89], ['01/25/2018', 0.0, 253.33], ['02/26/2018', 0.0, 270.22], ['03/26/2018', 0.0, 236.44], ['04/25/2018', 0.0, 253.33], ['05/25/2018', 0.0, 253.33], ['06/25/2018', 0.0, 261.78], ['07/25/2018', 0.0, 253.33], ['08/27/2018', 0.0, 278.67], ['09/25/2018', 0.0, 244.89], ['10/25/2018', 0.0, 253.33], ['11/26/2018', 0.0, 270.22], ['12/26/2018', 0.0, 253.33], ['01/25/2019', 0.0, 253.33], ['02/25/2019', 0.0, 261.78], ['03/25/2019', 0.0, 236.44], ['04/25/2019', 0.0, 261.78], ['05/28/2019', 0.0, 278.67], ['06/25/2019', 0.0, 236.44], ['07/25/2019', 0.0, 253.33], ['08/26/2019', 0.0, 270.22], ['09/25/2019', 0.0, 253.33], ['10/25/2019', 0.0, 253.33], ['11/25/2019', 0.0, 261.78], ['12/26/2019', 0.0, 261.78], ['01/27/2020', 0.0, 270.22], ['02/25/2020', 0.0, 244.89], ['03/25/2020', 0.0, 244.89], ['04/27/2020', 0.0, 278.67], ['05/26/2020', 0.0, 244.89], ['06/25/2020', 0.0, 253.33], ['07/27/2020', 0.0, 270.22], ['08/25/2020', 0.0, 244.89], ['09/25/2020', 0.0, 261.78], ['10/26/2020', 0.0, 261.78], ['11/25/2020', 0.0, 253.33], ['12/28/2020', 0.0, 278.67], ['01/25/2021', 0.0, 236.44], ['02/25/2021', 0.0, 261.78], ['03/25/2021', 0.0, 236.44], ['04/26/2021', 0.0, 270.22], ['05/25/2021', 0.0, 244.89], ['06/25/2021', 0.0, 261.78], ['07/26/2021', 0.0, 261.78], ['08/25/2021', 0.0, 253.33], ['09/27/2021', 0.0, 278.67], ['10/25/2021', 0.0, 236.44], ['11/26/2021', 0.0, 270.22], ['12/27/2021', 0.0, 261.78], ['01/25/2022', 0.0, 244.89], ['02/25/2022', 0.0, 261.78], ['03/25/2022', 0.0, 236.44], ['04/25/2022', 0.0, 261.78], ['05/25/2022', 0.0, 253.33], ['06/27/2022', 0.0, 278.67], ['07/25/2022', 0.0, 236.44], ['08/25/2022', 0.0, 261.78], ['09/26/2022', 0.0, 270.22], ['10/25/2022', 0.0, 244.89], ['11/25/2022', 0.0, 261.78], ['12/27/2022', 0.0, 270.22], ['01/25/2023', 0.0, 244.89], ['02/27/2023', 0.0, 278.67], ['03/27/2023', 0.0, 236.44], ['04/25/2023', 0.0, 244.89], ['05/25/2023', 0.0, 253.33], ['06/26/2023', 0.0, 270.22], ['07/25/2023', 0.0, 244.89], ['08/25/2023', 0.0, 261.78], ['09/25/2023', 0.0, 261.78], ['10/25/2023', 0.0, 253.33], ['11/27/2023', 0.0, 278.67], ['12/26/2023', 0.0, 244.89], ['01/25/2024', 0.0, 253.33], ['02/26/2024', 0.0, 270.22], ['03/25/2024', 0.0, 236.44], ['04/25/2024', 0.0, 261.78], ['05/28/2024', 0.0, 278.67], ['06/25/2024', 0.0, 236.44], ['07/25/2024', 0.0, 253.33], ['08/26/2024', 0.0, 270.22], ['09/25/2024', 0.0, 253.33], ['10/25/2024', 70.39, 253.33], ['11/25/2024', 17088.59, 261.74], ['12/26/2024', 16988.56, 252.79], ['01/27/2025', 16889.13, 251.77], ['02/25/2025', 16790.31, 219.89], ['03/25/2025', 16692.09, 204.37], ['04/25/2025', 16594.13, 217.53], ['05/27/2025', 16496.13, 215.58], ['06/25/2025', 16399.31, 187.29], ['07/25/2025', 16302.14, 185.44], ['08/25/2025', 16206.9, 183.08], ['09/25/2025', 16112.24, 174.6], ['10/27/2025', 16018.16, 171.52], ['11/25/2025', 15924.6, 147.6], ['12/26/2025', 15830.7, 149.44], ['01/26/2026', 15738.37, 141.15], ['02/25/2026', 15645.42, 128.62], ['03/25/2026', 15553.73, 112.65], ['04/27/2026', 15462.45, 124.1], ['05/26/2026', 15371.93, 101.48], ['06/25/2026', 15277.02, 97.19], ['07/27/2026', 15187.11, 95.41], ['08/25/2026', 15097.46, 79.03], ['09/25/2026', 15009.56, 76.58], ['10/26/2026', 14922.19, 68.72], ['11/25/2026', 14833.4, 58.94], ['12/28/2026', 14745.63, 56.57], ['01/25/2027', 14650.81, 41.02], ['02/25/2027', 14556.29, 37.75], ['03/25/2027', 14471.58, 27.21], ['04/26/2027', 14387.39, 23.28], ['05/25/2027', 14303.72, 14.05], ['06/25/2027', 14220.57, 7.53], ['07/26/2027', 162.0, 0.08]];
        var CPR02CDR06 = [['08/25/2011', 0.0, 252.84], ['09/26/2011', 0.0, 270.22], ['10/25/2011', 0.0, 244.89], ['11/25/2011', 0.0, 261.78], ['12/27/2011', 0.0, 270.22], ['01/25/2012', 0.0, 244.89], ['02/27/2012', 0.0, 278.67], ['03/26/2012', 0.0, 236.44], ['04/25/2012', 0.0, 253.33], ['05/25/2012', 0.0, 253.33], ['06/25/2012', 0.0, 261.78], ['07/25/2012', 0.0, 253.33], ['08/27/2012', 0.0, 278.67], ['09/25/2012', 0.0, 244.89], ['10/25/2012', 0.0, 253.33], ['11/26/2012', 0.0, 270.22], ['12/26/2012', 0.0, 253.33], ['01/25/2013', 0.0, 253.33], ['02/25/2013', 0.0, 261.78], ['03/25/2013', 0.0, 236.44], ['04/25/2013', 0.0, 261.78], ['05/28/2013', 0.0, 278.67], ['06/25/2013', 0.0, 236.44], ['07/25/2013', 0.0, 253.33], ['08/26/2013', 0.0, 270.22], ['09/25/2013', 0.0, 253.33], ['10/25/2013', 0.0, 253.33], ['11/25/2013', 0.0, 261.78], ['12/26/2013', 0.0, 261.78], ['01/27/2014', 0.0, 270.22], ['02/25/2014', 0.0, 244.89], ['03/25/2014', 0.0, 236.44], ['04/25/2014', 0.0, 261.78], ['05/27/2014', 0.0, 270.22], ['06/25/2014', 0.0, 244.89], ['07/25/2014', 0.0, 253.33], ['08/25/2014', 0.0, 261.78], ['09/25/2014', 0.0, 261.78], ['10/27/2014', 0.0, 270.22], ['11/25/2014', 0.0, 244.89], ['12/26/2014', 0.0, 261.78], ['01/26/2015', 0.0, 261.78], ['02/25/2015', 0.0, 253.33], ['03/25/2015', 0.0, 236.44], ['04/27/2015', 0.0, 278.67], ['05/26/2015', 0.0, 244.89], ['06/25/2015', 0.0, 253.33], ['07/27/2015', 0.0, 270.22], ['08/25/2015', 0.0, 244.89], ['09/25/2015', 0.0, 261.78], ['10/26/2015', 0.0, 261.78], ['11/25/2015', 0.0, 253.33], ['12/28/2015', 0.0, 278.67], ['01/25/2016', 0.0, 236.44], ['02/25/2016', 0.0, 261.78], ['03/25/2016', 0.0, 244.89], ['04/25/2016', 0.0, 261.78], ['05/25/2016', 0.0, 253.33], ['06/27/2016', 0.0, 278.67], ['07/25/2016', 0.0, 236.44], ['08/25/2016', 0.0, 261.78], ['09/26/2016', 0.0, 270.22], ['10/25/2016', 0.0, 244.89], ['11/25/2016', 0.0, 261.78], ['12/27/2016', 0.0, 270.22], ['01/25/2017', 0.0, 244.89], ['02/27/2017', 0.0, 278.67], ['03/27/2017', 0.0, 236.44], ['04/25/2017', 0.0, 244.89], ['05/25/2017', 0.0, 253.33], ['06/26/2017', 0.0, 270.22], ['07/25/2017', 0.0, 244.89], ['08/25/2017', 0.0, 261.78], ['09/25/2017', 0.0, 261.78], ['10/25/2017', 0.0, 253.33], ['11/27/2017', 0.0, 278.67], ['12/26/2017', 0.0, 244.89], ['01/25/2018', 0.0, 253.33], ['02/26/2018', 0.0, 270.22], ['03/26/2018', 0.0, 236.44], ['04/25/2018', 0.0, 253.33], ['05/25/2018', 0.0, 253.33], ['06/25/2018', 0.0, 261.78], ['07/25/2018', 0.0, 253.33], ['08/27/2018', 0.0, 278.67], ['09/25/2018', 0.0, 244.89], ['10/25/2018', 0.0, 253.33], ['11/26/2018', 0.0, 270.22], ['12/26/2018', 0.0, 253.33], ['01/25/2019', 0.0, 253.33], ['02/25/2019', 0.0, 261.78], ['03/25/2019', 0.0, 236.44], ['04/25/2019', 0.0, 261.78], ['05/28/2019', 0.0, 278.67], ['06/25/2019', 0.0, 236.44], ['07/25/2019', 0.0, 253.33], ['08/26/2019', 0.0, 270.22], ['09/25/2019', 0.0, 253.33], ['10/25/2019', 0.0, 253.33], ['11/25/2019', 0.0, 261.78], ['12/26/2019', 0.0, 261.78], ['01/27/2020', 0.0, 270.22], ['02/25/2020', 0.0, 244.89], ['03/25/2020', 0.0, 244.89], ['04/27/2020', 0.0, 278.67], ['05/26/2020', 0.0, 244.89], ['06/25/2020', 0.0, 253.33], ['07/27/2020', 0.0, 270.22], ['08/25/2020', 0.0, 244.89], ['09/25/2020', 0.0, 261.78], ['10/26/2020', 0.0, 261.78], ['11/25/2020', 0.0, 253.33], ['12/28/2020', 0.0, 278.67], ['01/25/2021', 0.0, 236.44], ['02/25/2021', 0.0, 261.78], ['03/25/2021', 0.0, 236.44], ['04/26/2021', 0.0, 270.22], ['05/25/2021', 0.0, 244.89], ['06/25/2021', 0.0, 261.78], ['07/26/2021', 0.0, 261.78], ['08/25/2021', 0.0, 253.33], ['09/27/2021', 0.0, 278.67], ['10/25/2021', 0.0, 236.44], ['11/26/2021', 0.0, 270.22], ['12/27/2021', 0.0, 261.78], ['01/25/2022', 0.0, 244.89], ['02/25/2022', 0.0, 261.78], ['03/25/2022', 0.0, 236.44], ['04/25/2022', 0.0, 261.78], ['05/25/2022', 0.0, 253.33], ['06/27/2022', 0.0, 278.67], ['07/25/2022', 0.0, 236.44], ['08/25/2022', 0.0, 261.78], ['09/26/2022', 0.0, 270.22], ['10/25/2022', 0.0, 244.89], ['11/25/2022', 0.0, 261.78], ['12/27/2022', 0.0, 270.22], ['01/25/2023', 0.0, 244.89], ['02/27/2023', 0.0, 278.67], ['03/27/2023', 0.0, 236.44], ['04/25/2023', 0.0, 244.89], ['05/25/2023', 0.0, 253.33], ['06/26/2023', 0.0, 270.22], ['07/25/2023', 0.0, 244.89], ['08/25/2023', 0.0, 261.78], ['09/25/2023', 10333.49, 261.78], ['10/25/2023', 18085.4, 248.1], ['11/27/2023', 17958.94, 262.83], ['12/26/2023', 17829.45, 222.17], ['01/25/2024', 17704.57, 220.8], ['02/26/2024', 17580.14, 225.95], ['03/25/2024', 17456.48, 189.4], ['04/25/2024', 17334.34, 200.55], ['05/28/2024', 17213.05, 203.83], ['06/25/2024', 17092.6, 164.8], ['07/25/2024', 16972.99, 167.92], ['08/26/2024', 16854.21, 169.94], ['09/25/2024', 16734.92, 150.78], ['10/25/2024', 16616.45, 142.3], ['11/25/2024', 16500.13, 138.34], ['12/26/2024', 16384.62, 129.7], ['01/27/2025', 16269.9, 125.03], ['02/25/2025', 16155.98, 105.34], ['03/25/2025', 16042.86, 94.07], ['04/25/2025', 15930.23, 95.75], ['05/27/2025', 15817.81, 90.23], ['06/25/2025', 15706.7, 74.02], ['07/25/2025', 15595.52, 68.62], ['08/25/2025', 15486.3, 62.74], ['09/25/2025', 15377.84, 54.63], ['10/27/2025', 15270.14, 48.08], ['11/25/2025', 15163.13, 36.09], ['12/26/2025', 15056.08, 30.64], ['01/26/2026', 14950.64, 22.76], ['02/25/2026', 14844.93, 14.45], ['03/25/2026', 13680.16, 6.47]];
        var CPR02CDR08 = [['08/25/2011', 0.0, 252.84], ['09/26/2011', 0.0, 270.22], ['10/25/2011', 0.0, 244.89], ['11/25/2011', 0.0, 261.78], ['12/27/2011', 0.0, 270.22], ['01/25/2012', 0.0, 244.89], ['02/27/2012', 0.0, 278.67], ['03/26/2012', 0.0, 236.44], ['04/25/2012', 0.0, 253.33], ['05/25/2012', 0.0, 253.33], ['06/25/2012', 0.0, 261.78], ['07/25/2012', 0.0, 253.33], ['08/27/2012', 0.0, 278.67], ['09/25/2012', 0.0, 244.89], ['10/25/2012', 0.0, 253.33], ['11/26/2012', 0.0, 270.22], ['12/26/2012', 0.0, 253.33], ['01/25/2013', 0.0, 253.33], ['02/25/2013', 0.0, 261.78], ['03/25/2013', 0.0, 236.44], ['04/25/2013', 0.0, 261.78], ['05/28/2013', 0.0, 278.67], ['06/25/2013', 0.0, 236.44], ['07/25/2013', 0.0, 253.33], ['08/26/2013', 0.0, 270.22], ['09/25/2013', 0.0, 253.33], ['10/25/2013', 0.0, 253.33], ['11/25/2013', 0.0, 261.78], ['12/26/2013', 0.0, 261.78], ['01/27/2014', 0.0, 270.22], ['02/25/2014', 0.0, 244.89], ['03/25/2014', 0.0, 236.44], ['04/25/2014', 0.0, 261.78], ['05/27/2014', 0.0, 270.22], ['06/25/2014', 0.0, 244.89], ['07/25/2014', 0.0, 253.33], ['08/25/2014', 0.0, 261.78], ['09/25/2014', 0.0, 261.78], ['10/27/2014', 0.0, 270.22], ['11/25/2014', 0.0, 244.89], ['12/26/2014', 0.0, 261.78], ['01/26/2015', 0.0, 261.78], ['02/25/2015', 0.0, 253.33], ['03/25/2015', 0.0, 236.44], ['04/27/2015', 0.0, 278.67], ['05/26/2015', 0.0, 244.89], ['06/25/2015', 0.0, 253.33], ['07/27/2015', 0.0, 270.22], ['08/25/2015', 0.0, 244.89], ['09/25/2015', 0.0, 261.78], ['10/26/2015', 0.0, 261.78], ['11/25/2015', 0.0, 253.33], ['12/28/2015', 0.0, 278.67], ['01/25/2016', 0.0, 236.44], ['02/25/2016', 0.0, 261.78], ['03/25/2016', 0.0, 244.89], ['04/25/2016', 0.0, 261.78], ['05/25/2016', 0.0, 253.33], ['06/27/2016', 0.0, 278.67], ['07/25/2016', 0.0, 236.44], ['08/25/2016', 0.0, 261.78], ['09/26/2016', 0.0, 270.22], ['10/25/2016', 0.0, 244.89], ['11/25/2016', 0.0, 261.78], ['12/27/2016', 0.0, 270.22], ['01/25/2017', 0.0, 244.89], ['02/27/2017', 0.0, 278.67], ['03/27/2017', 0.0, 236.44], ['04/25/2017', 0.0, 244.89], ['05/25/2017', 0.0, 253.33], ['06/26/2017', 0.0, 270.22], ['07/25/2017', 0.0, 244.89], ['08/25/2017', 0.0, 261.78], ['09/25/2017', 0.0, 261.78], ['10/25/2017', 0.0, 253.33], ['11/27/2017', 0.0, 278.67], ['12/26/2017', 0.0, 244.89], ['01/25/2018', 0.0, 253.33], ['02/26/2018', 0.0, 270.22], ['03/26/2018', 0.0, 236.44], ['04/25/2018', 0.0, 253.33], ['05/25/2018', 0.0, 253.33], ['06/25/2018', 0.0, 261.78], ['07/25/2018', 0.0, 253.33], ['08/27/2018', 0.0, 278.67], ['09/25/2018', 0.0, 244.89], ['10/25/2018', 0.0, 253.33], ['11/26/2018', 0.0, 270.22], ['12/26/2018', 0.0, 253.33], ['01/25/2019', 0.0, 253.33], ['02/25/2019', 0.0, 261.78], ['03/25/2019', 0.0, 236.44], ['04/25/2019', 0.0, 261.78], ['05/28/2019', 0.0, 278.67], ['06/25/2019', 0.0, 236.44], ['07/25/2019', 0.0, 253.33], ['08/26/2019', 0.0, 270.22], ['09/25/2019', 0.0, 253.33], ['10/25/2019', 0.0, 253.33], ['11/25/2019', 0.0, 261.78], ['12/26/2019', 0.0, 261.78], ['01/27/2020', 0.0, 270.22], ['02/25/2020', 0.0, 244.89], ['03/25/2020', 0.0, 244.89], ['04/27/2020', 0.0, 278.67], ['05/26/2020', 0.0, 244.89], ['06/25/2020', 0.0, 253.33], ['07/27/2020', 0.0, 270.22], ['08/25/2020', 0.0, 244.89], ['09/25/2020', 0.0, 261.78], ['10/26/2020', 0.0, 261.78], ['11/25/2020', 0.0, 253.33], ['12/28/2020', 0.0, 278.67], ['01/25/2021', 0.0, 236.44], ['02/25/2021', 0.0, 261.78], ['03/25/2021', 0.0, 236.44], ['04/26/2021', 0.0, 270.22], ['05/25/2021', 0.0, 244.89], ['06/25/2021', 0.0, 261.78], ['07/26/2021', 0.0, 261.78], ['08/25/2021', 0.0, 253.33], ['09/27/2021', 0.0, 278.67], ['10/25/2021', 0.0, 236.44], ['11/26/2021', 0.0, 270.22], ['12/27/2021', 0.0, 261.78], ['01/25/2022', 0.0, 244.89], ['02/25/2022', 0.0, 261.78], ['03/25/2022', 0.0, 236.44], ['04/25/2022', 0.0, 261.78], ['05/25/2022', 0.0, 253.33], ['06/27/2022', 0.0, 278.67], ['07/25/2022', 0.0, 236.44], ['08/25/2022', 0.0, 261.78], ['09/26/2022', 0.0, 270.22], ['10/25/2022', 0.0, 244.89], ['11/25/2022', 0.0, 261.78], ['12/27/2022', 0.0, 270.22], ['01/25/2023', 0.0, 244.89], ['02/27/2023', 0.0, 278.67], ['03/27/2023', 0.0, 236.44], ['04/25/2023', 0.0, 244.89], ['05/25/2023', 0.0, 253.33], ['06/26/2023', 0.0, 270.22], ['07/25/2023', 0.0, 244.89], ['08/25/2023', 0.0, 261.78], ['09/25/2023', 0.0, 261.78], ['10/25/2023', 0.0, 253.33], ['11/27/2023', 0.0, 278.67], ['12/26/2023', 0.0, 244.89], ['01/25/2024', 0.0, 253.33], ['02/26/2024', 0.0, 270.22], ['03/25/2024', 0.0, 236.44], ['04/25/2024', 0.0, 261.78], ['05/28/2024', 0.0, 278.67], ['06/25/2024', 0.0, 236.44], ['07/25/2024', 11072.68, 253.33], ['08/26/2024', 14961.68, 264.24], ['09/25/2024', 14864.29, 240.14], ['10/25/2024', 14727.14, 232.61], ['11/25/2024', 14572.35, 232.65], ['12/26/2024', 14438.77, 225.03], ['01/27/2025', 14287.07, 224.48], ['02/25/2025', 14213.2, 196.44], ['03/25/2025', 14101.46, 182.94], ['04/25/2025', 13915.88, 195.16], ['05/27/2025', 13769.1, 193.94], ['06/25/2025', 13696.7, 169.01], ['07/25/2025', 13551.97, 167.9], ['08/25/2025', 13409.66, 166.4], ['09/25/2025', 13286.31, 159.38], ['10/27/2025', 12956.47, 209.1], ['11/25/2025', 12906.21, 181.06], ['12/26/2025', 12741.92, 184.57], ['01/26/2026', 12625.0, 175.7], ['02/25/2026', 12530.34, 161.53], ['03/25/2026', 12458.36, 142.89], ['04/27/2026', 12236.16, 159.18], ['05/26/2026', 12208.19, 131.92], ['06/25/2026', 12071.6, 128.25], ['07/27/2026', 11918.68, 128.13], ['08/25/2026', 11869.36, 108.36], ['09/25/2026', 11719.8, 107.57], ['10/26/2026', 11611.86, 99.42], ['11/25/2026', 11523.18, 88.39], ['12/28/2026', 11358.12, 88.7], ['01/25/2027', 11343.16, 68.12], ['02/25/2027', 11176.25, 67.53], ['03/25/2027', 11128.64, 53.97], ['04/26/2027', 10952.47, 53.69], ['05/25/2027', 10905.43, 41.52], ['06/25/2027', 10768.87, 36.8], ['07/26/2027', 10669.25, 29.31], ['08/25/2027', 10587.71, 21.18], ['09/27/2027', 10437.53, 15.45], ['10/25/2027', 10425.2, 6.55], ['11/26/2027', 2.01, 0.0]];
        var CPR02CDR10 = [['08/25/2011', 0.0, 252.84], ['09/26/2011', 0.0, 270.22], ['10/25/2011', 0.0, 244.89], ['11/25/2011', 0.0, 261.78], ['12/27/2011', 0.0, 270.22], ['01/25/2012', 0.0, 244.89], ['02/27/2012', 0.0, 278.67], ['03/26/2012', 0.0, 236.44], ['04/25/2012', 0.0, 253.33], ['05/25/2012', 0.0, 253.33], ['06/25/2012', 0.0, 261.78], ['07/25/2012', 0.0, 253.33], ['08/27/2012', 0.0, 278.67], ['09/25/2012', 0.0, 244.89], ['10/25/2012', 0.0, 253.33], ['11/26/2012', 0.0, 270.22], ['12/26/2012', 0.0, 253.33], ['01/25/2013', 0.0, 253.33], ['02/25/2013', 0.0, 261.78], ['03/25/2013', 0.0, 236.44], ['04/25/2013', 0.0, 261.78], ['05/28/2013', 0.0, 278.67], ['06/25/2013', 0.0, 236.44], ['07/25/2013', 0.0, 253.33], ['08/26/2013', 0.0, 270.22], ['09/25/2013', 0.0, 253.33], ['10/25/2013', 0.0, 253.33], ['11/25/2013', 0.0, 261.78], ['12/26/2013', 0.0, 261.78], ['01/27/2014', 0.0, 270.22], ['02/25/2014', 0.0, 244.89], ['03/25/2014', 0.0, 236.44], ['04/25/2014', 0.0, 261.78], ['05/27/2014', 0.0, 270.22], ['06/25/2014', 0.0, 244.89], ['07/25/2014', 0.0, 253.33], ['08/25/2014', 0.0, 261.78], ['09/25/2014', 0.0, 261.78], ['10/27/2014', 0.0, 270.22], ['11/25/2014', 0.0, 244.89], ['12/26/2014', 0.0, 261.78], ['01/26/2015', 0.0, 261.78], ['02/25/2015', 0.0, 253.33], ['03/25/2015', 0.0, 236.44], ['04/27/2015', 0.0, 278.67], ['05/26/2015', 0.0, 244.89], ['06/25/2015', 0.0, 253.33], ['07/27/2015', 0.0, 270.22], ['08/25/2015', 0.0, 244.89], ['09/25/2015', 0.0, 261.78], ['10/26/2015', 0.0, 261.78], ['11/25/2015', 0.0, 253.33], ['12/28/2015', 0.0, 278.67], ['01/25/2016', 0.0, 236.44], ['02/25/2016', 0.0, 261.78], ['03/25/2016', 0.0, 244.89], ['04/25/2016', 0.0, 261.78], ['05/25/2016', 0.0, 253.33], ['06/27/2016', 0.0, 278.67], ['07/25/2016', 0.0, 236.44], ['08/25/2016', 0.0, 261.78], ['09/26/2016', 0.0, 270.22], ['10/25/2016', 0.0, 244.89], ['11/25/2016', 0.0, 261.78], ['12/27/2016', 0.0, 270.22], ['01/25/2017', 0.0, 244.89], ['02/27/2017', 0.0, 278.67], ['03/27/2017', 0.0, 236.44], ['04/25/2017', 0.0, 244.89], ['05/25/2017', 0.0, 253.33], ['06/26/2017', 0.0, 270.22], ['07/25/2017', 0.0, 244.89], ['08/25/2017', 0.0, 261.78], ['09/25/2017', 0.0, 261.78], ['10/25/2017', 0.0, 253.33], ['11/27/2017', 0.0, 278.67], ['12/26/2017', 0.0, 244.89], ['01/25/2018', 0.0, 253.33], ['02/26/2018', 0.0, 270.22], ['03/26/2018', 0.0, 236.44], ['04/25/2018', 0.0, 253.33], ['05/25/2018', 0.0, 253.33], ['06/25/2018', 0.0, 261.78], ['07/25/2018', 0.0, 253.33], ['08/27/2018', 0.0, 278.67], ['09/25/2018', 0.0, 244.89], ['10/25/2018', 0.0, 253.33], ['11/26/2018', 0.0, 270.22], ['12/26/2018', 0.0, 253.33], ['01/25/2019', 0.0, 253.33], ['02/25/2019', 0.0, 261.78], ['03/25/2019', 0.0, 236.44], ['04/25/2019', 0.0, 261.78], ['05/28/2019', 0.0, 278.67], ['06/25/2019', 0.0, 236.44], ['07/25/2019', 0.0, 253.33], ['08/26/2019', 0.0, 270.22], ['09/25/2019', 0.0, 253.33], ['10/25/2019', 0.0, 253.33], ['11/25/2019', 0.0, 261.78], ['12/26/2019', 0.0, 261.78], ['01/27/2020', 0.0, 270.22], ['02/25/2020', 0.0, 244.89], ['03/25/2020', 0.0, 244.89], ['04/27/2020', 0.0, 278.67], ['05/26/2020', 0.0, 244.89], ['06/25/2020', 0.0, 253.33], ['07/27/2020', 0.0, 270.22], ['08/25/2020', 0.0, 244.89], ['09/25/2020', 0.0, 261.78], ['10/26/2020', 0.0, 261.78], ['11/25/2020', 0.0, 253.33], ['12/28/2020', 0.0, 278.67], ['01/25/2021', 0.0, 236.44], ['02/25/2021', 0.0, 261.78], ['03/25/2021', 0.0, 236.44], ['04/26/2021', 0.0, 270.22], ['05/25/2021', 0.0, 244.89], ['06/25/2021', 0.0, 261.78], ['07/26/2021', 0.0, 261.78], ['08/25/2021', 0.0, 253.33], ['09/27/2021', 0.0, 278.67], ['10/25/2021', 0.0, 236.44], ['11/26/2021', 0.0, 270.22], ['12/27/2021', 0.0, 261.78], ['01/25/2022', 0.0, 244.89], ['02/25/2022', 0.0, 261.78], ['03/25/2022', 0.0, 236.44], ['04/25/2022', 0.0, 261.78], ['05/25/2022', 0.0, 253.33], ['06/27/2022', 0.0, 278.67], ['07/25/2022', 0.0, 236.44], ['08/25/2022', 0.0, 261.78], ['09/26/2022', 0.0, 270.22], ['10/25/2022', 0.0, 244.89], ['11/25/2022', 0.0, 261.78], ['12/27/2022', 0.0, 270.22], ['01/25/2023', 0.0, 244.89], ['02/27/2023', 0.0, 278.67], ['03/27/2023', 0.0, 236.44], ['04/25/2023', 0.0, 244.89], ['05/25/2023', 0.0, 253.33], ['06/26/2023', 0.0, 270.22], ['07/25/2023', 0.0, 244.89], ['08/25/2023', 0.0, 261.78], ['09/25/2023', 0.0, 261.78], ['10/25/2023', 0.0, 253.33], ['11/27/2023', 0.0, 278.67], ['12/26/2023', 0.0, 325.44], ['01/25/2024', 0.0, 336.67], ['02/26/2024', 0.0, 359.11], ['03/25/2024', 0.0, 314.22], ['04/25/2024', 0.0, 347.89], ['05/28/2024', 0.0, 370.33], ['06/25/2024', 0.0, 314.22], ['07/25/2024', 0.0, 336.67], ['08/26/2024', 0.0, 359.11], ['09/25/2024', 0.0, 336.67], ['10/25/2024', 0.0, 336.67], ['11/25/2024', 0.0, 347.89], ['12/26/2024', 0.0, 347.89], ['01/27/2025', 0.0, 359.11], ['02/25/2025', 0.0, 325.44], ['03/25/2025', 0.0, 314.22], ['04/25/2025', 0.0, 347.89], ['05/27/2025', 0.0, 359.11], ['06/25/2025', 0.0, 325.44], ['07/25/2025', 0.0, 336.67], ['08/25/2025', 0.0, 347.89], ['09/25/2025', 0.0, 347.89], ['10/27/2025', 0.0, 359.11], ['11/25/2025', 0.0, 325.44], ['12/26/2025', 0.0, 347.89], ['01/26/2026', 0.0, 347.89], ['02/25/2026', 0.0, 336.67], ['03/25/2026', 0.0, 314.22], ['04/27/2026', 0.0, 370.33], ['05/26/2026', 0.0, 325.44], ['06/25/2026', 0.0, 336.67], ['07/27/2026', 0.0, 359.11], ['08/25/2026', 0.0, 325.44], ['09/25/2026', 0.0, 347.89], ['10/26/2026', 0.0, 347.89], ['11/25/2026', 0.0, 336.67], ['12/28/2026', 0.0, 370.33], ['01/25/2027', 0.0, 314.22], ['02/25/2027', 0.0, 347.89], ['03/25/2027', 0.0, 314.22], ['04/26/2027', 0.0, 359.11], ['05/25/2027', 0.0, 325.44], ['06/25/2027', 5043.47, 347.89], ['07/26/2027', 7765.42, 344.38], ['08/25/2027', 7692.77, 328.04], ['09/27/2027', 7562.56, 355.15], ['10/25/2027', 7548.57, 296.59], ['11/26/2027', 7407.68, 333.53], ['12/27/2027', 7338.21, 317.96], ['01/25/2028', 7282.82, 292.67], ['02/25/2028', 7173.99, 307.78], ['03/27/2028', 7092.04, 302.79], ['04/25/2028', 7036.96, 278.64], ['05/25/2028', 6943.81, 283.51], ['06/26/2028', 6839.59, 297.42], ['07/25/2028', 6799.7, 265.09], ['08/25/2028', 6697.06, 278.64], ['09/25/2028', 6620.78, 273.98], ['10/25/2028', 6557.65, 260.68], ['11/27/2028', 6446.31, 281.9], ['12/26/2028', 6418.47, 243.53], ['01/25/2029', 6333.97, 247.61], ['02/26/2029', 6239.67, 259.56], ['03/26/2029', 6213.09, 223.2], ['04/25/2029', 6120.66, 234.96], ['05/25/2029', 6051.08, 230.84], ['06/25/2029', 5971.7, 234.32], ['07/25/2029', 5914.16, 222.74], ['08/27/2029', 5816.09, 240.63], ['09/25/2029', 5790.26, 207.68], ['10/25/2029', 5714.26, 210.94], ['11/26/2029', 5629.51, 220.9], ['12/26/2029', 5584.57, 203.3], ['01/25/2030', 5520.76, 199.54], ['02/25/2030', 5448.32, 202.35], ['03/25/2030', 5413.59, 179.35], ['04/25/2030', 5324.41, 194.8], ['05/28/2030', 5245.66, 203.42], ['06/25/2030', 5229.46, 169.3], ['07/25/2030', 5152.16, 177.88], ['08/26/2030', 5076.07, 186.03], ['09/25/2030', 5034.56, 170.99], ['10/25/2030', 4976.7, 167.6], ['11/25/2030', 4911.16, 169.72], ['12/26/2030', 4854.71, 166.3], ['01/27/2031', 4791.07, 168.18], ['02/25/2031', 4759.08, 149.3], ['03/25/2031', 4711.79, 141.16], ['04/25/2031', 4634.82, 153.0], ['05/27/2031', 4573.98, 154.61], ['06/25/2031', 4542.28, 137.14], ['07/25/2031', 4482.22, 138.81], ['08/25/2031', 4422.81, 140.32], ['09/25/2031', 4371.1, 137.24], ['10/27/2031', 4313.68, 138.53], ['11/25/2031', 4282.14, 122.73], ['12/26/2031', 4217.8, 128.22], ['01/26/2032', 4166.74, 125.28], ['02/25/2032', 4124.31, 118.44], ['03/25/2032', 4082.42, 111.8], ['04/26/2032', 4016.4, 120.44], ['05/25/2032', 3987.56, 106.53], ['06/25/2032', 3929.29, 111.11], ['07/26/2032', 3883.46, 108.37], ['08/25/2032', 3843.79, 102.26], ['09/27/2032', 3782.19, 109.64], ['10/25/2032', 3765.31, 90.65], ['11/26/2032', 3699.75, 100.9], ['12/27/2032', 3661.73, 95.17], ['01/25/2033', 3629.1, 86.65], ['02/25/2033', 3575.56, 90.1], ['03/25/2033', 3548.38, 79.13], ['04/25/2033', 3491.36, 85.14], ['05/25/2033', 3454.92, 80.04], ['06/27/2033', 3400.0, 85.49], ['07/25/2033', 3382.66, 70.4], ['08/25/2033', 3328.43, 75.59], ['09/26/2033', 3284.73, 75.64], ['10/25/2033', 3257.68, 66.41], ['11/25/2033', 3209.3, 68.72], ['12/27/2033', 3165.9, 68.63], ['01/25/2034', 3140.48, 60.14], ['02/27/2034', 3087.11, 66.11], ['03/27/2034', 3070.04, 54.15], ['04/25/2034', 3029.65, 54.09], ['05/25/2034', 2989.35, 53.91], ['06/26/2034', 2945.72, 55.36], ['07/25/2034', 2921.25, 48.25], ['08/25/2034', 2879.29, 49.55], ['09/25/2034', 2844.14, 47.54], ['10/25/2034', 2812.98, 44.09], ['11/27/2034', 2769.1, 46.42], ['12/26/2034', 2747.86, 38.99], ['01/25/2035', 2710.49, 38.48], ['02/26/2035', 2670.94, 39.1], ['03/26/2035', 2649.98, 32.54], ['04/25/2035', 2611.66, 33.08], ['05/25/2035', 2580.08, 31.32], ['06/25/2035', 2545.51, 30.57], ['07/25/2035', 2517.46, 27.87], ['08/27/2035', 2479.15, 28.79], ['09/25/2035', 2460.07, 23.69], ['10/25/2035', 2425.87, 22.85], ['11/26/2035', 2390.64, 22.63], ['12/26/2035', 2369.52, 19.6], ['01/25/2036', 2341.58, 18.01], ['02/25/2036', 2317.34, 16.98], ['03/25/2036', 2301.71, 14.37], ['04/25/2036', 2300.8, 13.76], ['05/27/2036', 2331.61, 12.56], ['06/25/2036', 2397.02, 9.86], ['07/25/2036', 2208.44, 8.59], ['08/25/2036', 2245.23, 7.34], ['09/25/2036', 2878.5, 5.77], ['10/27/2036', 5421.25, 3.89]];
        var CPR02CDR12 = [['08/25/2011', 0.0, 252.84], ['09/26/2011', 0.0, 270.22], ['10/25/2011', 0.0, 244.89], ['11/25/2011', 0.0, 261.78], ['12/27/2011', 0.0, 270.22], ['01/25/2012', 0.0, 244.89], ['02/27/2012', 0.0, 278.67], ['03/26/2012', 0.0, 236.44], ['04/25/2012', 0.0, 253.33], ['05/25/2012', 0.0, 253.33], ['06/25/2012', 0.0, 261.78], ['07/25/2012', 0.0, 253.33], ['08/27/2012', 0.0, 278.67], ['09/25/2012', 0.0, 244.89], ['10/25/2012', 0.0, 253.33], ['11/26/2012', 0.0, 270.22], ['12/26/2012', 0.0, 253.33], ['01/25/2013', 0.0, 253.33], ['02/25/2013', 0.0, 261.78], ['03/25/2013', 0.0, 236.44], ['04/25/2013', 0.0, 261.78], ['05/28/2013', 0.0, 278.67], ['06/25/2013', 0.0, 236.44], ['07/25/2013', 0.0, 253.33], ['08/26/2013', 0.0, 270.22], ['09/25/2013', 0.0, 253.33], ['10/25/2013', 0.0, 253.33], ['11/25/2013', 0.0, 261.78], ['12/26/2013', 0.0, 261.78], ['01/27/2014', 0.0, 270.22], ['02/25/2014', 0.0, 244.89], ['03/25/2014', 0.0, 236.44], ['04/25/2014', 0.0, 261.78], ['05/27/2014', 0.0, 270.22], ['06/25/2014', 0.0, 244.89], ['07/25/2014', 0.0, 253.33], ['08/25/2014', 0.0, 261.78], ['09/25/2014', 0.0, 261.78], ['10/27/2014', 0.0, 270.22], ['11/25/2014', 0.0, 244.89], ['12/26/2014', 0.0, 261.78], ['01/26/2015', 0.0, 261.78], ['02/25/2015', 0.0, 253.33], ['03/25/2015', 0.0, 236.44], ['04/27/2015', 0.0, 278.67], ['05/26/2015', 0.0, 244.89], ['06/25/2015', 0.0, 253.33], ['07/27/2015', 0.0, 270.22], ['08/25/2015', 0.0, 244.89], ['09/25/2015', 0.0, 261.78], ['10/26/2015', 0.0, 261.78], ['11/25/2015', 0.0, 253.33], ['12/28/2015', 0.0, 278.67], ['01/25/2016', 0.0, 236.44], ['02/25/2016', 0.0, 261.78], ['03/25/2016', 0.0, 244.89], ['04/25/2016', 0.0, 261.78], ['05/25/2016', 0.0, 253.33], ['06/27/2016', 0.0, 278.67], ['07/25/2016', 0.0, 236.44], ['08/25/2016', 0.0, 261.78], ['09/26/2016', 0.0, 270.22], ['10/25/2016', 0.0, 244.89], ['11/25/2016', 0.0, 261.78], ['12/27/2016', 0.0, 270.22], ['01/25/2017', 0.0, 244.89], ['02/27/2017', 0.0, 278.67], ['03/27/2017', 0.0, 236.44], ['04/25/2017', 0.0, 244.89], ['05/25/2017', 0.0, 253.33], ['06/26/2017', 0.0, 270.22], ['07/25/2017', 0.0, 244.89], ['08/25/2017', 0.0, 261.78], ['09/25/2017', 0.0, 261.78], ['10/25/2017', 0.0, 253.33], ['11/27/2017', 0.0, 278.67], ['12/26/2017', 0.0, 244.89], ['01/25/2018', 0.0, 253.33], ['02/26/2018', 0.0, 270.22], ['03/26/2018', 0.0, 236.44], ['04/25/2018', 0.0, 253.33], ['05/25/2018', 0.0, 253.33], ['06/25/2018', 0.0, 261.78], ['07/25/2018', 0.0, 253.33], ['08/27/2018', 0.0, 278.67], ['09/25/2018', 0.0, 244.89], ['10/25/2018', 0.0, 253.33], ['11/26/2018', 0.0, 270.22], ['12/26/2018', 0.0, 252.95], ['01/25/2019', 0.0, 249.3], ['02/25/2019', 0.0, 253.89], ['03/25/2019', 0.0, 225.98], ['04/25/2019', 0.0, 246.6], ['05/28/2019', 0.0, 258.69], ['06/25/2019', 0.0, 216.27], ['07/25/2019', 0.0, 228.39], ['08/26/2019', 0.0, 240.07], ['09/25/2019', 0.0, 221.77], ['10/25/2019', 0.0, 218.54], ['11/25/2019', 0.0, 222.54], ['12/26/2019', 0.0, 219.28], ['01/27/2020', 0.0, 223.03], ['02/25/2020', 0.0, 199.15], ['03/25/2020', 0.0, 196.25], ['04/27/2020', 0.0, 220.06], ['05/26/2020', 0.0, 190.52], ['06/25/2020', 0.0, 194.21], ['07/27/2020', 0.0, 204.12], ['08/25/2020', 0.0, 182.25], ['09/25/2020', 0.0, 191.96], ['10/26/2020', 0.0, 189.13], ['11/25/2020', 0.0, 180.32], ['12/28/2020', 0.0, 195.43], ['01/25/2021', 0.0, 163.34], ['02/25/2021', 0.0, 178.2], ['03/25/2021', 0.0, 158.56], ['04/26/2021', 0.0, 178.56], ['05/25/2021', 0.0, 159.4], ['06/25/2021', 0.0, 167.88], ['07/26/2021', 0.0, 165.38], ['08/25/2021', 0.0, 157.65], ['09/27/2021', 0.0, 170.82], ['10/25/2021', 0.0, 142.74], ['11/26/2021', 0.0, 160.71], ['12/27/2021', 0.0, 153.33], ['01/25/2022', 0.0, 141.26], ['02/25/2022', 0.0, 148.72], ['03/25/2022', 0.0, 132.27], ['04/25/2022', 0.0, 144.22], ['05/25/2022', 0.0, 137.42], ['06/27/2022', 0.0, 148.84], ['07/25/2022', 0.0, 165.23], ['08/25/2022', 0.0, 179.99], ['09/26/2022', 0.0, 182.76], ['10/25/2022', 0.0, 162.89], ['11/25/2022', 0.0, 171.3], ['12/27/2022', 0.0, 173.91], ['01/25/2023', 0.0, 155.0], ['02/27/2023', 0.0, 173.53], ['03/27/2023', 0.0, 144.81], ['04/25/2023', 0.0, 147.58], ['05/25/2023', 0.0, 150.2], ['06/26/2023', 0.0, 157.6], ['07/25/2023', 0.0, 140.46], ['08/25/2023', 0.0, 147.7], ['09/25/2023', 0.0, 145.27], ['10/25/2023', 0.0, 138.25], ['11/27/2023', 0.0, 149.57], ['12/26/2023', 0.0, 129.23], ['01/25/2024', 0.0, 131.49], ['02/26/2024', 0.0, 137.92], ['03/25/2024', 0.0, 118.65], ['04/25/2024', 0.0, 129.2], ['05/28/2024', 0.0, 135.22], ['06/25/2024', 0.0, 112.77], ['07/25/2024', 0.0, 118.82], ['08/26/2024', 0.0, 124.61], ['09/25/2024', 0.0, 114.82], ['10/25/2024', 0.0, 112.88], ['11/25/2024', 0.0, 114.66], ['12/26/2024', 0.0, 112.69], ['01/27/2025', 0.0, 114.33], ['02/25/2025', 0.0, 101.82], ['03/25/2025', 0.0, 96.63], ['04/25/2025', 0.0, 105.16], ['05/27/2025', 0.0, 106.67], ['06/25/2025', 0.0, 94.97], ['07/25/2025', 0.0, 96.55], ['08/25/2025', 0.0, 98.03], ['09/25/2025', 0.0, 96.31], ['10/27/2025', 0.0, 97.67], ['11/25/2025', 0.0, 86.94], ['12/26/2025', 0.0, 91.3], ['01/26/2026', 0.0, 89.68], ['02/25/2026', 0.0, 85.24], ['03/25/2026', 0.0, 78.14], ['04/27/2026', 0.0, 90.47], ['05/26/2026', 0.0, 78.06], ['06/25/2026', 0.0, 79.31], ['07/27/2026', 0.0, 83.07], ['08/25/2026', 0.0, 73.9], ['09/25/2026', 0.0, 77.58], ['10/26/2026', 0.0, 76.16], ['11/25/2026', 0.0, 72.34], ['12/28/2026', 0.0, 78.12], ['01/25/2027', 0.0, 65.04], ['02/25/2027', 0.0, 70.7], ['03/25/2027', 0.0, 62.67], ['04/26/2027', 0.0, 70.31], ['05/25/2027', 0.0, 62.52], ['06/25/2027', 0.0, 65.59], ['07/26/2027', 0.0, 64.35], ['08/25/2027', 0.0, 61.1], ['09/27/2027', 0.0, 65.94], ['10/25/2027', 0.0, 54.87], ['11/26/2027', 0.0, 61.53], ['12/27/2027', 0.0, 58.45], ['01/25/2028', 0.0, 53.63], ['02/25/2028', 0.0, 56.23], ['03/27/2028', 0.0, 55.14], ['04/25/2028', 0.0, 50.58], ['05/25/2028', 0.0, 51.31], ['06/26/2028', 0.0, 53.66], ['07/25/2028', 0.0, 47.67], ['08/25/2028', 0.0, 49.96], ['09/25/2028', 0.0, 48.96], ['10/25/2028', 0.0, 46.44], ['11/27/2028', 0.0, 50.06], ['12/26/2028', 0.0, 43.1], ['01/25/2029', 0.0, 43.7], ['02/26/2029', 0.0, 45.67], ['03/26/2029', 0.0, 39.14], ['04/25/2029', 0.0, 41.09], ['05/25/2029', 0.0, 40.25], ['06/25/2029', 0.0, 40.74], ['07/25/2029', 0.0, 38.61], ['08/27/2029', 0.0, 41.59], ['09/25/2029', 0.0, 35.77], ['10/25/2029', 0.0, 36.24], ['11/26/2029', 0.0, 37.84], ['12/26/2029', 0.0, 34.72], ['01/25/2030', 0.0, 33.98], ['02/25/2030', 0.0, 34.36], ['03/25/2030', 0.0, 30.37], ['04/25/2030', 0.0, 32.9], ['05/28/2030', 0.0, 34.26], ['06/25/2030', 0.0, 28.43], ['07/25/2030', 0.0, 29.8], ['08/26/2030', 0.0, 31.09], ['09/25/2030', 0.0, 28.49], ['10/25/2030', 0.0, 27.86], ['11/25/2030', 0.0, 28.14], ['12/26/2030', 0.0, 27.5], ['01/27/2031', 0.0, 27.74], ['02/25/2031', 0.0, 24.56], ['03/25/2031', 0.0, 23.17], ['04/25/2031', 0.0, 25.07], ['05/27/2031', 0.0, 25.27], ['06/25/2031', 0.0, 22.36], ['07/25/2031', 0.0, 22.59], ['08/25/2031', 0.0, 22.79], ['09/25/2031', 0.0, 22.25], ['10/27/2031', 0.0, 22.41], ['11/25/2031', 0.0, 19.81], ['12/26/2031', 0.0, 20.67], ['01/26/2032', 0.0, 20.16], ['02/25/2032', 0.0, 19.03], ['03/25/2032', 0.0, 17.93], ['04/26/2032', 0.0, 19.3], ['05/25/2032', 0.0, 17.04], ['06/25/2032', 0.0, 17.76], ['07/26/2032', 0.0, 17.3], ['08/25/2032', 0.0, 16.31], ['09/27/2032', 0.0, 17.47], ['10/25/2032', 0.0, 14.43], ['11/26/2032', 0.0, 16.06], ['12/27/2032', 0.0, 15.14], ['01/25/2033', 0.0, 13.78], ['02/25/2033', 0.0, 14.33], ['03/25/2033', 0.0, 12.58], ['04/25/2033', 0.0, 13.55], ['05/25/2033', 0.0, 12.75], ['06/27/2033', 0.0, 13.63], ['07/25/2033', 0.0, 11.23], ['08/25/2033', 0.0, 12.08], ['09/26/2033', 0.0, 12.1], ['10/25/2033', 0.0, 10.64], ['11/25/2033', 0.0, 11.04], ['12/27/2033', 0.0, 11.05], ['01/25/2034', 0.0, 9.71], ['02/27/2034', 0.0, 10.71], ['03/27/2034', 0.0, 8.8], ['04/25/2034', 0.0, 8.83], ['05/25/2034', 0.0, 8.85], ['06/26/2034', 0.0, 9.13], ['07/25/2034', 0.0, 8.0], ['08/25/2034', 0.0, 8.27], ['09/25/2034', 0.0, 7.99], ['10/25/2034', 0.0, 7.47], ['11/27/2034', 0.0, 7.94], ['12/26/2034', 0.0, 6.73], ['01/25/2035', 0.0, 6.71], ['02/26/2035', 0.0, 6.9], ['03/26/2035', 0.0, 5.81], ['04/25/2035', 0.0, 6.0], ['05/25/2035', 0.0, 5.77], ['06/25/2035', 0.0, 5.74], ['07/25/2035', 0.0, 5.33], ['08/27/2035', 0.0, 5.63], ['09/25/2035', 0.0, 4.74], ['10/25/2035', 0.0, 4.7], ['11/26/2035', 0.0, 4.8], ['12/26/2035', 0.0, 4.3], ['01/25/2036', 0.0, 4.11], ['02/25/2036', 0.0, 4.06], ['03/25/2036', 0.0, 3.62], ['04/25/2036', 0.0, 3.69], ['05/27/2036', 0.0, 3.62], ['06/25/2036', 0.0, 3.11], ['07/25/2036', 0.0, 3.06], ['08/25/2036', 0.0, 2.99], ['09/25/2036', 0.0, 2.83], ['10/27/2036', 0.0, 2.75], ['11/25/2036', 0.0, 2.35], ['12/26/2036', 0.0, 2.34], ['01/26/2037', 0.0, 2.12], ['02/25/2037', 0.0, 0.25], ['03/25/2037', 0.0, 0.0], ['04/27/2037', 0.0, 0.0], ['05/26/2037', 0.0, 0.0], ['06/25/2037', 0.0, 0.0], ['07/27/2037', 0.0, 0.0], ['08/25/2037', 0.0, 0.0], ['09/25/2037', 0.0, 0.0], ['10/26/2037', 0.0, 0.0]];
        var CPR02CDR14 = [['08/25/2011', 0.0, 252.84], ['09/26/2011', 0.0, 270.22], ['10/25/2011', 0.0, 244.89], ['11/25/2011', 0.0, 261.78], ['12/27/2011', 0.0, 270.22], ['01/25/2012', 0.0, 244.89], ['02/27/2012', 0.0, 278.67], ['03/26/2012', 0.0, 236.44], ['04/25/2012', 0.0, 253.33], ['05/25/2012', 0.0, 253.33], ['06/25/2012', 0.0, 261.78], ['07/25/2012', 0.0, 253.33], ['08/27/2012', 0.0, 278.67], ['09/25/2012', 0.0, 244.89], ['10/25/2012', 0.0, 253.33], ['11/26/2012', 0.0, 270.22], ['12/26/2012', 0.0, 253.33], ['01/25/2013', 0.0, 253.33], ['02/25/2013', 0.0, 261.78], ['03/25/2013', 0.0, 236.44], ['04/25/2013', 0.0, 261.78], ['05/28/2013', 0.0, 278.67], ['06/25/2013', 0.0, 236.44], ['07/25/2013', 0.0, 253.33], ['08/26/2013', 0.0, 270.22], ['09/25/2013', 0.0, 253.33], ['10/25/2013', 0.0, 253.33], ['11/25/2013', 0.0, 261.78], ['12/26/2013', 0.0, 261.78], ['01/27/2014', 0.0, 270.22], ['02/25/2014', 0.0, 244.89], ['03/25/2014', 0.0, 236.44], ['04/25/2014', 0.0, 261.78], ['05/27/2014', 0.0, 270.22], ['06/25/2014', 0.0, 244.89], ['07/25/2014', 0.0, 253.33], ['08/25/2014', 0.0, 261.78], ['09/25/2014', 0.0, 261.78], ['10/27/2014', 0.0, 270.22], ['11/25/2014', 0.0, 244.89], ['12/26/2014', 0.0, 261.78], ['01/26/2015', 0.0, 261.78], ['02/25/2015', 0.0, 253.33], ['03/25/2015', 0.0, 236.44], ['04/27/2015', 0.0, 278.67], ['05/26/2015', 0.0, 244.89], ['06/25/2015', 0.0, 253.33], ['07/27/2015', 0.0, 270.22], ['08/25/2015', 0.0, 244.89], ['09/25/2015', 0.0, 261.78], ['10/26/2015', 0.0, 261.78], ['11/25/2015', 0.0, 253.33], ['12/28/2015', 0.0, 278.67], ['01/25/2016', 0.0, 236.44], ['02/25/2016', 0.0, 261.78], ['03/25/2016', 0.0, 244.89], ['04/25/2016', 0.0, 261.78], ['05/25/2016', 0.0, 245.67], ['06/27/2016', 0.0, 261.95], ['07/25/2016', 0.0, 215.27], ['08/25/2016', 0.0, 230.82], ['09/26/2016', 0.0, 230.57], ['10/25/2016', 0.0, 202.06], ['11/25/2016', 0.0, 208.8], ['12/27/2016', 0.0, 208.18], ['01/25/2017', 0.0, 182.09], ['02/27/2017', 0.0, 199.89], ['03/27/2017', 0.0, 163.43], ['04/25/2017', 0.0, 163.06], ['05/25/2017', 0.0, 162.34], ['06/26/2017', 0.0, 166.48], ['07/25/2017', 0.0, 144.88], ['08/25/2017', 0.0, 148.61], ['09/25/2017', 0.0, 142.41], ['10/25/2017', 0.0, 131.92], ['11/27/2017', 0.0, 138.73], ['12/26/2017', 0.0, 116.36], ['01/25/2018', 0.0, 114.77], ['02/26/2018', 0.0, 116.52], ['03/26/2018', 0.0, 96.84], ['04/25/2018', 0.0, 98.43], ['05/25/2018', 0.0, 93.15], ['06/25/2018', 0.0, 90.89], ['07/25/2018', 0.0, 82.83], ['08/27/2018', 0.0, 85.58], ['09/25/2018', 0.0, 70.38], ['10/25/2018', 0.0, 67.94], ['11/26/2018', 0.0, 67.35], ['12/26/2018', 0.0, 58.39], ['01/25/2019', 0.0, 53.74], ['02/25/2019', 0.0, 50.8], ['03/25/2019', 0.0, 41.66], ['04/25/2019', 0.0, 41.57], ['05/28/2019', 0.0, 39.43], ['06/25/2019', 0.0, 29.41], ['07/25/2019', 0.0, 27.3], ['08/26/2019', 0.0, 24.68], ['09/25/2019', 0.0, 19.02], ['10/25/2019', 0.0, 14.98], ['11/25/2019', 0.0, 11.38], ['12/26/2019', 0.0, 7.33], ['01/27/2020', 0.0, 3.45]];
        var CPR04CDR05 = [['08/25/2011', 0.0, 252.84], ['09/26/2011', 0.0, 270.22], ['10/25/2011', 0.0, 244.89], ['11/25/2011', 0.0, 261.78], ['12/27/2011', 0.0, 270.22], ['01/25/2012', 0.0, 244.89], ['02/27/2012', 0.0, 278.67], ['03/26/2012', 0.0, 236.44], ['04/25/2012', 0.0, 253.33], ['05/25/2012', 0.0, 253.33], ['06/25/2012', 0.0, 261.78], ['07/25/2012', 0.0, 253.33], ['08/27/2012', 0.0, 278.67], ['09/25/2012', 0.0, 244.89], ['10/25/2012', 0.0, 253.33], ['11/26/2012', 0.0, 270.22], ['12/26/2012', 0.0, 253.33], ['01/25/2013', 0.0, 253.33], ['02/25/2013', 0.0, 261.78], ['03/25/2013', 0.0, 236.44], ['04/25/2013', 0.0, 261.78], ['05/28/2013', 0.0, 278.67], ['06/25/2013', 0.0, 236.44], ['07/25/2013', 0.0, 253.33], ['08/26/2013', 0.0, 270.22], ['09/25/2013', 0.0, 253.33], ['10/25/2013', 0.0, 253.33], ['11/25/2013', 0.0, 261.78], ['12/26/2013', 0.0, 261.78], ['01/27/2014', 0.0, 270.22], ['02/25/2014', 0.0, 244.89], ['03/25/2014', 0.0, 236.44], ['04/25/2014', 0.0, 261.78], ['05/27/2014', 0.0, 270.22], ['06/25/2014', 0.0, 244.89], ['07/25/2014', 0.0, 253.33], ['08/25/2014', 0.0, 261.78], ['09/25/2014', 0.0, 261.78], ['10/27/2014', 0.0, 270.22], ['11/25/2014', 0.0, 244.89], ['12/26/2014', 0.0, 261.78], ['01/26/2015', 0.0, 261.78], ['02/25/2015', 0.0, 253.33], ['03/25/2015', 0.0, 236.44], ['04/27/2015', 0.0, 278.67], ['05/26/2015', 0.0, 244.89], ['06/25/2015', 0.0, 253.33], ['07/27/2015', 0.0, 270.22], ['08/25/2015', 0.0, 244.89], ['09/25/2015', 0.0, 261.78], ['10/26/2015', 0.0, 261.78], ['11/25/2015', 0.0, 253.33], ['12/28/2015', 0.0, 278.67], ['01/25/2016', 0.0, 236.44], ['02/25/2016', 0.0, 261.78], ['03/25/2016', 0.0, 244.89], ['04/25/2016', 0.0, 261.78], ['05/25/2016', 0.0, 253.33], ['06/27/2016', 0.0, 278.67], ['07/25/2016', 0.0, 236.44], ['08/25/2016', 0.0, 261.78], ['09/26/2016', 0.0, 270.22], ['10/25/2016', 0.0, 244.89], ['11/25/2016', 0.0, 261.78], ['12/27/2016', 0.0, 270.22], ['01/25/2017', 0.0, 244.89], ['02/27/2017', 0.0, 278.67], ['03/27/2017', 0.0, 236.44], ['04/25/2017', 0.0, 244.89], ['05/25/2017', 0.0, 253.33], ['06/26/2017', 0.0, 270.22], ['07/25/2017', 0.0, 244.89], ['08/25/2017', 0.0, 261.78], ['09/25/2017', 0.0, 261.78], ['10/25/2017', 0.0, 253.33], ['11/27/2017', 0.0, 278.67], ['12/26/2017', 0.0, 244.89], ['01/25/2018', 0.0, 253.33], ['02/26/2018', 0.0, 270.22], ['03/26/2018', 0.0, 236.44], ['04/25/2018', 0.0, 253.33], ['05/25/2018', 0.0, 253.33], ['06/25/2018', 0.0, 261.78], ['07/25/2018', 0.0, 253.33], ['08/27/2018', 0.0, 278.67], ['09/25/2018', 0.0, 244.89], ['10/25/2018', 0.0, 253.33], ['11/26/2018', 0.0, 270.22], ['12/26/2018', 0.0, 253.33], ['01/25/2019', 0.0, 253.33], ['02/25/2019', 0.0, 261.78], ['03/25/2019', 0.0, 236.44], ['04/25/2019', 0.0, 261.78], ['05/28/2019', 0.0, 278.67], ['06/25/2019', 0.0, 236.44], ['07/25/2019', 0.0, 253.33], ['08/26/2019', 0.0, 270.22], ['09/25/2019', 0.0, 253.33], ['10/25/2019', 0.0, 253.33], ['11/25/2019', 0.0, 261.78], ['12/26/2019', 0.0, 261.78], ['01/27/2020', 0.0, 270.22], ['02/25/2020', 0.0, 244.89], ['03/25/2020', 0.0, 244.89], ['04/27/2020', 0.0, 278.67], ['05/26/2020', 0.0, 244.89], ['06/25/2020', 0.0, 253.33], ['07/27/2020', 0.0, 270.22], ['08/25/2020', 0.0, 244.89], ['09/25/2020', 0.0, 261.78], ['10/26/2020', 0.0, 261.78], ['11/25/2020', 0.0, 253.33], ['12/28/2020', 0.0, 278.67], ['01/25/2021', 0.0, 236.44], ['02/25/2021', 0.0, 261.78], ['03/25/2021', 0.0, 236.44], ['04/26/2021', 0.0, 270.22], ['05/25/2021', 0.0, 244.89], ['06/25/2021', 0.0, 261.78], ['07/26/2021', 0.0, 261.78], ['08/25/2021', 0.0, 253.33], ['09/27/2021', 0.0, 278.67], ['10/25/2021', 0.0, 236.44], ['11/26/2021', 0.0, 270.22], ['12/27/2021', 0.0, 261.78], ['01/25/2022', 0.0, 244.89], ['02/25/2022', 0.0, 261.78], ['03/25/2022', 0.0, 236.44], ['04/25/2022', 0.0, 261.78], ['05/25/2022', 0.0, 253.33], ['06/27/2022', 0.0, 278.67], ['07/25/2022', 0.0, 236.44], ['08/25/2022', 13493.69, 261.78], ['09/26/2022', 19214.98, 262.93], ['10/25/2022', 19061.05, 228.87], ['11/25/2022', 18905.05, 234.67], ['12/27/2022', 18737.71, 232.03], ['01/25/2023', 18563.93, 201.1], ['02/27/2023', 18390.08, 218.49], ['03/27/2023', 18242.69, 176.69], ['04/25/2023', 18094.44, 174.06], ['05/25/2023', 17948.89, 170.9], ['06/26/2023', 17804.17, 172.59], ['07/25/2023', 17661.41, 147.69], ['08/25/2023', 17519.76, 148.63], ['09/25/2023', 17379.21, 139.46], ['10/25/2023', 17239.77, 126.15], ['11/27/2023', 17101.42, 129.16], ['12/26/2023', 16960.76, 105.13], ['01/25/2024', 16824.43, 100.16], ['02/26/2024', 16688.79, 97.74], ['03/25/2024', 16554.14, 77.63], ['04/25/2024', 16421.11, 77.28], ['05/28/2024', 16289.12, 73.12], ['06/25/2024', 16158.16, 54.34], ['07/25/2024', 16028.22, 50.03], ['08/26/2024', 15899.3, 44.7], ['09/25/2024', 15770.23, 33.85], ['10/25/2024', 15642.19, 25.86], ['11/25/2024', 15516.27, 18.54], ['12/26/2024', 15391.34, 10.41], ['01/27/2025', 4497.69, 2.43]];
        var CPR06CDR05 = [['08/25/2011', 0.0, 252.84], ['09/26/2011', 0.0, 270.22], ['10/25/2011', 0.0, 244.89], ['11/25/2011', 0.0, 261.78], ['12/27/2011', 0.0, 270.22], ['01/25/2012', 0.0, 244.89], ['02/27/2012', 0.0, 278.67], ['03/26/2012', 0.0, 236.44], ['04/25/2012', 0.0, 253.33], ['05/25/2012', 0.0, 253.33], ['06/25/2012', 0.0, 261.78], ['07/25/2012', 0.0, 253.33], ['08/27/2012', 0.0, 278.67], ['09/25/2012', 0.0, 244.89], ['10/25/2012', 0.0, 253.33], ['11/26/2012', 0.0, 270.22], ['12/26/2012', 0.0, 253.33], ['01/25/2013', 0.0, 253.33], ['02/25/2013', 0.0, 261.78], ['03/25/2013', 0.0, 236.44], ['04/25/2013', 0.0, 261.78], ['05/28/2013', 0.0, 278.67], ['06/25/2013', 0.0, 236.44], ['07/25/2013', 0.0, 253.33], ['08/26/2013', 0.0, 270.22], ['09/25/2013', 0.0, 253.33], ['10/25/2013', 0.0, 253.33], ['11/25/2013', 0.0, 261.78], ['12/26/2013', 0.0, 261.78], ['01/27/2014', 0.0, 270.22], ['02/25/2014', 0.0, 244.89], ['03/25/2014', 0.0, 236.44], ['04/25/2014', 0.0, 261.78], ['05/27/2014', 0.0, 270.22], ['06/25/2014', 0.0, 244.89], ['07/25/2014', 0.0, 253.33], ['08/25/2014', 0.0, 261.78], ['09/25/2014', 0.0, 261.78], ['10/27/2014', 0.0, 270.22], ['11/25/2014', 0.0, 244.89], ['12/26/2014', 0.0, 261.78], ['01/26/2015', 0.0, 261.78], ['02/25/2015', 0.0, 253.33], ['03/25/2015', 0.0, 236.44], ['04/27/2015', 0.0, 278.67], ['05/26/2015', 0.0, 244.89], ['06/25/2015', 0.0, 253.33], ['07/27/2015', 0.0, 270.22], ['08/25/2015', 0.0, 244.89], ['09/25/2015', 0.0, 261.78], ['10/26/2015', 0.0, 261.78], ['11/25/2015', 0.0, 253.33], ['12/28/2015', 0.0, 278.67], ['01/25/2016', 0.0, 236.44], ['02/25/2016', 0.0, 261.78], ['03/25/2016', 0.0, 244.89], ['04/25/2016', 0.0, 261.78], ['05/25/2016', 0.0, 253.33], ['06/27/2016', 0.0, 278.67], ['07/25/2016', 0.0, 236.44], ['08/25/2016', 0.0, 261.78], ['09/26/2016', 0.0, 270.22], ['10/25/2016', 0.0, 244.89], ['11/25/2016', 0.0, 261.78], ['12/27/2016', 0.0, 270.22], ['01/25/2017', 0.0, 244.89], ['02/27/2017', 0.0, 278.67], ['03/27/2017', 0.0, 236.44], ['04/25/2017', 0.0, 244.89], ['05/25/2017', 0.0, 253.33], ['06/26/2017', 0.0, 270.22], ['07/25/2017', 0.0, 244.89], ['08/25/2017', 0.0, 261.78], ['09/25/2017', 0.0, 261.78], ['10/25/2017', 0.0, 253.33], ['11/27/2017', 0.0, 278.67], ['12/26/2017', 0.0, 244.89], ['01/25/2018', 0.0, 253.33], ['02/26/2018', 0.0, 270.22], ['03/26/2018', 0.0, 236.44], ['04/25/2018', 0.0, 253.33], ['05/25/2018', 0.0, 253.33], ['06/25/2018', 0.0, 261.78], ['07/25/2018', 0.0, 253.33], ['08/27/2018', 0.0, 278.67], ['09/25/2018', 0.0, 244.89], ['10/25/2018', 0.0, 253.33], ['11/26/2018', 0.0, 270.22], ['12/26/2018', 0.0, 253.33], ['01/25/2019', 0.0, 253.33], ['02/25/2019', 0.0, 261.78], ['03/25/2019', 0.0, 236.44], ['04/25/2019', 0.0, 261.78], ['05/28/2019', 0.0, 278.67], ['06/25/2019', 0.0, 236.44], ['07/25/2019', 0.0, 253.33], ['08/26/2019', 0.0, 270.22], ['09/25/2019', 0.0, 253.33], ['10/25/2019', 0.0, 253.33], ['11/25/2019', 0.0, 261.78], ['12/26/2019', 0.0, 261.78], ['01/27/2020', 0.0, 270.22], ['02/25/2020', 0.0, 244.89], ['03/25/2020', 0.0, 244.89], ['04/27/2020', 0.0, 278.67], ['05/26/2020', 0.0, 244.89], ['06/25/2020', 0.0, 253.33], ['07/27/2020', 0.0, 270.22], ['08/25/2020', 0.0, 244.89], ['09/25/2020', 0.0, 261.78], ['10/26/2020', 0.0, 261.78], ['11/25/2020', 0.0, 253.33], ['12/28/2020', 0.0, 278.67], ['01/25/2021', 18678.45, 236.44], ['02/25/2021', 21832.47, 252.0], ['03/25/2021', 21614.62, 217.29], ['04/26/2021', 21471.25, 236.65], ['05/25/2021', 21455.18, 203.95], ['06/25/2021', 25442.15, 206.78], ['07/26/2021', 21568.7, 193.46], ['08/25/2021', 20602.47, 176.29], ['09/27/2021', 20305.65, 182.43], ['10/25/2021', 20721.56, 145.19], ['11/26/2021', 22844.31, 154.73], ['12/27/2021', 23858.25, 137.94], ['01/25/2022', 24152.27, 117.35], ['02/25/2022', 19204.2, 112.8], ['03/25/2022', 19011.72, 92.8], ['04/25/2022', 18821.1, 92.79], ['05/25/2022', 18632.0, 80.26], ['06/27/2022', 18440.45, 77.91], ['07/25/2022', 18236.28, 57.38], ['08/25/2022', 18049.6, 53.98], ['09/26/2022', 17867.94, 45.97], ['10/25/2022', 17688.43, 32.91], ['11/25/2022', 17508.01, 25.92], ['12/27/2022', 17319.26, 17.29], ['01/25/2023', 14673.69, 7.19]];
        var CPR08CDR05 = [['08/25/2011', 0.0, 252.84], ['09/26/2011', 0.0, 270.22], ['10/25/2011', 0.0, 244.89], ['11/25/2011', 0.0, 261.78], ['12/27/2011', 0.0, 270.22], ['01/25/2012', 0.0, 244.89], ['02/27/2012', 0.0, 278.67], ['03/26/2012', 0.0, 236.44], ['04/25/2012', 0.0, 253.33], ['05/25/2012', 0.0, 253.33], ['06/25/2012', 0.0, 261.78], ['07/25/2012', 0.0, 253.33], ['08/27/2012', 0.0, 278.67], ['09/25/2012', 0.0, 244.89], ['10/25/2012', 0.0, 253.33], ['11/26/2012', 0.0, 270.22], ['12/26/2012', 0.0, 253.33], ['01/25/2013', 0.0, 253.33], ['02/25/2013', 0.0, 261.78], ['03/25/2013', 0.0, 236.44], ['04/25/2013', 0.0, 261.78], ['05/28/2013', 0.0, 278.67], ['06/25/2013', 0.0, 236.44], ['07/25/2013', 0.0, 253.33], ['08/26/2013', 0.0, 270.22], ['09/25/2013', 0.0, 253.33], ['10/25/2013', 0.0, 253.33], ['11/25/2013', 0.0, 261.78], ['12/26/2013', 0.0, 261.78], ['01/27/2014', 0.0, 270.22], ['02/25/2014', 0.0, 244.89], ['03/25/2014', 0.0, 236.44], ['04/25/2014', 0.0, 261.78], ['05/27/2014', 0.0, 270.22], ['06/25/2014', 0.0, 244.89], ['07/25/2014', 0.0, 253.33], ['08/25/2014', 0.0, 261.78], ['09/25/2014', 0.0, 261.78], ['10/27/2014', 0.0, 270.22], ['11/25/2014', 0.0, 244.89], ['12/26/2014', 0.0, 261.78], ['01/26/2015', 0.0, 261.78], ['02/25/2015', 0.0, 253.33], ['03/25/2015', 0.0, 236.44], ['04/27/2015', 0.0, 278.67], ['05/26/2015', 0.0, 244.89], ['06/25/2015', 0.0, 253.33], ['07/27/2015', 0.0, 270.22], ['08/25/2015', 0.0, 244.89], ['09/25/2015', 0.0, 261.78], ['10/26/2015', 0.0, 261.78], ['11/25/2015', 0.0, 253.33], ['12/28/2015', 0.0, 278.67], ['01/25/2016', 0.0, 236.44], ['02/25/2016', 0.0, 261.78], ['03/25/2016', 0.0, 244.89], ['04/25/2016', 0.0, 261.78], ['05/25/2016', 0.0, 253.33], ['06/27/2016', 0.0, 278.67], ['07/25/2016', 0.0, 236.44], ['08/25/2016', 0.0, 261.78], ['09/26/2016', 0.0, 270.22], ['10/25/2016', 0.0, 244.89], ['11/25/2016', 0.0, 261.78], ['12/27/2016', 0.0, 270.22], ['01/25/2017', 0.0, 244.89], ['02/27/2017', 0.0, 278.67], ['03/27/2017', 0.0, 236.44], ['04/25/2017', 0.0, 244.89], ['05/25/2017', 0.0, 253.33], ['06/26/2017', 0.0, 270.22], ['07/25/2017', 0.0, 244.89], ['08/25/2017', 0.0, 261.78], ['09/25/2017', 0.0, 261.78], ['10/25/2017', 0.0, 253.33], ['11/27/2017', 0.0, 278.67], ['12/26/2017', 0.0, 244.89], ['01/25/2018', 0.0, 253.33], ['02/26/2018', 0.0, 270.22], ['03/26/2018', 0.0, 236.44], ['04/25/2018', 0.0, 253.33], ['05/25/2018', 0.0, 253.33], ['06/25/2018', 0.0, 261.78], ['07/25/2018', 0.0, 253.33], ['08/27/2018', 0.0, 278.67], ['09/25/2018', 0.0, 244.89], ['10/25/2018', 0.0, 253.33], ['11/26/2018', 0.0, 270.22], ['12/26/2018', 0.0, 253.33], ['01/25/2019', 0.0, 253.33], ['02/25/2019', 0.0, 261.78], ['03/25/2019', 0.0, 236.44], ['04/25/2019', 0.0, 261.78], ['05/28/2019', 0.0, 278.67], ['06/25/2019', 0.0, 236.44], ['07/25/2019', 0.0, 253.33], ['08/26/2019', 0.0, 270.22], ['09/25/2019', 8834.47, 253.33], ['10/25/2019', 24927.27, 248.86], ['11/25/2019', 24631.42, 244.1], ['12/26/2019', 24338.97, 231.21], ['01/27/2020', 24049.89, 225.51], ['02/25/2020', 23803.5, 192.59], ['03/25/2020', 23481.31, 180.93], ['04/27/2020', 23202.11, 192.8], ['05/26/2020', 22926.13, 158.07], ['06/25/2020', 22653.34, 151.9], ['07/27/2020', 22383.4, 149.79], ['08/25/2020', 22116.43, 124.78], ['09/25/2020', 21852.97, 121.81], ['10/26/2020', 21592.54, 110.36], ['11/25/2020', 21334.08, 95.86], ['12/28/2020', 21079.11, 93.56], ['01/25/2021', 20826.21, 69.42], ['02/25/2021', 20576.75, 65.95], ['03/25/2021', 20330.9, 49.84], ['04/26/2021', 20146.52, 45.97], ['05/25/2021', 20065.88, 31.79], ['06/25/2021', 23216.74, 23.48], ['07/26/2021', 20016.96, 11.32], ['08/25/2021', 1613.11, 0.82]];
        var CPR10CDR05 = [['08/25/2011', 0.0, 252.84], ['09/26/2011', 0.0, 270.22], ['10/25/2011', 0.0, 244.89], ['11/25/2011', 0.0, 261.78], ['12/27/2011', 0.0, 270.22], ['01/25/2012', 0.0, 244.89], ['02/27/2012', 0.0, 278.67], ['03/26/2012', 0.0, 236.44], ['04/25/2012', 0.0, 253.33], ['05/25/2012', 0.0, 253.33], ['06/25/2012', 0.0, 261.78], ['07/25/2012', 0.0, 253.33], ['08/27/2012', 0.0, 278.67], ['09/25/2012', 0.0, 244.89], ['10/25/2012', 0.0, 253.33], ['11/26/2012', 0.0, 270.22], ['12/26/2012', 0.0, 253.33], ['01/25/2013', 0.0, 253.33], ['02/25/2013', 0.0, 261.78], ['03/25/2013', 0.0, 236.44], ['04/25/2013', 0.0, 261.78], ['05/28/2013', 0.0, 278.67], ['06/25/2013', 0.0, 236.44], ['07/25/2013', 0.0, 253.33], ['08/26/2013', 0.0, 270.22], ['09/25/2013', 0.0, 253.33], ['10/25/2013', 0.0, 253.33], ['11/25/2013', 0.0, 261.78], ['12/26/2013', 0.0, 261.78], ['01/27/2014', 0.0, 270.22], ['02/25/2014', 0.0, 244.89], ['03/25/2014', 0.0, 236.44], ['04/25/2014', 0.0, 261.78], ['05/27/2014', 0.0, 270.22], ['06/25/2014', 0.0, 244.89], ['07/25/2014', 0.0, 253.33], ['08/25/2014', 0.0, 261.78], ['09/25/2014', 0.0, 261.78], ['10/27/2014', 0.0, 270.22], ['11/25/2014', 0.0, 244.89], ['12/26/2014', 0.0, 261.78], ['01/26/2015', 0.0, 261.78], ['02/25/2015', 0.0, 253.33], ['03/25/2015', 0.0, 236.44], ['04/27/2015', 0.0, 278.67], ['05/26/2015', 0.0, 244.89], ['06/25/2015', 0.0, 253.33], ['07/27/2015', 0.0, 270.22], ['08/25/2015', 0.0, 244.89], ['09/25/2015', 0.0, 261.78], ['10/26/2015', 0.0, 261.78], ['11/25/2015', 0.0, 253.33], ['12/28/2015', 0.0, 278.67], ['01/25/2016', 0.0, 236.44], ['02/25/2016', 0.0, 261.78], ['03/25/2016', 0.0, 244.89], ['04/25/2016', 0.0, 261.78], ['05/25/2016', 0.0, 253.33], ['06/27/2016', 0.0, 278.67], ['07/25/2016', 0.0, 236.44], ['08/25/2016', 0.0, 261.78], ['09/26/2016', 0.0, 270.22], ['10/25/2016', 0.0, 244.89], ['11/25/2016', 0.0, 261.78], ['12/27/2016', 0.0, 270.22], ['01/25/2017', 0.0, 244.89], ['02/27/2017', 0.0, 278.67], ['03/27/2017', 0.0, 236.44], ['04/25/2017', 0.0, 244.89], ['05/25/2017', 0.0, 253.33], ['06/26/2017', 0.0, 270.22], ['07/25/2017', 0.0, 244.89], ['08/25/2017', 0.0, 261.78], ['09/25/2017', 0.0, 261.78], ['10/25/2017', 0.0, 253.33], ['11/27/2017', 0.0, 278.67], ['12/26/2017', 0.0, 244.89], ['01/25/2018', 0.0, 253.33], ['02/26/2018', 0.0, 270.22], ['03/26/2018', 0.0, 236.44], ['04/25/2018', 0.0, 253.33], ['05/25/2018', 0.0, 253.33], ['06/25/2018', 0.0, 261.78], ['07/25/2018', 0.0, 253.33], ['08/27/2018', 0.0, 278.67], ['09/25/2018', 0.0, 244.89], ['10/25/2018', 25190.19, 253.33], ['11/26/2018', 31124.07, 256.61], ['12/26/2018', 30738.57, 224.8], ['01/25/2019', 30318.58, 209.23], ['02/25/2019', 29886.62, 200.33], ['03/25/2019', 29331.8, 166.81], ['04/25/2019', 25820.41, 169.32], ['05/28/2019', 25464.53, 165.86], ['06/25/2019', 25113.42, 128.68], ['07/25/2019', 24767.02, 125.15], ['08/26/2019', 24425.27, 120.11], ['09/25/2019', 24088.11, 100.23], ['10/25/2019', 23755.48, 88.02], ['11/25/2019', 23427.31, 78.52], ['12/26/2019', 23103.55, 66.26], ['01/27/2020', 22784.14, 55.91], ['02/25/2020', 22501.59, 39.51], ['03/25/2020', 22157.77, 28.49], ['04/27/2020', 21851.08, 20.06], ['05/26/2020', 14150.51, 6.93]];

        var data;
        data = '''+str(data)+''';

        var totint;
        var totprint;

        // calculate the total interest and principal.
        function calculateTotal() {
        totint = 0;
        totprin = 0;
        for (var i=0;i<data.length;i++) {
            totprin = totprin + data[i][1];
            totint = totint + data[i][2]; } }

        // draw table of cash flow.
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

        // draw column chart of cash flow.
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

        // draw pie chart of cash breakdown.
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

        // function for redrawing chart when switching between cdr/cpr scenarios in Merrill Lynch example.
        function reDraw() {
            calculateTotal();
            drawTable();
            drawDashboard();
            drawPieChart();
            document.getElementById("interest").checked = true;
            document.getElementById("schedprin").checked = true;
            $(document).ready(function() {
                $("#categories").buttonset();
                $("#slider-range").slider({
                    range: true,
                    min: 1,
                    max: data.length,
                    values: [1, data.length],
                    animate: "normal",
                    slide: function(event, ui) {$("#amount").val(data[(ui.values[0]-1)][0] + " - " + data[(ui.values[1]-1)][0]); sliderChange(ui.values[0], ui.values[1]);},
                    stop: function(event, ui) {$("#amount").val(data[(ui.values[0]-1)][0] + " - " + data[(ui.values[1]-1)][0]); sliderChange(ui.values[0], ui.values[1]);} }); 
		$("#amount").val(data[$("#slider-range").slider("values", 0)-1][0] + " - " + data[$("#slider-range").slider("values", 1)-1][0]); }); }

        // checks if the upload csv file option is checked.
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

            // jquery slider tied to google charts slider.
            function sliderChange(low, high) {rangeSlider.setState({'lowValue':low, 'highValue':high}); rangeSlider.draw(); }

            // function for changing view of column chart.
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

            // initialize jquery ui elements.
            $(document).ready(function() {
                $("#tabs").tabs();
                $("button").button();
                $("#categories").buttonset();
                $("#fixcpr").buttonset();
                $("#fixcdr").buttonset();
                $("#accordion1").accordion({active: false, collapsible: true});
                $("#accordion2").accordion({collapsible: true, autoHeight: false});
                $("#slider-range").slider({
                    range: true,
                    min: 1,
                    max: data.length,
                    values: [1, data.length],
                    animate: "normal",
                    slide: function(event, ui) {$("#amount").val(data[(ui.values[0]-1)][0] + " - " + data[(ui.values[1]-1)][0]); sliderChange(ui.values[0], ui.values[1]);},
                    stop: function(event, ui) {$("#amount").val(data[(ui.values[0]-1)][0] + " - " + data[(ui.values[1]-1)][0]); sliderChange(ui.values[0], ui.values[1]);} }); 
		$("#amount").val(data[$("#slider-range").slider("values", 0)-1][0] + " - " + data[$("#slider-range").slider("values", 1)-1][0]); });
        </script>
    </head>
    <body style="font-size:62.5%;">
        <button type="button" onclick="home();");">Back to Home</button>
        <button type="button" onclick="logout();");">Sign Out</button>
        <!-- option to redraw with different data -->
        <div id="accordion1">
            <h3><a href="#">Cash Flow Grapher</a></h3>
            <div>
                <form action="/grapher" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td colspan="2"><button type="submit" name="loadml" value="true">Load MLMI2007-ML1 M1</button></td></tr>
                    </table>
                </form>
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
        <!-- display results -->
        <div id="accordion2">
            <h3><a href="#">Results</a></h3>
            <div>
                <!-- scenario change options ONLY DISPLAYED IF LOADING MERRILL LYNCH DATA -->
                <div '''+loadml+'''>
                    <span id="fixcdr">
                        <input type="radio" id="radio1" name="radio" onclick="data=CPR02CDR05; reDraw();" checked="checked" /><label for="radio1">02CPR:05CDR</label>
                        <input type="radio" id="radio7" name="radio" onclick="data=CPR04CDR05; reDraw();" /><label for="radio7">04CPR:05CDR</label>
                        <input type="radio" id="radio8" name="radio" onclick="data=CPR06CDR05; reDraw();" /><label for="radio8">06CPR:05CDR</label>
                        <input type="radio" id="radio9" name="radio" onclick="data=CPR08CDR05; reDraw();" /><label for="radio9">08CPR:05CDR</label>
                        <input type="radio" id="radio10" name="radio" onclick="data=CPR10CDR05; reDraw();" /><label for="radio10">10CPR:05CDR</label>
                    </span>
                    <span id="fixcpr">
                        <input type="radio" id="radio2" name="radio" onclick="data=CPR02CDR06; reDraw();" /><label for="radio2">02CPR:06CDR</label>
                        <input type="radio" id="radio3" name="radio" onclick="data=CPR02CDR08; reDraw();" /><label for="radio3">02CPR:08CDR</label>
                        <input type="radio" id="radio4" name="radio" onclick="data=CPR02CDR10; reDraw();" /><label for="radio4">02CPR:10CDR</label>
                        <input type="radio" id="radio5" name="radio" onclick="data=CPR02CDR12; reDraw();" /><label for="radio5">02CPR:12CDR</label>
                        <input type="radio" id="radio6" name="radio" onclick="data=CPR02CDR14; reDraw();" /><label for="radio6">02CPR:14CDR</label>
                    </span>    
                    <br /><br />
                </div>
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
<!-- '''+header+''' -->
<html>
    <head>
        <title>CUSIP Price Finder</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/'''+jquerytheme+'''/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script>
            function home() {window.location="/"; }
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }

            // initialize jquery ui elements.
            $(document).ready(function() {
                $("button").button();
                $("#accordion1").accordion();
                $("#accordion2").accordion(); });
        </script>
    </head>
    <body style="font-size:62.5%;">
        <button type="button" onclick="home();");">Back to Home</button>
        <button type="button" onclick="logout();");">Sign Out</button>
        <!-- option to paste CUSIP in a list -->
        <div id="accordion1">
            <h3><a href="#">CUSIP List Price Finder</a></h3>
            <div>
                <form action="/price" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td><textarea name="cusiplst" rows="3" cols="100">233889AE4, 12667GWF6, 68389FBW3, 86358RE29, 743873AP6, 617463AA2</textarea></td></tr>
                        <tr><td><p style="font-size:10px;">Enter CUSIP values separated by commas.<br />Do not enter any line breaks.</p></td></tr>
                        <tr><td><button type="submit" name="find-1" value="Find Price">Find Price</button></td></tr>
                    </table>
                </form>
            </div>
        </div>
        <!-- option to paste CUSIP in block, read first 9 characters of each line as CUSIP, ignore rest of line -->
        <div id="accordion2">
            <h3><a href="#">CUSIP Paste Price Finder</a></h3>
            <div>
                <form action="/price" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td><textarea name="cusippaste" rows="15" cols="100">
233889AE4 these
12667GWF6 characters
68389FBW3 will
86358RE29 be
743873AP6 ignored</textarea></td></tr>
                        <tr><td><p style="font-size:10px;">The first 9 characters of each line will be interpreted as a CUSIP.</p></td></tr>
                        <tr><td><button type="submit">Find Price</button></td></tr>
                    </table>
                </form>
            </div>
        </div>
    </body>
</html>
        ''')
    def post(self):
        raw_data = []
        # if using the first option (CUSIP in a list), format input into list.
        if str(self.request.get('find-1')) == 'Find Price':
            cusip_input = self.request.get('cusiplst')
            split_input = cusip_input.split(', ')
            for cusip in split_input:
                raw_data.append(str(cusip))
        # if using second option (CUSIP pasted, ignores everything in line after CUSIP), format input into list.
        else:
            cusip_input = self.request.get('cusippaste')
            split_input = cusip_input.split('\r\n')
            for i in split_input:
                raw_data.append(str(i)[:9])
        # go to fidelity site, fetch CUSIP information, parse data.
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
        # calls getpx(cusip) on a list of cusip, returns matrix of price data.
        def pxfinder(cusiplst):
            pxmat = []
            for cusip in cusiplst:
                pxmat.append([cusip, getpx(cusip)])
            return pxmat
        # passes input data into pxfinder.
        data = pxfinder(raw_data)
        self.response.out.write('''
<!-- '''+header+''' -->
<html>
    <head>
        <title>Pricing Results</title>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/'''+jquerytheme+'''/jquery-ui.css" rel="stylesheet" type="text/css"/>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>
        <script>
            function home() {window.location="/"; }
            function logout() {location.replace("'''+users.create_logout_url("/")+'''"); }

            // initialize jquery ui elements
            $(document).ready(function() {
                $("button").button();
                $("#accordion1").accordion({active: false, collapsible: true});
                $("#accordion2").accordion({active: false, collapsible: true});
                $("#accordion3").accordion({collapsible: true, autoHeight: false}); });
        </script>
        <script type="text/javascript" src="https://www.google.com/jsapi"></script>
        <script type="text/javascript ">

        // load google charts api.
        google.load('visualization', '1', {packages:['table']});
        google.load('visualization', '1', {packages:['corechart']});
        google.setOnLoadCallback(drawTable);

        var data = '''+str(data)+''';

        // draw table of price data using price matrix.
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
        <!-- option to search again with different CUSIP -->
        <div id="accordion1">
            <h3><a href="#">CUSIP List Price Finder</a></h3>
            <div>
                <form action="/price" method="post">
                    <table style="text-align:center; font-size:12px;" align="center" cellpadding="5">
                        <tr><td><textarea name="cusiplst" rows="3" cols="100">'''+self.request.get('cusiplst')+'''</textarea></td></tr>
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
                        <tr><td><textarea name="cusippaste" rows="15" cols="100">'''+self.request.get('cusippaste')+'''</textarea></td></tr>
                        <tr><td><p style="font-size:10px;">The first 9 characters of each line will be interpreted as a CUSIP.</p></td></tr>
                        <tr><td><button type="submit">Find Price</button></td></tr>
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

class BondVisual(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
<!-- '''+header+''' -->
<html>
<head>
        <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/themes/'''+jquerytheme+'''/jquery-ui.css" rel="stylesheet" type="text/css"/>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js" type="text/javascript"></script>
<script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.15/jquery-ui.min.js"></script>

<script type="application/javascript">

// function for drawing rounded rectangles
function roundRect(ctx, x, y, width, height, radius, fill, stroke)
{
    if (typeof stroke == "undefined" ) {
        stroke = true;
    }
    if (typeof radius === "undefined") {
        radius = 5;
    }
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
    if (stroke) {
        ctx.stroke();
    }
    if (fill) {
        ctx.fill();
    }        
}

// draw the bond visualzation.
function draw() {
    // visualization based on cdr and vpr value from slider.
    var x = $("#cdr-slider-range").slider("value") + $("#vpr-slider-range").slider("value")
    
    var c = document.getElementById("myCanvas");
    c.width = c.width
    var ctx = c.getContext("2d");

    ctx.font = "bold 18px arial";
    ctx.textBaseline = "top";
    ctx.fillStyle = "black";

    // determines which bond labels are drawn. if bond is completely gone from losses, label is not drawn.
    var a = 0;
    var b = 0;
    var c = 0;
    var d;
    // the m-array keeps track of what rectangles to draw.
    var m = [0, 0, 0, 0];
    if (x < 5) {
        ctx.fillText("AAA", 10, 10);
        ctx.fillText("1M1", 10, 377);
        ctx.fillText("SUBSM2-M6", 10, 419);
        ctx.fillText("XS/OC", 10, 531);
        d = 27*x/5;
        m = [1, 1, 1, 1];}
    else if (x < 13) {
        ctx.fillText("AAA", 10, 10);
        ctx.fillText("1M1", 10, 377);
        ctx.fillText("SUBSM2-M6", 10, 419);
        c = 105*(x-5)/8;
        m = [0, 1, 1, 1];}
    else if (x < 18) {
        ctx.fillText("AAA", 10, 10);
        ctx.fillText("1M1", 10, 377);
        b = 35*(x-13)/5;
        m = [0, 0, 1, 1];}
    else if (x < 30) {
        ctx.fillText("AAA", 10, 10);
        a = 360*(x-18)/12;
        m = [0, 0, 0, 1]}
        

    // draws the rectangles representing tranches.
    if (m[3] == 1) {
    ctx.strokeStyle = "#000066";
    ctx.fillStyle = "#3364c2";
    roundRect(ctx, 150, 10, 600, 360 - a, 5, true);}

    if (m[2] == 1) {
    ctx.strokeStyle = "#330000";
    ctx.fillStyle = "#f31900";
    roundRect(ctx, 150, 377, 600, 35 - b, 5, true);}

    if (m[1] == 1) {
    ctx.strokeStyle = "#cc3300";
    ctx.fillStyle = "#f7d72b";
    roundRect(ctx, 150, 419, 600, 105 - c, 5, true);}

    if (m[0] == 1) {
    ctx.strokeStyle = "#003300";
    ctx.fillStyle = "#44df00";
    roundRect(ctx, 150, 531, 600, 27 - d, 5, true);}
}
</script>
<script>
// initializes jquery ui elements. sliders for adjusting cdr and vpr.
$(document).ready(function() {
    $("button").button();
    $("#cdr-slider-range").slider({
        range: "min",
        max: 15,
        value: 0,
        animate: "normal",
        slide: function(event, ui) {$("#cdr-amount").val(ui.value + "%"); draw();},
        stop: function(event, ui) {$("#cdr-amount").val(ui.value + "%"); draw();} }); 
    $("#cdr-amount").val($("#cdr-slider-range").slider("value") + "%");
    $("#vpr-slider-range").slider({
        range: "min",
        max: 15,
        value: 0,
        animate: "normal",
        slide: function(event, ui) {$("#vpr-amount").val(ui.value + "%"); draw();},
        stop: function(event, ui) {$("#vpr-amount").val(ui.value + "%"); draw();} }); 
    $("#vpr-amount").val($("#vpr-slider-range").slider("value") + "%");
})
</script>
</head>
<body onload="draw()">
    <!-- sliders for cdr and vpr -->
    <label for="cdr-amount" style="font-family:arial; font-size:12px;">CDR:</label>
    <input type="text" id="cdr-amount" style="border:0; color:#f6931f; font-weight:bold;" readonly="readonly" />
    <div style="font-size:62.5%; width:400px;" id="cdr-slider-range"></div><br />
    <label for="vpr-amount" style="font-family:arial; font-size:12px;">VPR:</label>
    <input type="text" id="vpr-amount" style="border:0; color:#f6931f; font-weight:bold;" readonly="readonly" />
    <div style="font-size:62.5%; width:400px;" id="vpr-slider-range"></div><br />
    <!-- canvas for drawing bond visualization -->
    <canvas id="myCanvas" width="800" height="600">
    Sorry! Your browser does not support HTML5 Canvas.
    </canvas>
</body>
</html>
''')
                

application = webapp.WSGIApplication([('/', MainPage), ('/calculator', MBSCalculator), ('/grapher', CashFlowGrapher), ('/price', PriceFinder), ('/visual', BondVisual)], debug=False)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
