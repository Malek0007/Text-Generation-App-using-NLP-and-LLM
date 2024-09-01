from flask import Flask, request, render_template, jsonify
from text_processing import process_text, generate_text 

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-text', methods=['POST'])
def process_text_route():
    text = request.form['text']
    processed_data = process_text(text)
    return jsonify(processed_data)

@app.route('/generate-text', methods=['POST'])
def generate_text_route():
    text = request.form['text']
    generated_text = generate_text(text)
    return jsonify({"generated_text": generated_text})

if __name__ == '__main__':
    app.run(debug=True)
