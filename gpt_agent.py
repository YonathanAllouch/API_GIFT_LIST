from openai import OpenAI
import json
import os
from dotenv import load_dotenv



load_dotenv()
chat_api_key = os.getenv("OPENAI_API_KEY")


def get_user_input():
      list_event = []
      list_type = input("Which list would you like to make? (e.g. birthday, wedding, etc.)")
      list_event.append(list_type)
      number_of_gifts = input("How many items you would wish to have?")
      list_event.append(number_of_gifts)
      gender_of_the_gifts = input("Are the gifts are for a specific gender? Do you have more detalis about the kind of gifts you want to have in the list")
      list_event.append(gender_of_the_gifts)
      range_of_prices = input("What is the range of prices for the gifts? mention the minimal price and the maximal price.")
      list_event.append(range_of_prices)

      return list_event


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

    if 'choices' in response_dict and response_dict['choices']:

        response = response_dict['choices'][0]['message']['content']
        return response
    else:

        return None



def get_list_from_chat_gpt():
    description = get_user_input()
    prompt= f"please create in a json form a list for {description[0]} with {description[1]} items. Do not add any more information / lines beside the list {description[2]}the range of prices for each gift should be {description[3]} the list should have gifts in a diffrent prices. some of them should be cheap and some should be expensive. please create such list and also mention the range of the price for each gift "
    event_list=prompt_from_chatgpt(prompt)
    event_list = eval(event_list)
    return event_list
