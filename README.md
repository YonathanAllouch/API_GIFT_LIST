## Gift List Generator API

### Overview

The Gift List Generator API is a FastAPI-based application designed to create personalized gift lists using AI. By leveraging the power of GPT models, the API generates a list of gift suggestions based on user preferences such as list type, item count, recipient gender, and budget constraints. It features a robust backend with database integration for item storage and retrieval, and supports cross-origin requests to cater to various frontend clients.

### Features

Gift List Generation: Dynamically generate gift lists with AI-driven suggestions.
Database Integration: Store and retrieve gift items for efficient list management.
CORS Support: Configured to handle cross-origin requests, enabling seamless frontend integration.
Error Handling: Comprehensive error handling for a reliable user experience.

### Prerequisites

Python 3.x

FastAPI

Uvicorn (for running the server)

Sqlite

### Installation and Setup

Clone the repository:
```
  git clone https://github.com/YonathanAllouch/API_GIFT_LIST.git
```

Navigate to the project directory and install the requirements:
```
  cd main.py
  pip install -r requirements.txt
```

Ensure the database is set up as per the configuration in database.py.


Run the server using Uvicorn:
```
  uvicorn main:app --reload
```

### Usage

To generate a gift list, send a POST request to /generate-gift-list/ with the required parameters:


list_type: Type of gift list

number_of_items: Number of gift suggestions

gender_of_gifts: Gender preference for the gifts

price_range: Price range for the gifts


**Example request:**
```
{

  "list_type": "birthday",
  
  "number_of_items": 5,
  
  "gender_of_gifts": "for a 13 years old boy that like sport and cars",
  
  "price_range": "50 - 300"
  
}
```

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request with your changes.


## License

MIT License

## Demo

[![Gift List Demo]()](https://drive.google.com/file/d/1-VJ2LlgAoPcyW3DBflBB5U2FRnytccc2/view?usp=sharing)



