$(document).ready(function () {
    var socket = io.connect("https://your_ip:5000") //modify link to "https://your_ip:port"
    
    socket.on('connect', function () {
        socket.send("User connected!");
    });
    socket.on('disconnect', function () {
        console.log("User disconnected!");
    });

    socket.on('message', function (data) {
        $('.messages').append($('<p>').text(data));
    });

    $('#send').on('click', function () {
        socket.send($('#username').val() + ': ' + $('#message').val());
        $('.message').val('');
    });
})