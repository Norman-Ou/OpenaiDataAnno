from openai import OpenAI
import os
import glob

client = OpenAI()

jsonl_files = glob.glob("input_jsonl/*.jsonl")

# for jsonl_file in jsonl_files:
    # batch_input_file = client.files.create(
    #     file=open(jsonl_file, "rb"),
    #     purpose="batch"
    # )
    # print(jsonl_file)
    # print("upload file: ", batch_input_file.id) # file-SvYoKqJbFkKphSnVg8sdsp, file-T7GhGyxkuGSDqTUSLWEpr4

files_ids = ["file-SvYoKqJbFkKphSnVg8sdsp", "file-T7GhGyxkuGSDqTUSLWEpr4"]
for file_id in files_ids:
    batch_job = client.batches.create(
        input_file_id=file_id,
        endpoint="/v1/chat/completions",
        completion_window="24h",
        metadata={
            "description": "nightly eval job"
        }
    )
    print("create batch job: ", batch_job.id) # ["batch_68085879a5d481908896ac600110e400", "batch_6808587ab30481909aa350b51e100173"]