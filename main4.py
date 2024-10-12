import os
import base64
import json
from flask import Flask, request, render_template_string, jsonify
from fireworks.client import Fireworks
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

def initialize_client():
    return Fireworks(api_key="YOUR_API_KEY_HERE")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def create_completion(client, encoded_image):
    return client.chat.completions.create(
        model="accounts/fireworks/models/llama-v3p2-11b-vision-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": """
                            Extract all relevant data from the provided ID image, ensuring that each field is mapped to the keys in the specified JSON schema. Handle abbreviations and acronyms by converting them to their full forms whenever possible (e.g., "CA" to "California"). Carefully interpret alphanumeric characters that might be easily confused during extraction (e.g., the digit '1' versus the letter 'I', the letter 'O' versus the digit '0').

                            - **Accuracy**: Ensure that critical details like names, addresses, dates, and identification numbers are accurately extracted. Double-check for any misinterpretation of characters.
                            - **Consistency**: Convert all dates to a standard format (MM/DD/YYYY). For fields like "height" and "weight," follow common formatting conventions (e.g., height as feet and inches, weight in pounds).
                            - **Data Mapping**: If an extracted value is abbreviated or encoded (e.g., "BLK" for black hair), convert it to its full form or common equivalent.
                            - **Field Omission**: If any data points in the schema are not present on the ID, do not fabricate values—simply leave those fields out of the output. Only include fields with valid data.
                            
                            The output must strictly adhere to the following JSON schema. Pay particular attention to required fields (full_name, date_of_birth, id_number), and ensure that all extracted data is both accurate and precise.
                            """
                    }
                ]
            }
        ],
        max_tokens=1000
    )

def process_image(client, image_path):
    encoded_image = encode_image(image_path)
    completion = create_completion(client, encoded_image)
    try:
        return json.loads(completion.choices[0].message.content)
    except json.JSONDecodeError:
        print("Raw API response:", completion.choices[0].message.content)
        return {"error": "Failed to parse API response", "raw_response": completion.choices[0].message.content}

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            client = initialize_client()
            result = process_image(client, filepath)
            
            with open(filepath, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            if "error" in result:
                return render_template_string('''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>ID Information Extractor - Error</title>
                        <style>
                            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                            img { max-width: 100%; height: auto; }
                            pre { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }
                        </style>
                    </head>
                    <body>
                        <h1>ID Information Extractor - Error</h1>
                        <h2>Uploaded Image:</h2>
                        <img src="data:image/png;base64,{{ image }}" alt="Uploaded ID">
                        <h2>Error:</h2>
                        <p>{{ result.error }}</p>
                        <h3>Raw API Response:</h3>
                        <pre>{{ result.raw_response }}</pre>
                        <a href="/">Upload another image</a>
                    </body>
                    </html>
                ''', image=encoded_image, result=result)
            
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>ID Information Extractor</title>
                    <style>
                        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                        img { max-width: 100%; height: auto; }
                        pre { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }
                    </style>
                </head>
                <body>
                    <h1>ID Information Extractor</h1>
                    <h2>Uploaded Image:</h2>
                    <img src="data:image/png;base64,{{ image }}" alt="Uploaded ID">
                    <h2>Extracted Information:</h2>
                    <pre>{{ result }}</pre>
                    <a href="/">Upload another image</a>
                </body>
                </html>
            ''', image=encoded_image, result=json.dumps(result, indent=2))
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ID Information Extractor</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        </style>
    </head>
    <body>
        <h1>ID Information Extractor</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".png,.jpg,.jpeg">
            <input type="submit" value="Upload and Process">
        </form>
    </body>
    </html>
    '''

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
