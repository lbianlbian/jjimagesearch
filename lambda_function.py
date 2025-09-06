from clip_cpp import Clip
from PIL import Image
import math
import requests
import json
import base64
from io import BytesIO
import os

NEW_IMGS = 3  # NUMBER OF IMAGES TO DIVIDE THE ORIGINAL INTO FOR RECTANGLE CROPPING
MIN_CROP = 2  # MINIMUM TO SPLIT EACH DIMENSION BY IN SQUARE CROPPING, MUST BE 2
MAX_CROP = 3  # MAXIMUM TO SPLIT EACH DIMENSION BY IN SQUARE CROPPING
URL = "https://pure-ostrich-20361-gcp-usc1-vector.upstash.io/query"
AUTH_HEADER = {
    "Authorization": "Bearer ABsIMHB1cmUtb3N0cmljaC0yMDM2MS1nY3AtdXNjMXJlYWRvbmx5TWpWbFpqUmtORGt0T0RWa01TMDBZMlZpTFRsalptWXRORE0xTVRSbFlURTNaalE1"
}
DEFAULT = ["LJ-6187-YQN", "FD-9853-UTP", "BX-8172-MKE"]  # return this if nothing else works\

model = Clip(
    model_path_or_repo_id="CLIP-ViT-B-32-laion2B-s34B-b79K_ggml-text-model-q4_0.gguf",
    verbosity=2
)

def lambda_handler(event, context):
    '''
    image file will be base64 encoded in post body  with key image
    images will be stored in tmp dir as tmp/image{0 through IDK}.jpg with 0 being the original noncropped image
    '''
    # get image
    request_payload = json.loads(event['body'])
    b64_str = request_payload["image"]
    with open("/tmp/image0.jpg", "wb") as image_file:
        image_file.write(base64.b64decode(b64_str))
    img_b64dec = base64.b64decode(b64_str)
    img_byteIO = BytesIO(img_b64dec)
    # Read into PIL Image
    image = Image.open(img_byteIO)
    
    # crop based on dimensions
    width, height = image.size
    if width / 2 >= height:
        # crop by 3rds along width dimension
        for i in range(NEW_IMGS):
            left, right = width // NEW_IMGS * i, width // NEW_IMGS * (i + 1)
            crop = image.crop((left, 0, right, height))  # crop goes (left, upper, right, lower)
            crop.save(f"/tmp/image{i + 1}.jpg")

    elif height / 2 >= width:
        # crop by 3rds along height dimension
        for i in range(NEW_IMGS):
            upper, lower = height // NEW_IMGS * i, height // NEW_IMGS * (i + 1)
            crop = image.crop((0, upper, width, lower))  # crop goes (left, upper, right, lower)
            crop.save(f"/tmp/image{i + 1}.jpg")
    else:
        # crop into 4ths and then 9ths
        img_count = 1
        for split in range(MIN_CROP, MAX_CROP + 1):
            for i in range(split):
                for j in range(split):
                    left, right = width // split * i, width // split * (i + 1)
                    upper, lower = height // split * j, height // split * (j + 1)
                    crop = image.crop((left, upper, right, lower))
                    crop.save(f"/tmp/image{img_count}.jpg")
                    img_count += 1
    
    best_score = -1 * math.inf
    best_matches = DEFAULT
    i = 0
    while i <= (MAX_CROP + 1)**2:  # upper bound on number of images present
        curr_img_file = f"/tmp/image{i}.jpg"
        if not os.path.isfile(curr_img_file):
            break
        vector = model.load_preprocess_encode_image(curr_img_file)
        os.remove(curr_img_file)
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
        
        i += 1
    
    return json.dumps(best_matches)
