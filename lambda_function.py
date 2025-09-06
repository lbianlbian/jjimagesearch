from clip_cpp import Clip
import requests
import json
import base64
import os

URL = "https://pure-ostrich-20361-gcp-usc1-vector.upstash.io/query"
AUTH_HEADER = {
    "Authorization": "Bearer ABsIMHB1cmUtb3N0cmljaC0yMDM2MS1nY3AtdXNjMXJlYWRvbmx5TWpWbFpqUmtORGt0T0RWa01TMDBZMlZpTFRsalptWXRORE0xTVRSbFlURTNaalE1"
}
DEFAULT = ["LJ-6187-YQN", "FD-9853-UTP", "BX-8172-MKE"]  # return this if nothing else works\
PIC_DOWNLOAD_PATH = "/tmp/image.jpg"

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
    with open(PIC_DOWNLOAD_PATH, "wb") as image_file:
        image_file.write(base64.b64decode(b64_str))
    
    print(os.path.getsize(PIC_DOWNLOAD_PATH))

    vector = model.load_preprocess_encode_image(PIC_DOWNLOAD_PATH)
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
    
    return json.dumps([match["id"] for match in results])
