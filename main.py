from fastapi import FastAPI, HTTPException
from models import GiftList, SerpApiItem, FinalGiftItem 
import crud, agents
from gpt_agent import get_list_from_chat_gpt
from typing import List

app = FastAPI()

@app.post("/gift-lists/", response_model=int)
def create_gift_list(gift_list: GiftList):
    list_id = crud.create_gift_list(gift_list)
    return list_id

@app.get("/gift-lists/{list_id}")
def read_gift_list(list_id: int):
    items = crud.get_gift_list(list_id)
    if not items:
        raise HTTPException(status_code=404, detail="Gift list not found")
    return items

def select_best_option(search_results: List[SerpApiItem]) -> SerpApiItem:
    # Sort items by rating (descending), then by price (ascending)
    sorted_items = sorted(search_results, key=lambda x: (-x.rating if x.rating is not None else 0, float(x.price.strip('$'))))
    return sorted_items[0]

@app.post("/generate-gift-list/")
def generate_gift_list():
    gift_list = get_list_from_chat_gpt()  # Get the list from ChatGPT based on user input
    final_results = []

    with crud.get_db_connection() as conn:
        for item in gift_list:  # Assuming gift_list is a list of dictionaries with 'description' and 'price_range'
            if not crud.check_item_in_database(item['description'], conn):
                # If the item is not in the database, search for it and store the results
                price_segments = item['price_range'].split("-")  # Splitting the provided price range into segments
                search_results = agents.execute_parallel_searches(item['description'], price_segments)
                for result in search_results:
                    crud.store_search_result(result, conn)
            
            # Retrieve all options for the current item from the database
            all_options = crud.get_all_agent_options(item['description'], conn)

            # Select the best option based on rating and price
            best_option = select_best_option(all_options)
            
            # Append the best option to final_results
            final_results.append(FinalGiftItem(description=item['description'], best_option=best_option))

    return final_results