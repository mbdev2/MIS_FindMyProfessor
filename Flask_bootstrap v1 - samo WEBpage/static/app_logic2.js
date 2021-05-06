
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    console.log(socket);
    //receive details from server
    socket.on('newnumber', function(msg) {
      console.log(msg);
        console.log("Received number" + msg.number[0]);
        console.log("Received number" + msg.number[1]);
        if (msg.number[0] > 60 || msg.number[1] > 60) {
          if (msg.number[0] > msg.number[1]){
            number_string =
            '<div class="row justify-content-center">'+
            '<div class="col-lg-6 col-md-6 col-sm-12" style="padding-top: 40px; padding-right: 50px; padding-left: 50px">'+
            '<img src="static/tabla-popisana.jpg" alt="Tabla" style="border:5px solid white" class="img-fluid">' +
            '</div>'+
            '<div class="col-lg-6 col-md-6 col-sm-12" style="padding-top: 40px; padding-right: 50px; padding-left: 50px">'+
            //'<h3>Naprava 1: </h3>'+'<p>' + msg.number[0].toString() + '</p>'+ '</br>' +
            '<img src="static/tabla2.jpg" alt="Tabla" class="img-fluid" style="opacity: 0.7">' +
            //'<h3>Naprava 2: </h3>'+ '<p>' + msg.number[1].toString() + '</p>';
            '</div>'+
            '</div>'
          }
          else if (msg.number[0] < msg.number[1]){
            number_string =
            '<div class="row justify-content-center">'+
            ' <div class="col-lg-6 col-md-6 col-sm-12"  style="padding-top: 40px; padding-right: 50px; padding-left: 50px">'+
            '<img src="static/tabla.jpg" alt="Tabla" class="img-fluid" style="opacity: 0.7">' +
            '</div>'+
            '<div class="col-lg-6 col-md-6 col-sm-12"  style="padding-top: 40px; padding-right: 50px; padding-left: 50px">'+
            //'<h3>Naprava 1: </h3>'+'<p>' + msg.number[0].toString() + '</p>'+ '</br>' +
            '<img src="static/tabla2-popisana.jpg" alt="Tabla" style="border:5px solid white" class="img-fluid">' +
            //'<h3>Naprava 2: </h3>'+ '<p>' + msg.number[1].toString() + '</p>';
            '</div>'+
            '</div>'
          }
        }
        else{
          number_string =
          '<div class="row justify-content-center">'+
          ' <div class="col-lg-6 col-md-6 col-sm-12"  style="padding-top: 40px; padding-right: 50px; padding-left: 50px">'+
          '<img src="static/tabla.jpg" alt="Tabla" style="opacity: 0.7" class="img-fluid">' +
          '</div>'+
          '<div class="col-lg-6 col-md-6 col-sm-12"  style="padding-top: 40px; padding-right: 50px; padding-left: 50px">'+
          //'<h3>Naprava 1: </h3>'+'<p>' + msg.number[0].toString() + '</p>'+ '</br>' +
          '<img src="static/tabla2.jpg" alt="Tabla" style="opacity: 0.7" class="img-fluid">' +
          //'<h3>Naprava 2: </h3>'+ '<p>' + msg.number[1].toString() + '</p>';
          '</div>'+
          '</div>'
        }
        $('#log').html(number_string);

        char_string =
        '<div class="col justify-content-center">'+
        '<br><h2>Statistika uporabe:</h2><br>'+
        '<h4>Leva Tabla: ' + msg.number[2].toString() + '% </h4>'+
        '<h4>Desna Tabla: ' + msg.number[3].toString() + '% </h4>'+
        '<h4>Ni pisanja: ' + msg.number[4].toString() + '% </h4>'+
        '</div>'

        $('#char').html(char_string);

        google.charts.load('current', {'packages':['corechart']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {

          var data = google.visualization.arrayToDataTable([
            ['Task', 'Hours per Day'],
            ['Tabla 1',     msg.number[2]],
            ['Tabla 2',      msg.number[3]],
            ['Brez',  msg.number[4]],
          ]);

          var options = {
            title: 'Statistika Uporabe',
            backgroundColor: { fill:'transparent' },
            titleTextStyle: { color: 'white'},
            legend: {textStyle: {color: 'white'}, alignment: 'center'}
          };

          var chart = new google.visualization.PieChart(document.getElementById('piechart'));

          chart.draw(data, options);
        }

    });


});
