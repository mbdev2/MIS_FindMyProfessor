$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number[0]);
        console.log("Received number" + msg.number[1]);
        number_string = '<h3>Naprava 1: </h3>'+'<p>' + msg.number[0].toString() + '</p>'+ '</br>' +'<h3>Naprava 2: </h3>'+ '<p>' + msg.number[1].toString() + '</p>';
        $('#log').html(number_string);
    });
});
