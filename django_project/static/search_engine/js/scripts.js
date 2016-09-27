// JavaScript Document

//ready
var socket = null;
var isopen = false;
var my_address = null;

$(document).ready(function(){

    socket = new WebSocket("ws://127.0.0.1:9000");
    socket.binaryType = "arraybuffer";

    socket.onopen = function(){
        console.log('Connected!');
        isopen = true;
    }

    socket.onmessage = function(e){
        console.log('message');
        if (typeof e.data == "string") {
            if (e.data.indexOf('tcp')+1){
                console.log("Text message received: " + e.data);
                my_address = e.data;
            } else {
                console.log("Text message received: " + e.data);
                $.ajax({
                    url: "/"+e.data+"/",
                    type: "GET",
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain){
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    },
                    data: ({}),
                    dataType: "html",
                    success: function(data){
                        $('div.result-images').html(data);
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

    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $('form.search-image button').bind('click', function(e){
        e.preventDefault();
        var keyword = $('#id_keyword').val();
//        console.log(keyword)
        if(isopen){
            socket.send(my_address);
            console.log("Text message send.");
        } else {
            console.log("Connection not opened.")
        }
        if (keyword != ''){
            $.ajax({
                url: "/",
                type: "POST",
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain){
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                data: ({keyword: keyword}),
                dataType: "html",
                success: function(data){
                    $('div.result-images').html(data);
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
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain){
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            data: ({}),
            dataType: "html",
            success: function(data){
                $('div.result-images').html(data);
            }
        });
    });

});