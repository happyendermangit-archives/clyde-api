import requests,time
from flask import Flask, request
## CONFIG 
ALT_TOKEN = "" 
CLYDE_DM_CHANNEL_ID = 0  

## MUST HAVE CLYDE IN DMS 
## IF NOT THEN WONT WORK
app = Flask(__name__)

def dm(prompt):
    global ALT_TOKEN
    url = f"https://discord.com/api/v9/channels/{CLYDE_DM_CHANNEL_ID}/messages"
    headers = {
        "Authorization": ALT_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "content": prompt
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        last_ = None 
        while True: 
            channel_url = f"https://discord.com/api/v9/channels/{CLYDE_DM_CHANNEL_ID}/messages"
            params = {
                    "limit": 1,
            }
            messages_response = requests.get(channel_url, headers=headers, params=params).json()
            if messages_response[0].get('author').get('bot'):
                if messages_response[0]['content'] != last_:
                    return messages_response[0]['content']
            last_ = messages_response[0]['content']
        


@app.route('/api/v1/clyde_ai')
def main_api():
    prompt = request.args.get('prompt')
    if prompt:
        response = dm(prompt)
        if response is not None:
            return {"content":response,"code":200}
        else:
            return {"message": "Failed to retrieve message", "code": 500}
    else:
        return {"message": "Put a valid prompt", "code": 400}

app.run()
