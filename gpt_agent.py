from openai import OpenAI
import json
import os
from dotenv import load_dotenv



load_dotenv()
chat_api_key = os.getenv("gpt_api_key")


def prompt_from_chatgpt(user_input):
    api_key = chat_api_key
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
    print(response_dict)

    if 'choices' in response_dict and response_dict['choices']:

        response = response_dict['choices'][0]['message']['content']
    # Use json.loads() to safely parse the JSON string in the response
        try:
            event_list = json.loads(response)
            return event_list
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return None
    else:
        return None



def get_list_from_gpt(list_type: str, number_of_items: int, gender_of_gifts: str, price_range: str):
    prompt = f"Please create in a json form a list for a {list_type} with {number_of_items} item(s). {gender_of_gifts}. The range of prices for each gift should be {price_range}. The list should have gifts in different prices; some of them should be cheap and some should be expensive. Please create such a list and also mention the range of the price for each gift.Please don't add comments before or after the list provide only the JSON form of the list."
    event_list = prompt_from_chatgpt(prompt)
    return event_list
