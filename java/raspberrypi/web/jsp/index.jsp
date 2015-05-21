<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" import="java.io.*, java.lang.String, java.util.List" errorPage="/scripts/tools/err_page.jsp"%>
<html>
    <head>
            <link href='<%=request.getContextPath() %>/css/jquery-ui-1.10.3.custom.css' rel='stylesheet'>
            <link href='<%=request.getContextPath() %>/css/main.css' rel='stylesheet'>
            <script type='text/javascript' src='<%=request.getContextPath() %>/js/jquery-1.9.1.js'></script>
            <script type='text/javascript' src='<%=request.getContextPath() %>/js/jquery-ui-1.10.3.custom.js'></script>
            <script type='text/javascript' src='<%=request.getContextPath() %>/js/jquery-migrate-1.2.1.js'></script>
            <script type='text/javascript' src='<%=request.getContextPath() %>/js/jquery.timer.js'></script>
            <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
            <title>Raspberry Pi Controller</title>
    </head>
    <body>
        <script type='text/javascript'>
            String.prototype.replaceAll = function(str1, str2, ignore) 
            {
                return this.replace(new RegExp(str1.replace(/([\/\,\!\\\^\$\{\}\[\]\(\)\.\*\+\?\|\<\>\-\&])/g,"\\$&"),(ignore?"gi":"g")),(typeof(str2)=="string")?str2.replace(/\$/g,"$$$$"):str2);
            } 
            $( document ).ready(function() 
            {
                var jqXHR;
                $( "#accordion" ).accordion();
                $("#output").css("color","black");
                $("#output").css("font-size","16px");
                $("#output").html("SYSTEM READY");
                var audioElement = document.createElement('audio');
                audioElement.setAttribute('src', '<%=request.getContextPath() %>/mp3/Power Up SYSTEM Ready.mp3');
                audioElement.setAttribute('autoplay', 'autoplay');
                $.get();
                audioElement.addEventListener("load", function() {
                audioElement.play();
                }, true);
                audioElement.play();
                jqXHR = $.ajax(
                {
                        type: "GET",
                        contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                        dataType: "text",
                        url: "<%=request.getContextPath() %>/Manager?action=configfilelist"
                        //beforeSend: function() { $('.ajax').show(); }
                }).done(function(msg) 
                {
                    alert("all: "+msg);
                    var files = msg.split('\n');
                    for(var i = 0; i < files.length - 1; i++)
                    {
                        alert("file: "+files[i].replaceAll(']','').replaceAll('[',''));
                        $('#configfilelist').append($('<option>', {
                            value: files[i].replaceAll(']','').replaceAll('[',''),
                            text: files[i].replaceAll(']','').replaceAll('[','')
                        }));
                    }
                });
                $('#configfilelist').change(function() {
                    $('#configsectionlist').empty();
                   jqXHR = $.ajax(
                   {
                           type: "POST",
                           contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                           dataType: "text",
                           data: { configfile: $(this).val() },
                           url: "<%=request.getContextPath() %>/Manager?action=configsectionlist"
                           //beforeSend: function() { $('.ajax').show(); }
                   }).done(function(msg) 
                   {
                       var sections = msg.split(',');
                       for(var i = 0; i < sections.length; i++)
                       {
                           $('#configsectionlist').append($('<option>', {
                               value: sections[i].replaceAll(']','').replaceAll('[',''),
                               text: sections[i].replaceAll(']','').replaceAll('[','')
                           }));
                       }
                   });
                });
                $( "input[type=submit], a, button" )
                    .button()
                    .click(function( event ) {
                      event.preventDefault();
                });
                $( "#start" ).click(function() 
                {
                    var number1 = $("#number1").attr('value');
                    var number2 = $("#number2").attr('value');
                    audioElement.pause();
                    jqXHR = $.ajax(
                    {
                            type: "POST",
                            contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                            dataType: "text",
                            data: { number1: number1, number2: number2 },
                            url: "<%=request.getContextPath() %>/Manager?action=test"
                            //beforeSend: function() { $('.ajax').show(); }
                    }).done(function(msg) 
                    {
                        if(msg==1337)
                        {
                            $("#output").css("color","green");
                            $("#output").html("SUCCESS");
                            audioElement.setAttribute('src', '<%=request.getContextPath() %>/mp3/HUMAN VOICE CROWD APPLAUD CHEER SCREAM 01.mp3');
                            audioElement.play(); 
                        }
                        else
                        {
                            $("#output").css("color","red");
                            $("#output").html("FAIL");
                            audioElement.setAttribute('src', '<%=request.getContextPath() %>/mp3/HUMAN VOICE CROWD LOUD OHH 01.mp3');
                            audioElement.play();
                        }
                    });
                });
                $( "#stop" ).click(function() {
                    if(jqXHR){
                        jqXHR.abort();
                    }
                    audioElement.setAttribute('src', '');
                    //audioElement.currentTime = 0;
                    audioElement.pause();
                });
            });
        </script>
        <div id="accordion">
            <h3>Section 1</h3>
            <div>
                <table>
                    <tr>
                        <td>Number 1: <input type="text" id="number1"></td>
                        <td>Number 2: <input type="text" id="number2"></td>
                    </tr>
                    <tr>
                        <td><button id="start">Start</button></td>
                        <td><button id="stop">Stop</button></td>
                    </tr>
                </table>
            </div>
            <h3>Section 2</h3>
            <div>
                <table>
                    <tr>
                        <td>
                          <select id="configfilelist">
                          </select>
                        </td>
                        <td>
                          <select id="configsectionlist">
                          </select>
                        </td>
                        <td>
                          <select id="configlist">
                          </select>
                        </td>
                    </tr>
                    <tr>
                        <td><button id="start2">Start</button></td>
                        <td><button id="stop2">Stop</button></td>
                    </tr>
                </table>
            </div>
            <h3>Section 3</h3>
            <div>
              <p>
              Nam enim risus, molestie et, porta ac, aliquam ac, risus. Quisque lobortis.
              Phasellus pellentesque purus in massa. Aenean in pede. Phasellus ac libero
              ac tellus pellentesque semper. Sed ac felis. Sed commodo, magna quis
              lacinia ornare, quam ante aliquam nisi, eu iaculis leo purus venenatis dui.
              </p>
              <ul>
                <li>List item one</li>
                <li>List item two</li>
                <li>List item three</li>
              </ul>
            </div>
            <h3>Section 4</h3>
            <div>
              <p>
              Cras dictum. Pellentesque habitant morbi tristique senectus et netus
              et malesuada fames ac turpis egestas. Vestibulum ante ipsum primis in
              faucibus orci luctus et ultrices posuere cubilia Curae; Aenean lacinia
              mauris vel est.
              </p>
              <p>
              Suspendisse eu nisl. Nullam ut libero. Integer dignissim consequat lectus.
              Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
              inceptos himenaeos.
              </p>
            </div>
          </div>
        <div>
            <div id="output"></div>
        </div>
    </body>
</html>