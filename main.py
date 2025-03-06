import time
from utils.openai import OpenAIService

def read_file(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
       content = file.read()
    return content

def write_file(file_name, content):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)

start = time.time()
prompt_text = f"""
###objective
create a proper structured question and option from the given survey draft
There will be relation across question for creating options and question
resolve the dependency and give the question and option

###instruction
DO NOT GIVE ANY COMMENTS OR ADDITIONAL INFOS like prefix text like this is the survey draft or anything like that

###survey draft
{read_file("draft.txt")}
"""

prompt =  {"role": "user", "content": prompt_text}

output = (OpenAIService()).call_gpt([prompt])
print(time.time() - start)

with open("output_pet.txt", "w", encoding="utf-8") as file:
    file.write(output)

# output = file.read("output_pet.txt")

sample_output = read_file("mermaid_output_sample.txt")
base_prompt = read_file("mermaid_base_prompt.txt")
mermaid_prompt_text = f"""
{base_prompt}

###survey question
{output}
"""
print(mermaid_prompt_text)
mermaid_prompt =  {"role": "user", "content": mermaid_prompt_text}
start = time.time()
write_file("pet_prompt_mermaid.txt", mermaid_prompt_text)
mermaid_output = (OpenAIService()).call_gpt([mermaid_prompt])


print(time.time() - start)

mermaid_html = read_file("flowchart_template.html")

write_file("mermaid_output_pet.txt",mermaid_output)
mermaid_output_html = mermaid_html.replace("{mermaid_input}",mermaid_output)
write_file("mermaid_output_pet.html",mermaid_output_html)






