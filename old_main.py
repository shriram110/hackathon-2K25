import json
import time
from utils.openai import OpenAIService
import pandas as pd

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

def generate_mermaid_output(survey_output, base_prompt_file, template_file, output_text_file, output_html_file, output_txt_file):
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
    write_file(output_txt_file, mermaid_output)
    print(f"Mermaid processing time: {time.time() - start_time} seconds")
    
    mermaid_html_template = read_file(template_file)
    mermaid_output_html = mermaid_html_template.replace("{mermaid_input}", mermaid_output)
    write_file(output_html_file, mermaid_output_html)

def main():
    """Main execution function."""
    
    #structured verbose generation
    screener_output = process_survey_draft("screener_draft.txt", "screener_verbose.txt")
    screener_output = pd.DataFrame(json.loads(screener_output))
    screener_output.to_csv("screener_output.csv",index=False)
    
    #mermaid generation
    generate_mermaid_output(
        screener_output,
        "mermaid_base_prompt.txt",
        "flowchart_template.html",
        "pet_prompt_mermaid_screener.txt",
        "mermaid_output_screener.html",
        "screener_mermaid.txt"
    )

    rf_output = process_survey_draft("pet_rf_draft.txt", "rf_verbose.txt")
    rf_output = pd.DataFrame(json.loads(rf_output))
    rf_output.to_csv("rf_output.csv",index=False)
    generate_mermaid_output(
        rf_output,
        "mermaid_base_prompt.txt",
        "flowchart_template.html",
        "pet_prompt_mermaid_rf.txt",
        "mermaid_output_rf.html",
        "rf_mermaid.txt"
    )

if __name__ == "__main__":
    main()
