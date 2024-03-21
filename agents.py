from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging


load_dotenv()
serp_api_key = os.getenv("SERP_API_KEY")

def calculate_price_range(price_point: int) -> str:
    """
    Calculate a price range that is ±10% of the given price point.

    :param price_point: The central price point.
    :return: A string formatted as "low-high" representing the price range.
    """
    low_price = int(price_point * 0.9)
    high_price = int(price_point * 1.1)
    return f"{low_price}-{high_price}"

def search_with_serpapi(description: str, price_range_low: int, price_range_high: int) -> dict:
    logging.info(f"Starting SerpAPI search for '{description}' with price range {price_range_low}-{price_range_high}")
    search_result = {'description': description, 'price': None, 'link': None, 'rating': None}  # Default result
    """
    Perform a search using SerpAPI based on the given description and price range.

    :param description: The description of the gift item to search for.
    :param price_range_low: The lower bound of the price range for the search query.
    :param price_range_high: The upper bound of the price range for the search query.
    :return: A dictionary with the description, found price, and link, or an empty dict if no results.
    """
    params = {
    "engine": "google_shopping",
    "q": description,
    "tbs": f"mr:1,avg_rating:400,price:1,ppr_min:{price_range_low},ppr_max:{price_range_high},sales:1",
    "api_key": serp_api_key,
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        logging.info(f"Received SerpAPI results for '{description}': {results}")
        filters = results.get("filters", {})
        shopping_results = results.get("shopping_results", [])
        
        if shopping_results:
            best_match = next((item for item in shopping_results if item.get("position") == 1), None)
            if best_match:
                # Update search_result with the best match's details
                search_result.update({
                    "price": best_match.get("price"),
                    "link": best_match.get("link"),
                    "rating": float(best_match.get("rating", 0))
                })
            else:
                logging.warning(f"No best match found for '{description}' within the specified price range.")
        else:
            logging.warning(f"No shopping results found for '{description}'.")

    except KeyError as e:
        logging.error(f"KeyError accessing result data for '{description}': {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during SerpAPI search for '{description}': {e}")

    return search_result

def execute_parallel_searches(description: str, base_price_range: str) -> list:
    """
    Execute searches in parallel for the given description at three price points: low, mid, and high within ±10% range.

    :param description: The description of the gift item to search for.
    :param base_price_range: The base price range from GPT, formatted as "low-high".
    :return: A list of dictionaries, each containing the results of a search.
    """
    cleaned_price_range = base_price_range.replace('$', '').replace(' ', '')
     # Split the price range and ensure there are two parts
    parts = cleaned_price_range.split('-')
    if len(parts) != 2:
        raise ValueError(f"Invalid price_range format: {base_price_range}. Expected format: 'low-high'.")

     # Unpack the low and high values and convert them to integers
    low, high = map(int, parts)
    mid = (low + high) // 2  # Calculate the middle price point

    # Define price segments for the three agents with ±10% range
    price_segments = [
        (int(low * 0.9), int(low * 1.1)),
        (int(mid * 0.9), int(mid * 1.1)),
        (int(high * 0.9), int(high * 1.1))
    ]

    search_results = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        # Create a future for each price point search
        future_to_segment = {executor.submit(search_with_serpapi, description, segment[0], segment[1]): segment for segment in price_segments}

        # As each future completes, collect the results
        for future in as_completed(future_to_segment):
            search_results.append(future.result())

    return search_results


