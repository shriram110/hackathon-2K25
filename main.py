import json
import time
import os
from utils.openai import OpenAIService
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SurveyConfig:
    input_file: str
    output_file: str
    mermaid_base_prompt: str
    mermaid_template: str
    mermaid_prompt_output: str
    mermaid_html_output: str
    mermaid_txt_output: str
    output_dir: str

class FileHandler:
    @staticmethod
    def read_file(file_name: str) -> str:
        """Reads the content of a file."""
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def write_file(file_name: str, content: str) -> None:
        """Writes content to a file."""
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)

class SurveyProcessor:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service
        self.file_handler = FileHandler()

    def process_survey_draft(self, input_file: str, output_file: str) -> str:
        """Processes the survey draft and generates structured questions and options."""
        survey_draft = self.file_handler.read_file(input_file)
        survey_draft_prompt = self.file_handler.read_file("survey_draft_prompt.txt")
        survey_draft_prompt = survey_draft_prompt.replace("{survey_draft_input}", survey_draft)
        
        start_time = time.time()
        output = self.openai_service.call_gpt([{"role": "user", "content": survey_draft_prompt}])
        print(f"Processing time: {time.time() - start_time} seconds")
        output = output.replace("```json", "").replace("```", "")
        self.file_handler.write_file(output_file, output)
        return output

    def generate_mermaid_output(self, config: SurveyConfig) -> None:
        """Generates Mermaid.js visualization output."""
        base_prompt = self.file_handler.read_file(config.mermaid_base_prompt)
        mermaid_prompt_text = f"""
        {base_prompt}
        
        ###survey question
        {config.survey_output}
        """
        self.file_handler.write_file(config.mermaid_prompt_output, mermaid_prompt_text)
        
        mermaid_prompt = {"role": "user", "content": mermaid_prompt_text}
        start_time = time.time()
        mermaid_output = self.openai_service.call_gpt([mermaid_prompt])
        self.file_handler.write_file(config.mermaid_txt_output, mermaid_output)
        print(f"Mermaid processing time: {time.time() - start_time} seconds")
        
        mermaid_html_template = self.file_handler.read_file(config.mermaid_template)
        mermaid_output_html = mermaid_html_template.replace("{mermaid_input}", mermaid_output)
        self.file_handler.write_file(config.mermaid_html_output, mermaid_output_html)

    def process_and_save_survey(self, config: SurveyConfig) -> None:
        """Processes a survey and saves all related outputs."""
        # Process survey draft
        survey_output = self.process_survey_draft(config.input_file, config.output_file)
        
        # Convert to DataFrame and save CSV
        survey_df = pd.DataFrame(json.loads(survey_output))
        csv_output = os.path.join(config.output_dir, f"{os.path.splitext(os.path.basename(config.output_file))[0]}.csv")
        survey_df.to_csv(csv_output, index=False)
        
        # Generate Mermaid visualization
        config.survey_output = survey_output
        self.generate_mermaid_output(config)

def main():
    """Main execution function."""
    openai_service = OpenAIService()
    survey_processor = SurveyProcessor(openai_service)
    
    # Create output directory
    output_dir = "survey_outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Screener survey configuration
    screener_config = SurveyConfig(
        input_file="screener_draft.txt",
        output_file=os.path.join(output_dir, "screener_verbose.txt"),
        mermaid_base_prompt="mermaid_base_prompt.txt",
        mermaid_template="flowchart_template.html",
        mermaid_prompt_output=os.path.join(output_dir, "pet_prompt_mermaid_screener.txt"),
        mermaid_html_output=os.path.join(output_dir, "mermaid_output_screener.html"),
        mermaid_txt_output=os.path.join(output_dir, "screener_mermaid.txt"),
        output_dir=output_dir
    )
    
    # RF survey configuration
    rf_config = SurveyConfig(
        input_file="pet_rf_draft.txt",
        output_file=os.path.join(output_dir, "rf_verbose.txt"),
        mermaid_base_prompt="mermaid_base_prompt.txt",
        mermaid_template="flowchart_template.html",
        mermaid_prompt_output=os.path.join(output_dir, "pet_prompt_mermaid_rf.txt"),
        mermaid_html_output=os.path.join(output_dir, "mermaid_output_rf.html"),
        mermaid_txt_output=os.path.join(output_dir, "rf_mermaid.txt"),
        output_dir=output_dir
    )
    
    # Process both surveys
    survey_processor.process_and_save_survey(screener_config)
    survey_processor.process_and_save_survey(rf_config)

if __name__ == "__main__":
    main()
