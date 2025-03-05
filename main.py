import time
from utils.openai import OpenAIService

def read_file(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
       content = file.read()
    return content
start = time.time()
prompt_text = f"""
create a proper structured question and option from the given survey draft
There will be relation across question for creating options and question
resolve the dependency and give the question and option
###survey draft
{read_file("draft.txt")}
"""

prompt =  {"role": "user", "content": prompt_text}

output = (OpenAIService()).call_gpt([prompt])
print(time.time() - start)

with open("output_pet.txt", "w", encoding="utf-8") as file:
    file.write(output)
    
mermaid_prompt_text = f"""
Your job is to create a mermaid js for the given set of survey question this is done to check the survey flow
Whenever they mention quota added it as a layer in process flow

###output format
Return only mermaid.js part no additional info/commentry should be present
DO NOT APPEND str like ```mermaid at the front and ``` at the end
DO not make **MISTAKE IN GENERATION MERMAID JS** like Parse issue due to paranthesis in label
###survey question
{output}
"""

mermaid_prompt =  {"role": "user", "content": mermaid_prompt_text}
start = time.time()

mermaid_output = (OpenAIService()).call_gpt([mermaid_prompt])
print(time.time() - start)
with open("mermaid_output.txt", "w", encoding="utf-8") as file:
    file.write(mermaid_output)