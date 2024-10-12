# Fireworks FSI Demo
Demonstrate data extraction from images such as driver's licenses and passports using Fireworks AI API.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/agileresearchservices/fireworks_fsi_demo.git
   cd fireworks_fsi_demo
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install flask fireworks-ai werkzeug
   ```

4. The API key is already set in `main5.py`. If you need to use a different key, replace it in this line:
   ```python
   return Fireworks(api_key="YOUR_API_KEY_HERE")
   ```

5. Create an `uploads` folder in the project directory:
   ```
   mkdir uploads
   ```

## Running the Application

1. Start the Flask application:
   ```
   python main5.py
   ```

2. Open a web browser and navigate to `http://127.0.0.1:5000/`

3. Upload an image of a driver's license or passport to extract the information.

## Code Evolution

This repository contains multiple versions of the main application file, showing the evolution of the code:

- `main.py`: Initial version. The most simple version of the code using `llama-v3p2-11b-vision-instruct`. The prompt is not optimized.
- `main2.py`: Second iteration. Additional prompt engineering to improve the quality of the response. Using Fireworks json mode feature to enforce the JSON output.
- `main3.py`: Third iteration. The prompt is further optimized. Code is cleaned up and organized as a standard python script.
- `main4.py`: Fourth iteration. Continuous improvement of the prompt. Converted application to a Flask web application.
- `main5.py`: Final version (current). The JSON schema is included in the prompt.

To understand the development process and see how the code has evolved, please review each `main*.py` file in order. The final product is `main5.py`, which is the most up-to-date and feature-complete version of the application.

## Features

- Image upload and processing
- Data extraction from ID documents using Fireworks AI API
- JSON response parsing and error handling
- Web interface for easy interaction
- Support for various ID types (driver's licenses, passports, state IDs)
- Prompt engineering to ensure compliance with KYC standards
- Display of processed image alongside extracted information
- Error handling with display of raw API responses when parsing fails
- Support for .png, .jpg, and .jpeg file formats

## Notes

- The application uses modules from Python's standard library (base64, json) in addition to the installed packages.
- The maximum file size for upload is set to 16MB. To adjust this, modify the `MAX_CONTENT_LENGTH` setting in `main5.py`.
- The application is set to run in debug mode. For production deployment, set `debug=False` in the `app.run()` call at the end of `main5.py`.
- Allowed file types for upload are .png, .jpg, and .jpeg. To modify this, adjust the `allowed_file()` function in `main5.py`.
- Ensure that your Fireworks AI API key has the necessary permissions to use the vision model.

## Usage

1. Start the application as described in the "Running the Application" section.

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. You will see a simple web interface with an "Upload Image" button.

4. Click on the "Upload Image" button and select an image of a driver's license, passport, or state ID that you want to extract information from.

5. After selecting the image, it will be automatically uploaded and processed.

6. The application will use the Fireworks AI API to analyze the image and extract relevant information.

7. The extracted information will be displayed alongside the uploaded image.

8. The extracted data typically includes:
   - Document type (e.g., driver's license, passport)
   - Personal information (name, date of birth, etc.)
   - Document-specific details (issue date, expiration date, etc.)

9. If there are any errors in processing or if the API cannot extract the information, an error message and the raw API response will be displayed.

10. You can upload multiple images in succession to process different documents. Click the back button in your browser to return to the upload page to upload another image.

Note: Ensure that you have a stable internet connection, as the application needs to communicate with the Fireworks AI API for image processing.

## License

`none`
