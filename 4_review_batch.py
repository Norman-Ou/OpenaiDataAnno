from openai import OpenAI
import os
import glob

client = OpenAI()

batch1 = client.batches.retrieve("batch_68085879a5d481908896ac600110e400")
batch2 = client.batches.retrieve("batch_6808587ab30481909aa350b51e100173")

print(batch1.status)
print(batch2.status)

batch1_output = client.files.content(batch1.output_file_id)
batch2_output = client.files.content(batch2.output_file_id)

import pdb; pdb.set_trace()

batch1_output_text = batch1_output.text
batch2_output_text = batch2_output.text

output_dir = "output_jsonl"
os.makedirs(output_dir, exist_ok=True)

with open(f"{output_dir}/batch1_output.jsonl", "w") as f: f.write(batch1_output_text)

with open(f"{output_dir}/batch2_output.jsonl", "w") as f: f.write(batch2_output_text) 







