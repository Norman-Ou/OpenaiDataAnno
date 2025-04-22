from openai import OpenAI
import os
import base64

client = OpenAI()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

image_path = "/home/Norman-Ou/OpenaiDataAnno/data/crowdai/val/images/000000000011.jpg"
image_base64 = encode_image(image_path)
prompt_path = os.path.join("input_txt/val", os.path.basename(image_path).replace(".jpg", ".txt"))

with open(prompt_path, "r") as f:
    prompt = f.read()


completion = client.chat.completions.create(
    model="ft:gpt-4o-2024-08-06:personal::Abh7Ac4S",
    messages=[
        {"role": "developer", "content": "You are an intelligent chatbot tasked with identifying and describing objects within an 300x300 pixel image."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]
        }
    ]
)

print(completion.choices[0].message)