var server = require('http').createServer(),
    io = require('socket.io').listen(server),
    process = require('process');

//port to listen can be set through command line argument by running 'node server.js [port]' (it defaults to 7080)
var port = (process.argv.length >= 3) ? process.argv[2] : 8080;
var debug = process.argv.length >= 4 && process.argv[3] == "debug";

function log(str){
    if(debug === true){
        console.log(str);
        if (io.sockets.clients().length > 0)
        {
            io.sockets.emit("debug", {message: str});
        }
    }
};

server.listen(port);
console.log("Server listening on port " + port);

io.sockets.on('connection', function(socket) {

	log("Connection established.");

	socket.on('windSpeedUpdate', function(data) {
        if (data)
        {
            log("Wind speed spdate: " + data['value'] + " from " + data["id"]);
            //socket.emit("ack", {'original':'windSpeedUpdate'});
            socket.broadcast.emit("windSpeedUpdate", data);
        }
        else
        {
            log("No data received");
        }
    });

    socket.on('windDirectionUpdate', function(data) {
        if (data)
        {
            log("Wind direction update: " + data['value'] + " from " + data["id"]);
            //socket.emit("ack", {'original':'windDirectionUpdate'});
            socket.broadcast.emit("windDirectionUpdate", data);
        }
        else
        {
            log("No data received");
        }
    });

});
