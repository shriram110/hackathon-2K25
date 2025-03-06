import time
from utils.openai import OpenAIService

def read_file(file_name):
    """Reads the content of a file."""
    with open(file_name, "r", encoding="utf-8") as file:
        return file.read()

def write_file(file_name, content):
    """Writes content to a file."""
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)



def process_survey_draft(input_file, output_file):
    """Processes the survey draft and generates structured questions and options."""
    survey_draft = read_file(input_file)
    survey_draft_prompt = read_file("survey_draft_prompt.txt")
    survey_draft_prompt = survey_draft_prompt.replace("{survey_draft_input}", survey_draft)
    start_time = time.time()
    output = OpenAIService().call_gpt([{"role": "user", "content": survey_draft_prompt}])
    print(f"Processing time: {time.time() - start_time} seconds")
    write_file(output_file, output)
    return output

def generate_mermaid_output(survey_output, base_prompt_file, template_file, output_text_file, output_html_file):
    """Generates Mermaid.js visualization output."""
    base_prompt = read_file(base_prompt_file)
    mermaid_prompt_text = f"""
    {base_prompt}
    
    ###survey question
    {survey_output}
    """
    write_file(output_text_file, mermaid_prompt_text)
    
    mermaid_prompt = {"role": "user", "content": mermaid_prompt_text}
    start_time = time.time()
    mermaid_output = OpenAIService().call_gpt([mermaid_prompt])
    write_file("mermaid_output_file.txt", mermaid_output)
    print(f"Mermaid processing time: {time.time() - start_time} seconds")
    
    mermaid_html_template = read_file(template_file)
    mermaid_output_html = mermaid_html_template.replace("{mermaid_input}", mermaid_output)
    write_file(output_html_file, mermaid_output_html)

def main():
    """Main execution function."""
    survey_output = process_survey_draft("draft.txt", "output_pet.txt")
    # generate_mermaid_output(
    #     survey_output,
    #     "mermaid_base_prompt.txt",
    #     "flowchart_template.html",
    #     "pet_prompt_mermaid.txt",
    #     "mermaid_output_pet.html"
    # )

if __name__ == "__main__":
    main()
