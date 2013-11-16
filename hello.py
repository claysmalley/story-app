import os
from flask import Flask, Response, request, render_template_string, render_template
from twilio.rest import TwilioRestClient
from run_game import RunGame
from story_game import Story
import database_access
import os
#from flask_bootstrap import Bootstrap

account_sid = "AC20abc57414d1cc3b1b6cf8c63fe93e4b"
auth_token  = "830591f9c55c50af9c52c936ee507ede"
client = TwilioRestClient(account_sid, auth_token)
our_number = "+12402153687"
completed_stores = []

conn = database_access.DatabaseConnection()

start_gaming = RunGame(conn)

app = Flask(__name__)

@app.route('/responses', methods = ['GET', 'POST'])
def hello():
    m = request.values
    from_number = m['From'] 
    message = m['Body']

    output = start_gaming.receive_all_messages(from_number, message)
    if len(output) == 4:
        send_text(output[0], output[2])
        send_text(output[1], output[3])
    elif len(output) == 3:
        send_text(output[0], output[2])
        send_text(output[1], output[2])
    else:
        send_text(output[0], output[1])
    return

@app.route('/story/<int:story_id>', methods = ['GET'])
def view_story(story_id):
    story = conn.get_story(story_id)
    return story

@app.route('/')
def home():
    template = render_template( "index.html", m=conn.get_stories(20))
    return template

def send_text( number, message):
    """
    Returns the xml string in the correct Twillio Response
    format for rendering. 
    """
    send = client.messages.create(body=message, to=number, from_=our_number)
    return

if __name__ == '__main__':
    main()

def main():
    app.run(debug = True)
