#!/usr/bin/env python

import time
import boto.sqs
import json
from twilio.rest import TwilioRestClient

import creds

ACCOUNT_SID = creds.ACCOUNT_SID
AUTH_TOKEN = creds.AUTH_TOKEN

def main():
  conn = boto.sqs.connect_to_region("ap-southeast-1")
  billing_queue = conn.get_queue('billing-queue')

  while True:
    print "Long polling billing queue ...", billing_queue._arn()

    sqs_message_list = billing_queue.get_messages(num_messages=1, wait_time_seconds=20)
    if sqs_message_list:
      sqs_message = sqs_message_list[0]
      json_message = json.loads(sqs_message.get_body())

      text_message = "//".join([json_message.get('TopicArn'), json_message.get('Subject'), json_message.get('Message')])

      print "Sending message ...", text_message
      client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
      twilio_message = client.messages.create(to="+971528703911", from_="+14805265812", body=text_message,)
    
      billing_queue.delete_message(sqs_message)
    else:
      print "No message found on the billing queue ..."
      
    print "Sleeping for 10 seconds .."
    time.sleep(10)

if __name__=='__main__':
  try:
    main()
  except Exception as e:
    print "Error: ", e.message

