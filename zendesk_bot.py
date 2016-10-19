from flask import Flask, request
import json 
import urllib2

app = Flask(__name__)

BOT_TOKEN = "Your Bot's token"
ROOM_ID = "Room ID"

@app.route('/', methods =['POST'])


def zendesk_payload():
    events = None
    json_file = request.json
    
    if 'id' in json_file:
        ticket_id = json_file['id']
        ticket_url = json_file['ticket_url']
        ticket_title = json_file['title']
        events = """Ticket **#{0}** has gone stale\n\n{1}\n\n{2}<br><br>""".format(ticket_id,ticket_url,ticket_title)
        
    elif 'customer_name' in json_file:
        customer_name = json_file['customer_name']
        ticket_url = json_file['ticket_url']
        events = """**High Priority Customer: {0} opened a new ticket**\n\n{1}<br><br>""".format(customer_name,ticket_url)
        
    if events != None:
        toSpark(events)
        
    return 'Ok'
    
    

# Function that connects to Spark and sends ticket details in markdown format to a Spark room    
def toSpark(alerts):
    url = 'https://api.ciscospark.com/v1/messages'
    headers = {'accept':'application/json','Content-Type':'application/json','Authorization': 'Bearer '+ BOT_TOKEN}
    values =   {'roomId': ROOM_ID, 'markdown': alerts }
    data = json.dumps(values)
    req = urllib2.Request(url = url , data = data , headers = headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8080, debug=True)
