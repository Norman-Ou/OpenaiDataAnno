import os
import base64
import json
from collections import defaultdict

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

prompt = open("prompt.txt", "r").read()

item = {
    "custom_id": "request-1", 
    "method": "POST", 
    "url": "/v1/chat/completions", 
    "body": {
        # "model": "gpt-4.1-2025-04-14",
        "model": "gpt-4o-2024-08-06",
        "messages": [{
            "role": "system", 
            "content": "You are an intelligent chatbot tasked with identifying and describing objects within an 300x300 pixel image. "
        },{
            "role": "user", 
            "content": [],
        }],
    "max_tokens": 1000}
}

data_root = "data/CrowdAI"
data_split = "train" # "val"

image_dir = os.path.join(data_root, data_split, "images")

# 读取标注文件
with open(os.path.join(data_root, data_split, "annotation.json"), "r") as f:
    annotations = json.load(f)

# 按图像ID组织标注数据
image_annotations = defaultdict(list)
for ann in annotations["annotations"]:
    image_annotations[ann["image_id"]].append(ann)

import pdb; pdb.set_trace()

for image_file in os.listdir(image_dir):
    image_path = os.path.join(image_dir, image_file)
    image_base64 = encode_image(image_path)
    item["body"]["messages"][1]["content"].append({
        "type": "input_image",
        "image_url": f"data:image/jpeg;base64,{image_base64}",
    })
    





