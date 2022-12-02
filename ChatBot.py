import requests 
from dotenv import load_dotenv
import os
from os.path import join, dirname

from twilio.rest import Client

load_dotenv()

TWILLIO_SECRET = os.getenv('TWILLIO_SECRET')
TWILLIO_SID = os.getenv('TWILLIO_SID')
TWILLIO_NUMBER = os.getenv('TWILLIO_NUMBER')
GPT3_TOKEN = os.getenv('GPT3_TOKEN')
client = Client(TWILLIO_SID, TWILLIO_SECRET)

def send_message(to_number, message):
  message = client.messages.create(
                                  body=message,
                                  from_=TWILLIO_NUMBER,
                                  to=to_number
                                )
  if message.status == "sent":
    return 



def ChatGPT(prompt):
  headers={
  "Content-Type": "application/json",
  "Authorization": f"Bearer {GPT3_TOKEN}"
  }

  body = {
    "model": "text-davinci-003",
    "prompt": f"casual chat:\n{prompt}",
    "max_tokens": 512,
    "temperature": 0.85,
  }
  response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=body)
  message = response.json()
  message = message['choices']
  message = message['text']
  print(f"New Prompt!\nResponse:{str(message)}")
  return str(message)  

  
from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route("/sms", methods=["POST"])
def sms_reply():
  resp = MessagingResponse()
  data = request.form
  body = data.to_dict()
  print(body["Body"])
  prompt = body["Body"]
  reply = ChatGPT(prompt)
  resp.message(reply)
  return str(resp)

@app.route('/sms/new', methods=["POST"])
def new_chat():
  phone_num = request.form.get('phone_num')
  message = request.form.get('message')
  reply = ChatGPT(message)
  send_message(phone_num, reply)
  print(phone_num)
  
  # call twilio stuff with phone num
  return f'Text sent to {phone_num}'






## twilio needs server to send webhook replys to, 
## 