from twilio.rest import TwilioRestClient
 
# Your Account Sid and Auth Token from twilio.com/user/account
account_sid = "AC20abc57414d1cc3b1b6cf8c63fe93e4b"
auth_token  = "830591f9c55c50af9c52c936ee507ede"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.sms.messages.create(body="FUCK YES",
    to="+18328004670",    # Replace with your phone number
    from_="+12402153687") # Replace with your Twilio number
print message.sid