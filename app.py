from flask import Flask, request, render_template, jsonify
from model_loader import ImageCaptionModel
from PIL import Image
import gc
import json
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

model = ImageCaptionModel()

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Caption api
@app.route('/caption', methods=['POST'])
def caption_api():
    # Check file existence
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No file uploaded.'}), 400

    # Validate image type
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        return jsonify({'error': 'Only .jpg, .jpeg, or .png files are allowed.'}), 400
    
    # Load image with PIL and resize
    try:
        image = Image.open(file.stream).convert('RGB')
        image.thumbnail([768,768], Image.LANCZOS)
    except Exception as e:
        app.logger.error(f'Image loading error: {e}')
        return jsonify({'error': f'Image loading error: {e}'}), 500
    
    # Get generation arguments
    args = {}
    try:
        settings = json.loads(request.form.get('settings'))
        args['temperature'] = float(settings.get('temperature'))
        args['top_k'] = int(settings.get('top_k'))
        args['top_p'] = float(settings.get('top_p'))
    except: 
        pass
    
    # Model Inference
    try:
        caption = model.get_caption(image, args)
    except Exception as e:
        app.logger.error(f'Model error: {e}')
        return jsonify({'error': f'Model error: {e}'}), 500
    
    del image, args
    gc.collect()
    app.logger.info('Successfully generated caption')    
    return jsonify({'caption': caption})

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'error': 'File too large. Please keep the file size under 5MB'}), 413
    
if __name__ == '__main__':
    app.run(debug=False)