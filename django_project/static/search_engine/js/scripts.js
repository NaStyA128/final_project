// JavaScript Document

//ready
var socket = null;
var isopen = false;
var my_address = null;

$(document).ready(function(){

    $('form.search-image button').bind('click', function(e){
        e.preventDefault();

        socket = new WebSocket("ws://127.0.0.1:9000");
        socket.binaryType = "arraybuffer";

        socket.onopen = function(){
            console.log('Connected!');
            isopen = true;
        }

        socket.onmessage = function(e){
            if (typeof e.data == "string") {
                if (e.data.indexOf('tcp')+1){
                    console.log("Text message received: " + e.data);
                    my_address = e.data;
                } else {
                    console.log("Text message received: " + e.data);
                    $.ajax({
                        url: "/"+e.data+"/",
                        type: "GET",
                        data: ({}),
                        dataType: "html",
                        success: function(data){
                            $('div.result-images').html(data);
                            console.log('Close!');
                            socket.close();
                        }
                    });
                }
            }
        }

        socket.onclose = function(e){
            console.log("Connection closed.");
            socket = null;
            isopen = false;
        }

        var keyword = $('#id_keyword').val();

        if (keyword != ''){
            $.ajax({
                url: "/",
                type: "POST",
                data: $('form.search-image').serialize(),
                dataType: "html",
                success: function(data){
                    $('div.result-images').html(data);
                    console.log(keyword);
                    if(isopen){
//                    socket.
                        socket.send(JSON.stringify({'keyword': keyword}));
                        console.log("Text message send.");
                    } else {
                        console.log("Connection not opened.")
                    }
                }
            });
        }
    });

    $('.result-urls div a').bind('click', function(e){
        e.preventDefault();
        href = $(this).attr('href');
        $.ajax({
            url: href,
            type: "GET",
            data: ({}),
            dataType: "html",
            success: function(data){
                $('div.result-images').html(data);
            }
        });
    });

});