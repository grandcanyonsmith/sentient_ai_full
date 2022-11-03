import requests
import os
import sys





# define the function

def send_email(recipient,text_response):
    json = {"recipient": recipient, "subject": "test", "body": text_response}
    send = requests.post('https://hooks.zapier.com/hooks/catch/12053983/b0qmqye/', json=json)
    # r = requests.post('https://hooks.zapier.com/hooks/catch/12053983/b0z2nmo/', json={"text": predicted_text})
    # print(r.status_code)
    # print(r.text)
    # write the code to send the email
    

# write a function that queries emails.txt and returns a list of dictionaries. Each dictionary should have the following keys: name, email
def get_emails():
    # get the emails from path /Users/canyonsmith/Documents/GitHub/whispering/emails.txt
    email_path = "/Users/canyonsmith/Desktop/sentient_ai/assistent_ai_code/whispering/emails.txt"
    with open(email_path, 'r') as f:
        lines = f.readlines()
        emails = []
        for line in lines:
            line = line.strip()
            line = line.split(",")
            name = line[0]
            email = line[1]
            emails.append({"name": name, "email": email})
        return [email for email in emails if email["name"] != "name"]
    
        

# define the main function
def main(sender, recipient, subject, body):
    # call the function
    send_email(sender, recipient, subject, body)


# parameters
# sender = 'canyonfsmith@gmail.com'
# recipient = 
# subject =
# body =





        