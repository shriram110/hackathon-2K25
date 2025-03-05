import time
import json

from functools import wraps

from openai import AzureOpenAI
# from logger import logger
# from config import env_settings, constants

module_name = "openai_service"

def retry_with_backoff(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            delay = 16
            while attempt <= max_retries:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    attempt += 1
                    if attempt > max_retries:
                        raise

                    delay *= 2  # Incremental backoff
                    # Log the failure
                    time.sleep(delay)
        return wrapper

    return decorator


class OpenAIService:

    @retry_with_backoff(max_retries=3)
    def call_gpt(self, messages, is_json_response=False):
        start_time = time.time()
        try:
            if (is_json_response):
                response = self.azure_open_ai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    # max_tokens=4000,
                    # response_format={"type": "json_object"},
                    temperature=0,
                    top_p=0
                )

                content = response.choices[0].message.content.strip()
                data = json.loads(content)
            else:
                response = self.azure_open_ai_client.chat.completions.create(
                    model="gpt-4o",
                    temperature=0,
                    top_p=0,
                    messages=messages
                )
                data = response.choices[0].message.content


            return data

        except Exception as e:
            print(e)
            error_msg = f"Error while calling azure openai, reason: {e}"

        return None
