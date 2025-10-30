# preso da
# https://docs.leonardo.ai/docs/generate-images-using-image-to-image-guidance

import json
import requests
import time
from semaphores import wait_semaphore, set_semaphore, clear_semaphores
import sys


if len(sys.argv) < 3:
    print("Uso: python script.py nome_file_output.txt")
    sys.exit(1)

print(sys.argv)

OUTPUT_FOLDER= sys.argv[1]
santino_fname = OUTPUT_FOLDER + "/" + "numsantino" + ".txt"

with open(santino_fname, 'r') as file:
    NUMSANTINO = file.read().strip()
print(NUMSANTINO)

with open('modelli/id%s.txt'%NUMSANTINO, 'r') as file:
    idsantino = file.read().strip()

with open('modelli/prompt%s.txt'%NUMSANTINO, 'r') as file:
    promptsantino = file.read().strip()
    print(promptsantino)

print("#%s#"%idsantino)

api_key = "7ca0994a-3927-46c8-ab54-9e86595c7958"
authorization = "Bearer %s" % api_key

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}

# STEPS TO UPLOADING IMAGE - Get a presigned URL for uploading an image
url = "https://cloud.leonardo.ai/api/rest/v1/init-image"

payload = {"extension": "jpg"}

response = requests.post(url, json=payload, headers=headers)

print("Get a presigned URL for uploading an image: %s" % response.status_code)

# Upload image via presigned URL
fields = json.loads(response.json()['uploadInitImage']['fields'])

url = response.json()['uploadInitImage']['url']

# For getting the image later
uploaded_image_id = response.json()['uploadInitImage']['id']

image_file_path = OUTPUT_FOLDER+"/utente.jpg"

files = {'file': open(image_file_path, 'rb')}

response = requests.post(url, data=fields, files=files)  # Header is not needed

print("Upload image via presigned URL: %s" % response.status_code)

url = "https://cloud.leonardo.ai/api/rest/v1/generations"

payload = {
    # TODO parametri
    # Parametri per la generazione. cft qui:
    # https://docs.leonardo.ai/docs/commonly-used-api-values

  "num_images": 1,
  "height": 1536, #2212
  "width": 1024, #1470
  "modelId": "b24e16ff-06e3-43eb-8d33-4416c2d75876",# Leonardo Lightning XL
  "prompt": promptsantino,
  "presetStyle":"CINEMATIC",

  #"photoReal": True,
  #"photoRealVersion":"v2",

# vale la pena ?

  #"alchemy":True,
  "alchemy":False,

  # a me da risltati scadenti
  #"contrast":4,

  #"styleUUID": "8e2bc543-6ee2-45f9-bcd9-594b6ce84dcd", # portrait
  "styleUUID": "645e4195-f63d-4715-a3f2-3fb1e6eb8c70",# Illustration
  "controlnets": [
        {
            "initImageId": uploaded_image_id,
            "initImageType": "UPLOADED",
            "preprocessorId": 133, # Character Reference Id
            "strengthType": "High",
        },
        {
            "initImageId": idsantino, # santino1
            "initImageType": "UPLOADED",
            "preprocessorId": 67, # Style Reference Id
            "strengthType": "Mid",
        },
        {
            "initImageId": idsantino, # santino1
            "initImageType": "UPLOADED",
            "preprocessorId": 100, #Content Reference Id
            "strengthType": "Mid",
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)

print("Generation of Images using Multiple ControlNets %s" % response.status_code)
risposta=response.json()
print(risposta)
if "error" in risposta:
    print(risposta["error"])
else:
    id=risposta['sdGenerationJob']['generationId']
    print("id "+id)
    # Get the generation of images
    final_generation_id = response.json()['sdGenerationJob']['generationId']

    url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % final_generation_id

    Finito = False
    Attesa=0
    print("Aspetto generazione..")

    while not Finito:
        time.sleep(1)
        r = requests.get(url, headers=headers)
        response = r.json()
        if not response["generations_by_pk"]["generated_images"]:
            print(Attesa)
            Attesa = Attesa+ 1
        else:
            imgurl=response["generations_by_pk"]["generated_images"][0]["url"]
            imgid=response["generations_by_pk"]["generated_images"][0]["id"]
            print("Fatto:\n"+imgid+ "\n"+imgurl)
            Finito = True

    immagine = requests.get(imgurl)

    fname= OUTPUT_FOLDER+"/generata.jpg"
    if immagine.status_code == 200:
        with open(fname, "wb") as f:
            f.write(immagine.content)
        print("Salvata come "+fname)
    else:
        print(f"Errore scaricando: {immagine.status_code}")


set_semaphore("leogenera")