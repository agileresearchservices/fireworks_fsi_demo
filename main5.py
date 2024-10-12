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
                        "text": '''Extract the following KYC (Know Your Customer) fields from the provided ID image. Only include fields that are clearly visible and do not infer or fabricate any information. Your response MUST start with a valid JSON object using the exact structure and field names provided below:
                        {
                            "full_name": "",
                            "date_of_birth": "",
                            "id_number": "",
                            "issue_date": "",
                            "expiration_date": "",
                            "nationality": "",
                            "sex": "",
                            "id_type": "",
                            "address": "",
                            "kyc_status": "complete" or "incomplete",
                            "flags": []
                        }

                        Guidelines:
                        1. Use MM/DD/YYYY format for all dates.
                        2. Use "M" for male and "F" for female in the "sex" field.
                        3. Convert state abbreviations to full names (e.g., "CA" to "California").
                        4. Set "kyc_status" to "incomplete" if any of the first 7 fields (full_name through id_type) are missing.
                        5. Add relevant flags to the "flags" array for any issues or uncertainties.
                        6. For "id_type", use "Passport", "Driver's License", "State ID", or other appropriate types.
                        7. Include "address" only if it's present on the ID.
                        8. Do not add any fields that are not in the provided structure.
                        9. Driver's license and state ID numbers should be considered the id_number. DLN is a driver's license number.

                        After the JSON object, you may provide a brief commentary on any notable aspects of the extraction process or potential issues.
                        '''
                    }
                ]
            }
        ],
        max_tokens=1000
    )

def process_image(client, image_path):
    encoded_image = encode_image(image_path)
    completion = create_completion(client, encoded_image)
    response_content = completion.choices[0].message.content
    try:
        # Try to find JSON object in the response
        json_start = response_content.find('{')
        json_end = response_content.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            json_str = response_content[json_start:json_end]
            result = json.loads(json_str)
            return result
        else:
            raise ValueError("No JSON object found in the response")
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing API response: {str(e)}")
        print("Raw API response:", response_content)
        return {"error": "Failed to parse API response", "raw_response": response_content}

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
