from flask import Flask, request, render_template, jsonify
import threading
import requests
import base64
import gc
import json
import os

HF_TOKEN = os.environ.get('HF_TOKEN')
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# HF api for image-to-text model inference
def query(image_encoded, args = {}):
    headers = {
		"Accept" : "application/json",
		"Authorization": "Bearer " + HF_TOKEN,
		"Content-Type": "application/json" 
	}
    
    response = requests.post(
		"https://ahz74gvhq3nyzwbe.us-east-1.aws.endpoints.huggingface.cloud", 
		headers=headers, 
		json={
            "inputs": image_encoded,
            "generation_args": args
        }  
	).json()
    
    try:
        return response[0]
    except:
        return response

# Wake up the image-to-text model server
def wakeup():
    try:
        _ = query("wake")
    except:
        pass
    return

# Route for the main page
@app.route('/')
def index():
    threading.Thread(target = wakeup).start()
    return render_template('index.html')

# Caption request
@app.route('/caption', methods=['POST'])
def caption():
    # Encode Image to base64
    try:
        file = request.files.get('image')
        image_encoded = base64.b64encode(file.read()).decode("utf-8")
    except Exception as e:
        app.logger.error(f'Image encoding error: {e}')
        return jsonify({'error': f'Image encoding error: {e}'}), 500
    
    # Get generation arguments
    settings = {}
    try:
        settings = json.loads(request.form.get('settings'))
    except: 
        pass
    
    # Model Inference with API
    response = query(image_encoded, settings)
    if 'error' in response:
        if '503' in response['error']:
            return jsonify({'error': "Server starting up, please wait for a moment"}), 503
        app.logger.error(f'Model error: {response["error"]}')
        return jsonify({'error': f'Model error: {response["error"]}'}), 500
    caption = response['generated_caption']
    
    del image_encoded
    gc.collect()
    app.logger.info('Successfully generated caption')    
    return jsonify({'caption': caption})

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File size exceeds backend server limits.'}), 413
 
if __name__ == '__main__':
    app.run(debug=False)