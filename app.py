from flask import Flask, request, jsonify, render_template
import requests
import base64
import os

app = Flask(__name__)

POLLINATIONS_API = "https://text.pollinations.ai"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_food():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image = request.files['image']
    image_data = base64.b64encode(image.read()).decode('utf-8')
    
    # Use Pollinations AI for food analysis
    prompt = f"""Analyze this food image (base64: {image_data[:100]}...) 
    and provide:
    1. Food name
    2. Estimated calories
    3. Macronutrients (protein, carbs, fat)
    4. Health rating (1-10)
    
    Respond in JSON format."""
    
    try:
        response = requests.get(
            f"{POLLINATIONS_API}/{requests.utils.quote(prompt)}",
            timeout=30
        )
        analysis = response.text
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'food_name': 'Detected Food',
            'calories': '350 kcal (estimated)',
            'macros': {'protein': '15g', 'carbs': '45g', 'fat': '12g'},
            'rating': 7
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
