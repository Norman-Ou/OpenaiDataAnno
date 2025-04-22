import os
import base64
import json
import numpy as np
from tqdm import tqdm
from collections import defaultdict
import matplotlib.patches as patches
from matplotlib import pyplot as plt

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def compute_polygon_centroid(polygon):
    """
    polygon: List of [x1, y1, x2, y2, ..., xn, yn]
    """
    points = np.array(polygon).reshape(-1, 2)
    x = points[:, 0]
    y = points[:, 1]

    # Shoelace formula
    a = x[:-1] * y[1:] - x[1:] * y[:-1]
    A = np.sum(a) / 2.0


    cx = np.sum((x[:-1] + x[1:]) * a) / (6.0 * A)
    cy = np.sum((y[:-1] + y[1:]) * a) / (6.0 * A)

    return cx, cy

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

data_root = "data/crowdai"
data_split = "train" # "val", "train"

image_dir = os.path.join(data_root, data_split, "images")
output_jsonl = f"input_jsonl/CrowdAI_{data_split}_batch.jsonl"
os.makedirs("input_jsonl", exist_ok=True)
os.makedirs(f"input_txt/{data_split}", exist_ok=True)

# 读取标注文件
with open(os.path.join(data_root, data_split, "annotation-small.json"), "r") as f:
    annotations = json.load(f)

# 按图像ID组织标注数据
print("loading annotations...")
image_annotations = defaultdict(dict)
for ann in tqdm(annotations["images"]):
    if os.path.exists(os.path.join(data_root, data_split, "images", ann["file_name"])):
        image_annotations[ann["id"]] = {
            "annotations": [],
            "image_path": ann["file_name"],
        }

for ann in tqdm(annotations["annotations"]):
    if ann["image_id"] in image_annotations:
        image_annotations[ann["image_id"]]["annotations"].append(ann)


# 初始化计数器和文件索引
count = 0
file_index = 0
current_output_jsonl = f"{output_jsonl.split('.')[0]}_{file_index}.jsonl"

# for anno in tqdm(image_annotations):
for anno in image_annotations:
    image_path = image_annotations[anno]["image_path"]
    image_path = os.path.join(data_root, data_split, "images", image_path)
    data_id = os.path.basename(image_path).split('.')[0]
    
    # 为了与原代码保持一致，仍然创建objs列表
    objs = []
    for ins_index, obj in enumerate(image_annotations[anno]["annotations"]):
        x, y = compute_polygon_centroid(obj["segmentation"])
        if np.isnan(x) or np.isnan(y):
            continue

        center_x = int(x)
        center_y = int(y)

        # obj_index = obj["id"]
        obj_index = ins_index
        obj_category = "building"
        # obj_category = obj["category_id"]
        objs.append(f"{obj_index} {obj_category} [{center_x},{center_y}]")

    item['custom_id'] = data_id
    
    # image_base64 = encode_image(image_path)
    # item["body"]["messages"][1]["content"].append({
    #     "type": "input_image",
    #     "image_url": f"data:image/jpeg;base64,{image_base64}",
    # })

    objs_str = "\n".join(objs)
    # print(objs_str)
    # print()

    with open(f"input_txt/{data_split}/{data_id}.txt", "w") as f:
        f.write(prompt.replace("<objects>", objs_str))

    
    item["body"]["messages"][1]["content"].append({
        "type": "text",
        "text": prompt.replace("<objects>", objs_str),
    })

    # with open(current_output_jsonl, "a") as f:
    #     f.write(json.dumps(item) + "\n")
    
    # # 每处理500条数据后，创建新的jsonl文件
    # count += 1
    # if count >= 1000:
    #     count = 0
    #     file_index += 1
    #     current_output_jsonl = f"{output_jsonl.split('.')[0]}_{file_index}.jsonl"
    #     print(f"创建新文件: {current_output_jsonl}")
    




