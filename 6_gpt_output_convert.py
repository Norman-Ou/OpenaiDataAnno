import json

def read_jsonl(file_path):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:  # 跳过空行
                    try:
                        json_obj = json.loads(line)
                        data.append(json_obj)
                    except json.JSONDecodeError as e:
                        print(f"解析JSON时出错: {e}, 行内容: {line}")
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
    except Exception as e:
        print(f"读取文件时出错: {e}")
    
    return data


def get_content(jsonl_data):
    """
    从jsonl数据中提取生成的content内容，以custom_id为key
    
    Args:
        jsonl_data: 读取的jsonl数据列表
        
    Returns:
        dict: 以custom_id为key，content为value的字典
    """
    contents = {}
    for item in jsonl_data:
        try:
            # 检查是否存在custom_id字段
            if 'custom_id' in item:
                custom_id = item['custom_id']
                # 检查是否存在response和body字段
                if 'response' in item and 'body' in item['response']:
                    body = item['response']['body']
                    # 检查是否存在choices字段
                    if 'choices' in body and len(body['choices']) > 0:
                        # 获取第一个choice的message内容
                        message = body['choices'][0]['message']
                        if 'content' in message:
                            contents[custom_id] = message['content']
        except Exception as e:
            print(f"提取content时出错: {e}")
    
    return contents


valid_jsonl = "output_jsonl/batch2_output.jsonl"
train_jsonl = "output_jsonl/batch1_output.jsonl"

valid_data = read_jsonl(valid_jsonl)
train_data = read_jsonl(train_jsonl)

valid_contents = get_content(valid_data)
train_contents = get_content(train_data)

with open("valid_contents.json", "w") as f:
    json.dump(valid_contents, f)

with open("train_contents.json", "w") as f:
    json.dump(train_contents, f)


