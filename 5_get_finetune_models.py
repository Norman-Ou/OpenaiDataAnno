from openai import OpenAI
client = OpenAI()

jobs = client.fine_tuning.jobs.list()

for job in jobs:
    print()
    print(job.id)
    print(job.status)
    print(job.created_at)
    print(job.model) # ftjob-QLUj5F9YcsePw3JuWbhMaUYu
    print(job.fine_tuned_model)
    import pdb; pdb.set_trace()

