import json
import requests
import time

api_key = "7ca0994a-3927-46c8-ab54-9e86595c7958"
authorization = "Bearer %s" % api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}

# Get a presigned URL for uploading an image
url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

payload = {"extension": "jpg"}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)

# Upload image via presigned URL
fields = json.loads(response.json()['uploadInitImage']['fields'])

url = response.json()['uploadInitImage']['url']

image_id = response.json()['uploadInitImage']['id']  # For getting the image later

image_file_path = "output.jpg"
files = {'file': open(image_file_path, 'rb')}

response = requests.post(url, data=fields, files=files) # Header is not needed

print(response.status_code)

# Generate with an image prompt
url = "https://cloud.leonardo.ai/api/rest/v1/generations"

payload = {
    "height": 512,
    "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3", # Setting model ID to Leonardo Creative
    "prompt": "A photo of a young adult",
    "width": 512,
    "imagePrompts": [image_id] # Accepts an array of image IDs
}

response = requests.post(url, json=payload, headers=headers)

print(response.status_code)

# Get the generation of images
generation_id = response.json()['sdGenerationJob']['generationId']

url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id

time.sleep(20)

response = requests.get(url, headers=headers)

print(response.text)