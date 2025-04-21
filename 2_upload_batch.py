from openai import OpenAI
import os
import glob

client = OpenAI()

jsonl_files = glob.glob("*.jsonl")

for jsonl_file in jsonl_files:
    batch_input_file = client.files.create(
        file=open(jsonl_file, "rb"),
        purpose="batch"
    )
    print(jsonl_file)
    print("upload file: ", batch_input_file.id)

    batch_job = client.batches.create(
        input_file_id=batch_input_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": "nightly eval job"
        }
    )
    print("create batch job: ", batch_job.id)