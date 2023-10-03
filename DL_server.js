var http = require('http');
var fs = require('fs');
var path = require('path');

http.createServer(function (request, response) {
    console.log('request starting...');

    var filePath = 'D:\OTP' + request.url.split('?')[0];

    var extname = path.extname(filePath);
    var contentType = 'text/html';
    switch (extname) {
        case '.js':
            contentType = 'text/javascript';
            break;
        case '.css':
            contentType = 'text/css';
            break;
        case '.json':
            contentType = 'application/json';
            break;
        case '.png':
            contentType = 'image/png';
            break;      
        case '.jpg':
            contentType = 'image/jpg';
            break;
        case '.wav':
            contentType = 'audio/wav';
            break;
    }

    fs.readFile(filePath, function(error, content) {
        if (error) {
			response.writeHead(404);
			response.end('Sorry, check with the site admin for error: '+error.code+' ..\n');
			response.end(); 
        }
        else {
            response.writeHead(200, { 'Content-Type': contentType, 'Content-Length': Buffer.byteLength(content) });
            response.end(content, 'utf-8');
        }
    });

}).listen(80);
console.log('Server running at localhost');