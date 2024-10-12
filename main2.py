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
                    "text": """
                        Extract all relevant data from the provided ID image, ensuring that each field is mapped to the keys in the specified JSON schema. Handle abbreviations and acronyms by converting them to their full forms whenever possible (e.g., "CA" to "California"). Carefully interpret alphanumeric characters that might be easily confused during extraction (e.g., the digit '1' versus the letter 'I', the letter 'O' versus the digit '0').

                        - **Accuracy**: Ensure that critical details like names, addresses, dates, and identification numbers are accurately extracted. Double-check for any misinterpretation of characters.
                        - **Consistency**: Convert all dates to a standard format (MM/DD/YYYY). For fields like "height" and "weight," follow common formatting conventions (e.g., height as feet and inches, weight in pounds).
                        - **Data Mapping**: If an extracted value is abbreviated or encoded (e.g., "BLK" for black hair), convert it to its full form or common equivalent.
                        - **Field Omission**: If any data points in the schema are not present on the ID, do not fabricate values—simply leave those fields out of the output. Only include fields with valid data.
                        
                        The output must strictly adhere to the following JSON schema. Pay particular attention to required fields (full_name, date_of_birth, id_number), and ensure that all extracted data is both accurate and precise.

                        ### JSON Schema:
                        {
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

                        - **Example Output**:
                        {
                        "full_name": "Ima Cardholder",
                        "date_of_birth": "08/31/1977",
                        "address": "2570 24TH STREET, ANYTOWN, CA 95818",
                        "id_number": "I1234568",
                        "issue_date": "08/31/2014",
                        "hair_color": "Brown",
                        "height": "5'-05\"",
                        "weight": "125 lb",
                        "id_type": "DRIVER LICENSE"
                        }
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

# Print the response
print(json.dumps(json.loads(completion.choices[0].message.content), indent=2))