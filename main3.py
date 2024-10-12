import os
import base64
import json
from fireworks.client import Fireworks

def initialize_client():
    return Fireworks(api_key="YOUR_API_KEY_HERE")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def create_completion(client, encoded_image):
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

    return client.chat.completions.create(
        model="accounts/fireworks/models/llama-v3p2-11b-vision-instruct",
        messages=[
            {
                "role": "user",
                "content": [
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

def process_image(client, image_path):
    encoded_image = encode_image(image_path)
    completion = create_completion(client, encoded_image)
    return json.loads(completion.choices[0].message.content)

def main():
    client = initialize_client()
    folder_path = "Identity Documents"
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            print(f"Processing {filename}:")
            result = process_image(client, image_path)
            print(json.dumps(result, indent=2))
            print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()