var express = require("express");
var myParser = require("body-parser");
var request = require("request");
var app = express();

var port = 8080;
var Token = 'YOUR_BOT_TOKEN';
var room_id = 'ROOM_ID';

app.use(myParser.json());
app.post("/", function(request, response) {
    var body =  request.body;
    
    if("id" in body) {
        var results = "Ticket "+ "**#"+body.id+"**"+" has gone stale" +"\n\n"+body.title+"\n\n" + body.ticket_url+"<br><br>";
        to_Spark(results);
        response.end('Ok');
        
    }
    else if("customer_name" in body){
    
        var results = "**High Priority Customer: **"+ "***"+body.customer_name+"***"+"** opened a new ticket:**"+"\n\n"+body.ticket_url+"<br><br>";
        to_Spark(results);
        response.end('Ok');
        
    }
    else {
    
        response.end('Expecting something else');
        
    }
});

//Function that connects to Spark and sends ticket detail in markdown format to a Spark room  
function to_Spark(results){
    request({
        headers: {'content-type' : 'application/json', 'Content-Type':'application/json','Authorization': 'Bearer '+Token },
        url: 'https://api.ciscospark.com/v1/messages',
        method: "POST",
        body: JSON.stringify({ "roomId":room_id, "markdown": results})
        
    }, function(error, response, body){
    console.log(body);
        
    });

}

app.listen(port);
console.log("App running on: " + port);