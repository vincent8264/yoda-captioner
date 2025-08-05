import requests
import os
HF_TOKEN = os.environ.get('HF_TOKEN')

def query(image_encoded, args):
    payload = {
        "inputs": image_encoded,
        "generation_args": args
    }  
    
    headers = {
		"Accept" : "application/json",
		"Authorization": "Bearer " + HF_TOKEN,
		"Content-Type": "application/json" 
	}
    
    response = requests.post(
		"https://ahz74gvhq3nyzwbe.us-east-1.aws.endpoints.huggingface.cloud", 
		headers=headers, 
		json=payload
	)

    return response.json()[0]