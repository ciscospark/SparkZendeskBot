from flask import Flask , request
import json 
import urllib , urllib2

app = Flask(__name__)

@app.route('/', methods =['POST'])


def zendesk_payload():
    
    json_file = request.json
    
    if 'id' in json_file:
        ticket_id = json_file['id']
        ticket_url = json_file['ticket_url']
        ticket_title = json_file['title']
        events = """Ticket **#%s** has gone stale\n\n%s\n\n%s<br><br>""" % (ticket_id,ticket_url,ticket_title)
        toSpark(events)
        
    elif 'customer_name' in json_file:
        customer_name = json_file['customer_name']
        ticket_url = json_file['ticket_url']
        events = """**High Priority Customer: %s opened a new ticket**\n\n%s<br><br>""" % (customer_name,ticket_url)
        toSpark(events)
        
    return 'Ok'
    
    

# Function that connects to Spark and sends ticket details in markdown format to a Spark room    
def toSpark(alerts):
    url = 'https://api.ciscospark.com/v1/messages'
    headers = {'accept':'application/json','Content-Type':'application/json','Authorization': 'Bearer BOT_TOKEN'}
    values =   {'roomId':'ROOM_ID', 'markdown': alerts }
    data = json.dumps(values)
    req = urllib2.Request(url = url , data = data , headers = headers)
    response = urllib2.urlopen(req)
    the_page = response.read()
    print the_page


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8080, debug= True)
