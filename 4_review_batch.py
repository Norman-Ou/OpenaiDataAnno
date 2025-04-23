from openai import OpenAI
import os
import glob

client = OpenAI()

batch1 = client.batches.retrieve("batch_68085879a5d481908896ac600110e400")
batch2 = client.batches.retrieve("batch_6808587ab30481909aa350b51e100173")

print(batch1.status)
print(batch2.status)



