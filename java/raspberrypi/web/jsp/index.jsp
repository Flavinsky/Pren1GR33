<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" import="java.io.*, java.lang.String, java.util.List" errorPage="/scripts/tools/err_page.jsp"%>
<html>
    <head>
            <link href='<%=request.getContextPath() %>/css/jquery-ui-1.10.3.custom.css' rel='stylesheet'>
            <link href='<%=request.getContextPath() %>/css/main.css' rel='stylesheet'>
            <script type='text/javascript' src='<%=request.getContextPath() %>/js/jquery-1.9.1.js'></script>
            <script type='text/javascript' src='<%=request.getContextPath() %>/js/jquery-ui-1.10.3.custom.js'></script>
            <script type='text/javascript' src='<%=request.getContextPath() %>/js/jquery-migrate-1.2.1.js'></script>
            <script type='text/javascript' src='<%=request.getContextPath() %>/js/jquery.timer.js'></script>
            <script type='text/javascript' src='<%=request.getContextPath() %>/js/responsivevoice.js'></script>
            <script type='text/javascript' src='<%=request.getContextPath() %>/js/imgpreview.full.jquery.js'></script>
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
                $("#systemstatus").css("color","black");
                $("#systemstatus").css("font-size","16px");
                $("#systemstatus").html("SYSTEM READY");
                var voice = responsiveVoice;
                voice.setDefaultVoice('UK English Male');
                voice.speak('SYSTEM READY');
                //var audioElement = document.createElement('audio');
                //audioElement.setAttribute('src', '<%=request.getContextPath() %>/mp3/Power Up SYSTEM Ready.mp3');
                //audioElement.setAttribute('autoplay', 'autoplay');
                //$.get();
                //audioElement.addEventListener("load", function() {
                //audioElement.play();
                //}, true);
                //audioElement.play();
                $('#pythonfilelist').empty();
                jqXHR = $.ajax(
                {
                        type: "GET",
                        contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                        dataType: "text",
                        url: "<%=request.getContextPath() %>/Manager?action=pythonfilelist"
                        //beforeSend: function() { $('.ajax').show(); }
                }).done(function(msg) 
                {
                    var files = msg.split('\n');
                    files = files[0].split(',');
                    for(var i = 0; i < files.length; i++)
                    {
                        $('#pythonfilelist').append($('<option>', {
                            value: files[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ',''),
                            text: files[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ','')
                        }));
                    }
                });
                $('#configfilelist').empty();
                jqXHR = $.ajax(
                {
                        type: "GET",
                        contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                        dataType: "text",
                        url: "<%=request.getContextPath() %>/Manager?action=configfilelist"
                        //beforeSend: function() { $('.ajax').show(); }
                }).done(function(msg) 
                {
                    var files = msg.split('\n');
                    files = files[0].split(',');
                    for(var i = 0; i < files.length; i++)
                    {
                        $('#configfilelist').append($('<option>', {
                            value: files[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ',''),
                            text: files[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ','')
                        }));
                    }
                    $('#configsectionlist').empty();
                    jqXHR = $.ajax(
                    {
                            type: "POST",
                            contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                            dataType: "text",
                            data: { configfile: $("#configfilelist option:selected").text() },
                            url: "<%=request.getContextPath() %>/Manager?action=configsectionlist"
                            //beforeSend: function() { $('.ajax').show(); }
                    }).done(function(msg) 
                    {
                        var sections = msg.split(',');
                        for(var i = 0; i < sections.length; i++)
                        {
                            $('#configsectionlist').append($('<option>', {
                                value: sections[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ',''),
                                text: sections[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ','')
                            }));
                        }
                        $('#configlist').empty();
                        jqXHR = $.ajax(
                        {
                                type: "POST",
                                contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                                dataType: "text",
                                data: { configfile: $("#configfilelist option:selected").text(), configsection: $("#configsectionlist option:selected").text() },
                                url: "<%=request.getContextPath() %>/Manager?action=configlist"
                                //beforeSend: function() { $('.ajax').show(); }
                        }).done(function(msg) 
                        {
                            var configs = msg.split(',');
                            for(var i = 0; i < configs.length; i++)
                            {
                                $('#configlist').append($('<option>', {
                                    value: configs[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ',''),
                                    text: configs[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ','')
                                }));
                            }
                            jqXHR = $.ajax(
                            {
                                    type: "POST",
                                    contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                                    dataType: "text",
                                    data: { configfile: $("#configfilelist option:selected").text(), configsection: $("#configsectionlist option:selected").text(), configkey: $("#configlist option:selected").text() },
                                    url: "<%=request.getContextPath() %>/Manager?action=configvalue"
                                    //beforeSend: function() { $('.ajax').show(); }
                            }).done(function(msg) 
                            {
                                $("#keyvalue").val(msg);
                            });
                        });
                    });
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
                               value: sections[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ',''),
                               text: sections[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ','')
                           }));
                       }
                        jqXHR = $.ajax(
                        {
                                type: "POST",
                                contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                                dataType: "text",
                                data: { configfile: $("#configfilelist option:selected").text(), configsection: $("#configsectionlist option:selected").text(), configkey: $("#configlist option:selected").text() },
                                url: "<%=request.getContextPath() %>/Manager?action=configvalue"
                                //beforeSend: function() { $('.ajax').show(); }
                        }).done(function(msg) 
                        {
                            $("#keyvalue").val(msg);
                        });
                   });
                });
                $('#configsectionlist').change(function() {
                   $('#configlist').empty();
                   jqXHR = $.ajax(
                   {
                           type: "POST",
                           contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                           dataType: "text",
                           data: { configfile: $("#configfilelist option:selected").text(), configsection: $(this).val() },
                           url: "<%=request.getContextPath() %>/Manager?action=configlist"
                           //beforeSend: function() { $('.ajax').show(); }
                   }).done(function(msg) 
                   {
                       var configs = msg.split(',');
                       for(var i = 0; i < configs.length; i++)
                       {
                           $('#configlist').append($('<option>', {
                               value: configs[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ',''),
                               text: configs[i].replaceAll(']','').replaceAll('[','').replaceAll('\r','').replaceAll('\n','').replaceAll(' ','')
                           }));
                       }
                        jqXHR = $.ajax(
                        {
                                type: "POST",
                                contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                                dataType: "text",
                                data: { configfile: $("#configfilelist option:selected").text(), configsection: $("#configsectionlist option:selected").text(), configkey: $("#configlist option:selected").text() },
                                url: "<%=request.getContextPath() %>/Manager?action=configvalue"
                                //beforeSend: function() { $('.ajax').show(); }
                        }).done(function(msg) 
                        {
                            $("#keyvalue").val(msg);
                        });
                   });
                });
                $('#configlist').change(function() {
                   jqXHR = $.ajax(
                   {
                           type: "POST",
                           contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                           dataType: "text",
                           data: { configfile: $("#configfilelist option:selected").text(), configsection: $("#configsectionlist option:selected").text(), configkey: $(this).val() },
                           url: "<%=request.getContextPath() %>/Manager?action=configvalue"
                           //beforeSend: function() { $('.ajax').show(); }
                   }).done(function(msg) 
                   {
                       $("#keyvalue").val(msg);
                   });
                });
                
                $( "#setvalue" ).click(function() 
                {
                   jqXHR = $.ajax(
                   {
                           type: "POST",
                           contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                           dataType: "text",
                           data: { configfile: $("#configfilelist option:selected").text(), configsection: $("#configsectionlist option:selected").text(), configkey: $("#configlist option:selected").text(), newconfigvalue: $("#keyvalue").val() },
                           url: "<%=request.getContextPath() %>/Manager?action=setconfigvalue"
                           //beforeSend: function() { $('.ajax').show(); }
                   }).done(function(msg) 
                   {
                       $("#keyvalue").val(msg);
                   });
                });
                
                $("input[type=submit], a, button")
                    .button()
                    .click(function( event ) {
                      event.preventDefault();
                });
                
                $("#run").click(function() 
                {
                    voice.cancel();
                    //audioElement.pause();
                    jqXHR = $.ajax(
                    {
                            type: "POST",
                            contentType: "application/x-www-form-urlencoded; charset=ISO-8859-1",
                            dataType: "text",
                            data: { pythonfile: $("#pythonfilelist option:selected").text() },
                            url: "<%=request.getContextPath() %>/Manager?action=run"
                            //beforeSend: function() { $('.ajax').show(); }
                    }).done(function(msg) 
                    {
                        var objToday = new Date(),
                                        weekday = new Array('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
                                        dayOfWeek = weekday[objToday.getDay()],
                                        domEnder = new Array( 'th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th' ),
                                        dayOfMonth = today + (objToday.getDate() < 10) ? '0' + objToday.getDate() + domEnder[objToday.getDate()] : objToday.getDate() + domEnder[parseFloat(("" + objToday.getDate()).substr(("" + objToday.getDate()).length - 1))],
                                        months = new Array('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'),
                                        curMonth = months[objToday.getMonth()],
                                        curYear = objToday.getFullYear(),
                                        curHour = objToday.getHours() > 12 ? objToday.getHours() - 12 : (objToday.getHours() < 10 ? "0" + objToday.getHours() : objToday.getHours()),
                                        curMinute = objToday.getMinutes() < 10 ? "0" + objToday.getMinutes() : objToday.getMinutes(),
                                        curSeconds = objToday.getSeconds() < 10 ? "0" + objToday.getSeconds() : objToday.getSeconds(),
                                        curMeridiem = objToday.getHours() > 12 ? "PM" : "AM";
                        var today = curHour + ":" + curMinute + "." + curSeconds + curMeridiem + " " + dayOfWeek + " " + dayOfMonth + " of " + curMonth + ", " + curYear;
                        if($("#output").val()=="")
                        {
                            $("#output").val("---------------------------------------------------------------------"+"\n"+today+"\n"+"---------------------------------------------------------------------"+"\n"+msg);
                        }
                        else
                        {
                            $("#output").val($("#output").val()+"---------------------------------------------------------------------"+"\n"+today+"\n"+"---------------------------------------------------------------------"+"\n"+msg);
                        }
                        $('#output').scrollTop($('#output')[0].scrollHeight);
                        voice.speak(msg);
                        /*if(msg==1337)
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
                        }*/
                    });
                });
                $("#clear").click(function() 
                {
                    $('#output').val("");
                });
                $("#getimg").click(function() 
                {
                       var host = location.protocol + '//' + location.hostname + ':' + location.port;
                       $("#outputimgbinary").attr('href', host+"/raspberrypi/python/binary.jpg");
                       $("#outputimgbinary").css('display', 'block');
                       $("#outputimgcontours").attr('href', host+"/raspberrypi/python/contours.jpg");
                       $("#outputimgcontours").css('display', 'block');
                        $('#outputimgbinary, #outputimgcontours').imgPreview({
                            containerID: 'imgPreviewWithStyles',
                            imgCSS: {
                                // Limit preview size:
                                //height: 150,
                                width: 1200
                            },
                            // When container is shown:
                            onShow: function(link){
                                $('<span>' + $(link).text() + '</span>').appendTo(this);
                            },
                            // When container hides: 
                            onHide: function(link){
                                $('span', this).remove();
                            }
                        });
                });
                /*$("#stop").click(function() {
                    if(jqXHR){
                        jqXHR.abort();
                    }
                    audioElement.setAttribute('src', '');
                    //audioElement.currentTime = 0;
                    audioElement.pause();
                });*/
            });
        </script>
        <div id="accordion">
            <h3>Python-Konfigurationswerte setzen</h3>
            <div>
                <table>
                    <tr>
                        <td>
                          <select id="configfilelist"></select>
                        </td>
                        <td>
                          <select id="configsectionlist"></select>
                        </td>
                        <td>
                          <select id="configlist"></select>
                        </td>
                    </tr>
                    <tr>
                        <td><input type="text" id="keyvalue" value=""></td>
                        <td><button id="setvalue">Wert setzen</button></td>
                    </tr>
                </table>
            </div>
            <h3>Pythonscripts ausführen</h3>
            <div>
                <table>
                    <tr>
                        <td>
                            <select id="pythonfilelist"></select>
                        </td>
                        <td><button id="run">Ausführen</button></td>
                        <td><button id="clear">Leeren</button></td>
                        <td><button id="getimg">Neue Bilder laden</button></td>
                    </tr>
                    <tr>
                        <td colspan="2"><textarea id="output" style="width: 300px; height: 150px; resize: none; color: black;" disabled></textarea></td>
                        <td><a id="outputimgbinary" style="display:none;">Binary Image</a></td>
                        <td><a id="outputimgcontours" style="display:none;">Contours Image</a></td>
                    </tr>
                </table>
            </div>
          </div>
        <br/>
        <div>
            <div id="systemstatus"></div>
        </div>
    </body>
</html>