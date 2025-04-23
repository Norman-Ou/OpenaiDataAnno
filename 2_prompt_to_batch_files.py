import os
import json 
import base64
from tqdm import tqdm

split = "train"
prompt_dir = "input_txt/train"
image_dir = "data/crowdai/train/images"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

item = {
    "custom_id": "request-1", 
    "method": "POST", 
    "url": "/v1/chat/completions", 
    "body": {
        "model": "ft:gpt-4o-2024-08-06:personal::Abh7Ac4S",
        "messages": [{
            "role": "system", 
            "content": "You are an intelligent chatbot tasked with identifying and describing objects within an 300x300 pixel image. "
        },{
            "role": "user", 
            "content": [],
        }],
    "max_tokens": 1000}
}


count = 0
file_index = 0
current_output_jsonl = "input_jsonl/{split}/crowdai_{file_index}.jsonl"
current_output_jsonl = current_output_jsonl.format(split=split, file_index=file_index)
os.makedirs(os.path.dirname(current_output_jsonl), exist_ok=True)

prompt_files = os.listdir(prompt_dir)
prompt_files.sort()

for prompt_file in tqdm(prompt_files):
    image_path = os.path.join(image_dir, prompt_file.replace(".txt", ".jpg"))   
    image_base64 = encode_image(image_path)

    data_id = prompt_file.replace(".txt", "")
    item["custom_id"] = data_id
    item["body"]["messages"][1]["content"] = []  # 清空之前的内容

    item["body"]["messages"][1]["content"].append({
        "type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
    })
    
    with open(os.path.join(prompt_dir, prompt_file), "r") as f:
        prompt = f.read()

    item["body"]["messages"][1]["content"].append({
        "type": "text", "text": prompt
    })

    # 检查当前文件大小
    current_file_path = current_output_jsonl.format(split=split, file_index=file_index)
    if os.path.exists(current_file_path):
        file_size = os.path.getsize(current_file_path) / (1024 * 1024)  # 转换为MB
    else:
        file_size = 0
    
    # 如果当前文件大小接近500MB，创建新文件
    if file_size > 450:  # 设置一个稍小的阈值，以确保不会超过500MB
        count = 0
        file_index += 1
        current_file_path = current_output_jsonl.format(split=split, file_index=file_index)

    with open(current_file_path, "a") as f:
        f.write(json.dumps(item) + "\n")    

    # 每处理100条数据后，也创建新的jsonl文件
    count += 1
    if count >= 100:
        count = 0
        file_index += 1

    