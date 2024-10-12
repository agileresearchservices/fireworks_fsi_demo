from fireworks.client import Fireworks
import base64
import json

# Initialize the Fireworks client
client = Fireworks(api_key="YOUR_API_KEY_HERE")

# Read the image file and encode it in base64
with open("Identity Documents/License 1.png", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

# Define the JSON schema for the output
json_schema = {
    "type": "object",
    "properties": {
        "full_name": {"type": "string"},
        "date_of_birth": {"type": "string"},
        "address": {"type": "string"},
        "nationality": {"type": "string"},
        "birth_place": {"type": "string"},
        "id_number": {"type": "string"},
        "expiration_date": {"type": "string"},
        "issue_date": {"type": "string"},
        "class": {"type": "string"},
        "restrictions": {"type": "string"},
        "endorsements": {"type": "string"},
        "eye_color": {"type": "string"},
        "hair_color": {"type": "string"},
        "sex": {"type": "string"},
        "height": {"type": "string"},
        "weight": {"type": "string"},
        "id_type": {"type": "string"}
    },
    "required": ["full_name", "date_of_birth", "id_number"]
}

# Create the completion request
completion = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p2-11b-vision-instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Extract all relevant data from the provided ID image, ensuring that keys and values follow the specified JSON schema. Be mindful of abbreviations and acronyms, and attempt to match them to their full forms where possible. Pay special attention to potential misinterpretations of alphanumeric characters (e.g., capital 'I' mistaken for the digit '1'). For values that appear as abbreviations or encoded terms, convert them to common names or values. Ensure that names, addresses, dates, and identification numbers are accurately extracted. If any data points in the schema are missing from the image, do not fabricate values—simply omit those fields. The output should follow this schema exactly. Ensure accuracy and precision in the extracted data, especially for alphanumeric codes and dates. "
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encoded_image}"
                    }
                }
            ]
        }
    ],
    response_format={"type": "json_object", "schema": json_schema},
    max_tokens=256,
    temperature=0.4
)

# Print the response
print(json.dumps(json.loads(completion.choices[0].message.content), indent=2))