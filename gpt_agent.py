from openai import OpenAI
import json
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()
chat_api_key = os.getenv("gpt_api_key")


def prompt_from_chatgpt(user_input):
    api_key = chat_api_key
    if not api_key:
        print("GPT API key not found. Please check your environment variables.")
        return None
    
    try:
        client = OpenAI(api_key=api_key)
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": user_input,
                }
            ])

        response_dict = json.loads(chat_completion.model_dump_json())
        print(f"Received response from GPT: {response_dict}")

        if 'choices' in response_dict and response_dict['choices']:

            response = response_dict['choices'][0]['message']['content']
        # Use json.loads() to safely parse the JSON string in the response
            # Remove Markdown code block syntax if present
            cleaned_response = response.replace('```json', '').replace('```', '').strip()
            logging.info(f"Cleaned GPT response content: {cleaned_response}")

            try:
                event_list = json.loads(cleaned_response)
                print(f"GPT response parsed successfully: {event_list}")
                # Ensure the output is always a dictionary, even if GPT returns a list
                if isinstance(event_list, list):
                    return {'gifts': event_list}
                else:
                    return event_list
                
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}\nResponse content: {response}")
                return None
        else:
            logging.error("GPT did not return any items.")
            return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while processing GPT response: {e}")
        return None


def get_list_from_gpt(list_type: str, number_of_items: int, gender_of_gifts: str, price_range: str):
    prompt = f"Please create in a json form a list for a {list_type} with exactly {number_of_items} item(s). For {gender_of_gifts}. The range of prices for each gift should be {price_range}. The list should have gifts in different prices; some of them should be cheap and some should be expensive. Please create such a list and also mention the range of the price for each gift. Please don't add comments before or after the list provide only the JSON form of the list. Please the first key of your JSON should be 'gifts'."
    event_list = prompt_from_chatgpt(prompt)
    return event_list
