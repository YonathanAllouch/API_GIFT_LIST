from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed



load_dotenv()
serpapi_key = os.getenv("SERPAPI_KEY")

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
    """
    Perform a search using SerpAPI based on the given description and price range.

    :param description: The description of the gift item to search for.
    :param price_range_low: The lower bound of the price range for the search query.
    :param price_range_high: The upper bound of the price range for the search query.
    :return: A dictionary with the description, found price, and link, or an empty dict if no results.
    """
    url = "https://www.searchapi.io/api/v1/search"
    params = {
    "engine": "google_shopping",
    "q": description,
    "tbs": f"mr:1,avg_rating:400,price:1,ppr_min:{price_range_low},ppr_max:{price_range_high},sales:1",
    "api_key": serpapi_key,
    }
    search = GoogleSearch(params)
    results = search.get_dict().get('shopping_results', [])
    filters = results["filters"]


    if results:
        best_match = results[0]  # Assuming the first result is the best match
        return {
            "description": description,
            "price": best_match.get("price"),
            "link": best_match.get("link"),
            "rating": float(best_match.get("rating", 0))
        }

    return {}

def execute_parallel_searches(description: str, base_price_range: str) -> list:
    """
    Execute searches in parallel for the given description at three price points: low, mid, and high within ±10% range.

    :param description: The description of the gift item to search for.
    :param base_price_range: The base price range from GPT, formatted as "low-high".
    :return: A list of dictionaries, each containing the results of a search.
    """
    low, high = map(int, base_price_range.split('-'))
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


