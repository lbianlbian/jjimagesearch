from datetime import datetime
print("start of file", datetime.now())
from clip_cpp import Clip
print("imported clip", datetime.now())
from PIL import Image

import math
import requests
import json
import base64
from io import BytesIO

NEW_IMGS = 3  # NUMBER OF IMAGES TO DIVIDE THE ORIGINAL INTO FOR RECTANGLE CROPPING
MIN_CROP = 2  # MINIMUM TO SPLIT EACH DIMENSION BY IN SQUARE CROPPING, MUST BE 2
MAX_CROP = 3  # MAXIMUM TO SPLIT EACH DIMENSION BY IN SQUARE CROPPING
URL = "https://pure-ostrich-20361-gcp-usc1-vector.upstash.io/query"
AUTH_HEADER = {
    "Authorization": "Bearer ABsIMHB1cmUtb3N0cmljaC0yMDM2MS1nY3AtdXNjMXJlYWRvbmx5TWpWbFpqUmtORGt0T0RWa01TMDBZMlZpTFRsalptWXRORE0xTVRSbFlURTNaalE1"
}
DEFAULT = ["LJ-6187-YQN", "FD-9853-UTP", "BX-8172-MKE"]  # return this if nothing else works\

print("starting clip load", datetime.now())
model = Clip(
    model_path_or_repo_id="clip-vit-base-patch32_ggml-model-f16.gguf",
    model_file="clip-vit-base-patch32_ggml-model-f16.gguf",
    verbosity=2
)
print("clip is loaded:", datetime.now())

def lambda_handler(event, context):
    '''
    image file will be base64 encoded in post body  with key image
    '''
    # get image
    request_payload = json.loads(event['body'])
    b64_img = request_payload["image"]
    img_b64dec = base64.b64decode(b64_img)
    img_byteIO = BytesIO(img_b64dec)
    # Read into PIL Image
    image = Image.open(img_byteIO)
    images = [image]
    # crop based on dimensions
    width, height = image.size
    if width / 2 >= height:
        # crop by 3rds along width dimension
        for i in range(NEW_IMGS):
            left, right = width // NEW_IMGS * i, width // NEW_IMGS * (i + 1)
            crop = image.crop((left, 0, right, height))  # crop goes (left, upper, right, lower)
            images.append(crop)

    elif height / 2 >= width:
        # crop by 3rds along height dimension
        for i in range(NEW_IMGS):
            upper, lower = height // NEW_IMGS * i, height // NEW_IMGS * (i + 1)
            crop = image.crop((0, upper, width, lower))  # crop goes (left, upper, right, lower)
            images.append(crop)
    else:
        # crop into 4ths and then 9ths
        for split in range(MIN_CROP, MAX_CROP + 1):
            for i in range(split):
                for j in range(split):
                    left, right = width // split * i, width // split * (i + 1)
                    upper, lower = height // split * i, height // split * (i + 1)
                    crop = image.crop((left, upper, right, lower))
                    images.append(crop)
    
    inputs = processor(images=images, return_tensors="pt")
    vectors = model.get_image_features(**inputs).tolist()
    best_score = -1 * math.inf
    best_matches = DEFAULT
    for vector in vectors:
        curr_payload = {
            "vector": vector,
            "includeMetadata": True,
            "topK": 3
        }
        resp = requests.post(URL, json=curr_payload, headers=AUTH_HEADER)
        '''
        {
            "result": [
                {
                    "id": "id-0",
                    "score": 1.0,
                    "metadata": {
                        "link": "upstash.com"
                    }
                },
                {
                    "id": "id-1",
                    "score": 0.99996454,
                    "metadata": {
                        "link": "docs.upstash.com"
                    }
                }
            ]
        }

        '''
        results = resp.json()["result"]
        if results[0]["score"] > best_score:
            best_score = results[0]["score"]
            best_matches = [match["id"] for match in results]
            
    return json.dumps(best_matches)
